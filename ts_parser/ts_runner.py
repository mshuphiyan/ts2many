import subprocess
import json
from pathlib import Path

def extract_ts_ast(ts_project_path: str):
    result = subprocess.run(
        ["node", "ts_parser/ts_morph_bridge.js", ts_project_path],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)
