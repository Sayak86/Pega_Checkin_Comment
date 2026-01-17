import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
