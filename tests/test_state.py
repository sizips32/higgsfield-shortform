import json
import subprocess
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parents[1] / "lib" / "state.py"


def run(args, cwd):
    return subprocess.run(
        [sys.executable, str(STATE), *args],
        cwd=cwd, capture_output=True, text=True
    )


def read_state(cwd, slug):
    p = Path(cwd) / "projects" / slug / "state.json"
    return json.loads(p.read_text())


def test_init_creates_state(tmp_path):
    r = run(["init", "demo", "--logline", "우산"], tmp_path)
    assert r.returncode == 0
    s = read_state(tmp_path, "demo")
    assert s["slug"] == "demo"
    assert s["logline"] == "우산"
    assert s["currentStep"] == 1
    assert len(s["steps"]) == 7
    assert s["steps"]["1"]["name"] == "ideate"
    assert s["steps"]["4"]["gate"] is False


def test_init_twice_without_force_fails(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    r = run(["init", "demo", "--logline", "y"], tmp_path)
    assert r.returncode == 1


def test_read_field(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    r = run(["read", "demo", "--field", "currentStep"], tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "1"


def test_read_missing_exits_2(tmp_path):
    r = run(["read", "nope"], tmp_path)
    assert r.returncode == 2


def test_set_output_marks_done(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    r = run(["set-output", "demo", "1", "--file", "briefs/concept.md"], tmp_path)
    assert r.returncode == 0
    s = read_state(tmp_path, "demo")
    assert s["steps"]["1"]["status"] == "done"
    assert s["steps"]["1"]["output"] == "briefs/concept.md"


def test_advance_blocked_when_gate_not_approved(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    run(["set-output", "demo", "1", "--file", "briefs/concept.md"], tmp_path)
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 3
    s = read_state(tmp_path, "demo")
    assert s["currentStep"] == 1


def test_advance_blocked_when_not_done(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 3


def test_approve_requires_done(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    r = run(["approve", "demo", "1"], tmp_path)
    assert r.returncode == 4


def test_approve_then_advance(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    run(["set-output", "demo", "1", "--file", "briefs/concept.md"], tmp_path)
    assert run(["approve", "demo", "1"], tmp_path).returncode == 0
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 0
    assert read_state(tmp_path, "demo")["currentStep"] == 2


def test_non_gated_step_advances_without_approve(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    s_path = Path(tmp_path) / "projects" / "demo" / "state.json"
    s = json.loads(s_path.read_text())
    s["currentStep"] = 4
    s["steps"]["4"]["status"] = "done"
    s_path.write_text(json.dumps(s))
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 0
    assert read_state(tmp_path, "demo")["currentStep"] == 5


def test_corruption_recovers_from_backup(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    run(["set-output", "demo", "1", "--file", "briefs/concept.md"], tmp_path)
    s_path = Path(tmp_path) / "projects" / "demo" / "state.json"
    s_path.write_text("{ broken json")
    r = run(["read", "demo", "--field", "slug"], tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "demo"
