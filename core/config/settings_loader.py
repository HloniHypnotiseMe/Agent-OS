"""
Agent-OS Core: Settings Loader
"""

import json
from pathlib import Path
from typing import Dict

def load_settings(path: str = None) -> Dict:
    if path is None:
        path = Path(__file__).parent.parent.parent / "settings.json"
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {"version": "1.0", "default_model": "claude-3-5-sonnet"}

settings = load_settings()