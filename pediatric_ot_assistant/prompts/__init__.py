"""Prompt template loading.

Templates are Markdown files rendered with ``str.format``; keep literal
braces out of them (tests enforce that every placeholder resolves).
"""

from importlib import resources


def load_prompt(name: str) -> str:
    return (resources.files(__package__) / f"{name}.md").read_text(encoding="utf-8")
