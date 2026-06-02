import json
import subprocess
import sys
from pathlib import Path

STATE = Path(__file__).resolve().parents[1] / "lib" / "state.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(STATE), *args],
                          cwd=cwd, capture_output=True, text=True)


def test_steps_1_2_full_gate_flow(tmp_path):
    assert run(["init", "subway-umbrella", "--logline", "지하철 우산"], tmp_path).returncode == 0
    # step 1
    run(["set-output", "subway-umbrella", "1", "--file", "briefs/concept.md"], tmp_path)
    assert run(["approve", "subway-umbrella", "1"], tmp_path).returncode == 0
    assert run(["advance", "subway-umbrella"], tmp_path).returncode == 0
    # step 2
    run(["set-output", "subway-umbrella", "2", "--file", "briefs/shotlist.md"], tmp_path)
    assert run(["approve", "subway-umbrella", "2"], tmp_path).returncode == 0
    assert run(["advance", "subway-umbrella"], tmp_path).returncode == 0
    s = json.loads((Path(tmp_path) / "projects" / "subway-umbrella" / "state.json").read_text())
    assert s["currentStep"] == 3
    assert s["steps"]["1"]["status"] == "done"
    assert s["steps"]["2"]["gateApproved"] is True
