import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTRIBUTOR_LIST = BASE_DIR / "_data" / "contributors.yml"

def load_yaml():
    with open(CONTRIBUTOR_LIST, "r") as f:
        return yaml.safe_load(f) or []

def get_contributor_names(data):
    names = []

    for block in data:
        value = block.get("name", [])

        if isinstance(value, str):
            names.append(value)
        elif isinstance(value, list):
            names.extend(name for name in value if isinstance(name, str))

    return names