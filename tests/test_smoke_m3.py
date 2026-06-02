import json
import subprocess
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parents[1] / "lib" / "state.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(STATE), *args],
                          cwd=cwd, capture_output=True, text=True)


def _advance_gated(slug, step, fname, cwd):
    run(["set-output", slug, step, "--file", fname], cwd)
    assert run(["approve", slug, step], cwd).returncode == 0
    assert run(["advance", slug], cwd).returncode == 0


def test_steps_1_to_6_flow(tmp_path):
    assert run(["init", "demo", "--logline", "지하철 우산"], tmp_path).returncode == 0
    _advance_gated("demo", "1", "briefs/concept.md", tmp_path)
    _advance_gated("demo", "2", "briefs/shotlist.md", tmp_path)
    _advance_gated("demo", "3", "assets/keyframes.json", tmp_path)
    run(["set-output", "demo", "4", "--file", "briefs/prompts.json"], tmp_path)
    assert run(["advance", "demo"], tmp_path).returncode == 0
    _advance_gated("demo", "5", "assets/clips.json", tmp_path)
    _advance_gated("demo", "6", "briefs/selects.md", tmp_path)
    s = json.loads((Path(tmp_path) / "projects" / "demo" / "state.json").read_text())
    assert s["currentStep"] == 7
    assert s["steps"]["5"]["gateApproved"] is True
    assert s["steps"]["6"]["gateApproved"] is True


def test_step_5_render_gate_blocks_without_approve(tmp_path):
    run(["init", "demo", "--logline", "x"], tmp_path)
    _advance_gated("demo", "1", "briefs/concept.md", tmp_path)
    _advance_gated("demo", "2", "briefs/shotlist.md", tmp_path)
    _advance_gated("demo", "3", "assets/keyframes.json", tmp_path)
    run(["set-output", "demo", "4", "--file", "briefs/prompts.json"], tmp_path)
    run(["advance", "demo"], tmp_path)
    run(["set-output", "demo", "5", "--file", "assets/clips.json"], tmp_path)
    r = run(["advance", "demo"], tmp_path)
    assert r.returncode == 3
    assert json.loads((Path(tmp_path) / "projects" / "demo" / "state.json").read_text())["currentStep"] == 5
