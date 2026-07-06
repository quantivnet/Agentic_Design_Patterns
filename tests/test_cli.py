import pytest

from conftest import EXAMPLES, FakeOTClient
from pediatric_ot_assistant import cli
from pediatric_ot_assistant.models import ReviewReport

MAYA = str(EXAMPLES / "maya_r.yaml")
DESHAWN = str(EXAMPLES / "deshawn_t.yaml")


@pytest.fixture
def fake_cli_client(monkeypatch):
    client = FakeOTClient(structured=ReviewReport(passed=True))
    monkeypatch.setattr(cli, "_client_factory", lambda: client)
    return client


def test_formats_lists_all(capsys):
    assert cli.main(["formats"]) == 0
    out = capsys.readouterr().out
    for value in ("iep", "progress-note", "teacher-checklist", "parent-handout", "summary"):
        assert value in out


def test_validate_ok():
    assert cli.main(["validate", "--case", MAYA, "--format", "iep"]) == 0


def test_validate_blocking_exit_code():
    assert cli.main(["validate", "--case", DESHAWN, "--format", "iep"]) == 2


def test_validate_all_formats_summary(capsys):
    assert cli.main(["validate", "--case", DESHAWN]) == 0
    err = capsys.readouterr().err
    assert "BLOCKED" in err and "ready" in err


def test_validate_missing_file():
    assert cli.main(["validate", "--case", "no/such/file.yaml"]) == 1


def test_validate_invalid_case(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("student:\n  grade: '2'\n")  # no name
    assert cli.main(["validate", "--case", str(bad)]) == 1


def test_generate_to_stdout(fake_cli_client, capsys):
    code = cli.main(["generate", "--case", MAYA, "--format", "iep"])
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("# Occupational Therapy Evaluation")
    assert "Reviewer: no findings." in captured.err


def test_generate_blocking_exit_code(fake_cli_client):
    assert cli.main(["generate", "--case", DESHAWN, "--format", "iep"]) == 2
    assert fake_cli_client.generate_calls == []


def test_generate_allow_missing(fake_cli_client):
    code = cli.main(
        ["generate", "--case", DESHAWN, "--format", "iep", "--allow-missing"]
    )
    assert code == 0
    assert len(fake_cli_client.generate_calls) == 1


def test_generate_output_collision(fake_cli_client, tmp_path):
    out = tmp_path / "doc.md"
    out.write_text("existing")
    args = ["generate", "--case", MAYA, "--format", "summary", "-o", str(out)]
    assert cli.main(args) == 3
    assert out.read_text() == "existing"
    assert cli.main(args + ["--force"]) == 0
    assert out.read_text().startswith("# Occupational Therapy Evaluation")


def test_generate_writes_file(fake_cli_client, tmp_path):
    out = tmp_path / "sub" / "doc.md"
    code = cli.main(
        ["generate", "--case", MAYA, "--format", "summary", "-o", str(out)]
    )
    assert code == 0
    assert out.exists()


def test_generate_phi_leak_exit_code(monkeypatch, tmp_path):
    leaky = FakeOTClient(document="# Doc\n\nMaya attends Lincoln Elementary.\n")
    monkeypatch.setattr(cli, "_client_factory", lambda: leaky)
    out = tmp_path / "doc.md"
    code = cli.main(
        ["generate", "--case", MAYA, "--format", "summary", "--redact", "-o", str(out)]
    )
    assert code == 4
    assert not out.exists()  # leaky document must never be written


def test_generate_redaction_map_on_stderr(fake_cli_client, capsys):
    fake_cli_client.document = "# Doc\n\n[STUDENT] did well.\n"
    code = cli.main(["generate", "--case", MAYA, "--format", "summary", "--redact"])
    assert code == 0
    captured = capsys.readouterr()
    assert "[STUDENT] <- Maya Rodriguez" in captured.err
    assert "Maya" not in captured.out
