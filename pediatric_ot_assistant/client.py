"""Anthropic API wrapper.

This is the only module that imports the ``anthropic`` SDK. The pipeline
takes any object with this class's two public methods, which is what
lets the entire test suite run offline with a fake client.

Note for claude-sonnet-5: do not pass temperature/top_p/top_k and do not
prefill the assistant turn — both are rejected by the API. Adaptive
thinking is left at its default.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

DEFAULT_MODEL = "claude-sonnet-5"


def default_model() -> str:
    return os.getenv("OT_ASSIST_MODEL", DEFAULT_MODEL)


class OTAssistError(Exception):
    """A pipeline error with a message suitable for the CLI user."""


@dataclass
class GenerationResult:
    text: str
    stop_reason: str | None


def _system_blocks(system: str) -> list[dict]:
    # The system prompt is byte-stable across calls; caching it makes the
    # review call (and repeated generations) cheaper.
    return [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]


class OTClient:
    """Lazily-constructed Anthropic client with friendly error translation."""

    def __init__(self) -> None:
        self._client = None

    def _get(self):
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover
                raise OTAssistError(
                    "The 'anthropic' package is not installed. "
                    "Run: pip install -e ."
                ) from exc
            self._client = anthropic.Anthropic()
        return self._client

    def _translate(self, exc: Exception) -> OTAssistError:
        import anthropic

        if isinstance(exc, anthropic.AuthenticationError):
            return OTAssistError(
                "No usable Anthropic credentials. Set ANTHROPIC_API_KEY "
                "(see .env.example) or run 'ant auth login'."
            )
        if isinstance(exc, anthropic.APIConnectionError):
            return OTAssistError(f"Could not reach the Anthropic API: {exc}")
        if isinstance(exc, anthropic.APIStatusError):
            return OTAssistError(f"Anthropic API error ({exc.status_code}): {exc.message}")
        return OTAssistError(str(exc))

    def generate_text(
        self,
        system: str,
        prompt: str,
        model: str,
        max_tokens: int = 8000,
        verbose: bool = False,
    ) -> GenerationResult:
        client = self._get()
        try:
            with client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                system=_system_blocks(system),
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                if verbose:
                    for chunk in stream.text_stream:
                        print(chunk, end="", file=sys.stderr, flush=True)
                    print(file=sys.stderr)
                message = stream.get_final_message()
        except Exception as exc:
            raise self._translate(exc) from exc
        text = "".join(
            block.text for block in message.content if getattr(block, "text", None)
        )
        return GenerationResult(text=text, stop_reason=message.stop_reason)

    def parse_structured(
        self,
        system: str,
        prompt: str,
        output_model,
        model: str,
        max_tokens: int = 2000,
    ):
        client = self._get()
        try:
            message = client.messages.parse(
                model=model,
                max_tokens=max_tokens,
                system=_system_blocks(system),
                messages=[{"role": "user", "content": prompt}],
                output_format=output_model,
            )
        except Exception as exc:
            raise self._translate(exc) from exc
        if message.parsed_output is None:
            raise OTAssistError(
                "The model did not return the expected structured output "
                f"(stop_reason={message.stop_reason})."
            )
        return message.parsed_output
