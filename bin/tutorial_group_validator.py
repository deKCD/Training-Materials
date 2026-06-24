import os
import sys
import yaml
from pathlib import Path

BASE_DIR = Path(".")
TUTORIALS_GROUP = BASE_DIR / "_data" / "tutorial_groups.yml"
TUTORIALS_DIR = BASE_DIR / "_tutorials/"

def load_yaml():
    with open(TUTORIALS_GROUP, "r") as f:
        return yaml.safe_load(f)

def get_defined_tutorials(data):
    names = []
    for block in data:
        tutorials = block.get("tutorials", [])
        names.extend(tutorials)
    return names

def get_existing_folders():
    return [p.name for p in TUTORIALS_DIR.iterdir() if p.is_dir()]
    
def main():
    data = load_yaml()

    defined = set(get_defined_tutorials(data))
    existing = set(get_existing_folders())

    missing_folders = defined - existing
    extra_folders = existing - defined

    errors = False

    if missing_folders:
        print("Missing folders for tutorials:")
        for m in sorted(missing_folders):
            print(f"  - {m}")
        errors = True

    if extra_folders:
        print("Existing folders not referenced in YAML:")
        for e in sorted(extra_folders):
            print(f"  - {e}")

if __name__ == "__main__":
    main()