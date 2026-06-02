import json
import subprocess
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parents[1] / "lib" / "state.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(STATE), *args],
                          cwd=cwd, capture_output=True, text=True)


def test_steps_1_to_4_flow(tmp_path):
    assert run(["init", "demo", "--logline", "지하철 우산"], tmp_path).returncode == 0
    for step, fname in [("1", "briefs/concept.md"),
                        ("2", "briefs/shotlist.md"),
                        ("3", "assets/keyframes.json")]:
        run(["set-output", "demo", step, "--file", fname], tmp_path)
        assert run(["approve", "demo", step], tmp_path).returncode == 0
        assert run(["advance", "demo"], tmp_path).returncode == 0
    run(["set-output", "demo", "4", "--file", "briefs/prompts.json"], tmp_path)
    assert run(["advance", "demo"], tmp_path).returncode == 0
    s = json.loads((Path(tmp_path) / "projects" / "demo" / "state.json").read_text())
    assert s["currentStep"] == 5
    assert s["steps"]["3"]["gateApproved"] is True
    assert s["steps"]["4"]["status"] == "done"


def test_step_3_gate_blocks_without_approve(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    for step, fname in [("1", "briefs/concept.md"), ("2", "briefs/shotlist.md")]:
        run(["set-output", "demo", step, "--file", fname], tmp_path)
        run(["approve", "demo", step], tmp_path)
        run(["advance", "demo"], tmp_path)
    run(["set-output", "demo", "3", "--file", "assets/keyframes.json"], tmp_path)
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 3
    assert json.loads((Path(tmp_path) / "projects" / "demo" / "state.json").read_text())["currentStep"] == 3
