import os
from typing import Dict, List, Tuple, Any
import yaml

def parse_markdown_metadata(markdown_text: str) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """
    Parses the YAML frontmatter metadata block delimited by '---'
    at the top of a Markdown file into a dictionary.

    Args:
        markdown_text (str): The raw markdown string content.

    Returns:
        Tuple[Dict[str, Any], List[Dict[str, str]]]:
            Parsed metadata dictionary and validation errors.
    """

    metadata = {}
    errors = []

    REQUIRED_FIELDS = {
        "layout",
        "title",
        "description",
        "time_estimation",
        "level",
        "keywords",
        "questions",
        "objectives",
        "key_points",
        "version",
        "life_cycle",
        "contributions",
        "authorship",
        "editing",
        "funding"
    }

    LIST_FIELDS = {
        "questions",
        "objectives",
        "key_points",
        "authorship",
        "editing",
        "funding"
    }

    # Check if markdown file is empty
    lines = markdown_text.strip().splitlines()

    if not lines:
        return {}, [{"error": "Empty document."}]

    # Check opening metadata delimiter
    if lines[0].strip() != "---":
        return {}, [{"error": "Missing metadata part."}]

    # Find closing delimiter
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}, [{"error": "Unclosed metadata."}]

    # Extract YAML block
    yaml_text = "\n".join(lines[1:end_idx])

    # Parse YAML
    try:
        metadata = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as exc:
        return {}, [{"error": f"Invalid YAML metadata: {exc}"}]

    # Validate metadata structure
    if not isinstance(metadata, dict):
        return {}, [{"error": "Metadata must be a YAML mapping."}]

    # Validate required fields
    for field in REQUIRED_FIELDS:

        # Special handling for nested contribution fields
        if field in {"authorship", "editing", "funding"}:
            continue

        if field not in metadata:
            errors.append({
                "error": f"Field '{field}' is missing."
            })
            continue

        value = metadata[field]

        if value == "" or value is None or value == {} or value == []:
            errors.append({
                "error": f"Field '{field}' is empty."
            })
            continue

        if field in LIST_FIELDS:
            if not isinstance(value, list) or len(value) == 0 or any(not isinstance(item, str) or item.strip() == "" for item in value):
                errors.append({
                    "error": f"Field '{field}' is empty."
                })

    # Validate contributions
    if "contributions" in metadata:

        contributions = metadata["contributions"]

        if not isinstance(contributions, dict):
            errors.append({
                "error": "Field 'contributions' must be a mapping."
            })

        else:
            for sub_field in ["authorship", "editing", "funding"]:

                if sub_field not in contributions:
                    errors.append({
                        "error": f"Sub-field '{sub_field}' missing inside contributions."
                    })
                    continue

                value = contributions[sub_field]

                if value == "" or value is None:
                    errors.append({
                        "error": f"Field 'contributions: {sub_field}' is empty."
                    })

                elif isinstance(value, list) and len(value) == 0:
                    # Empty lists are allowed for editing/funding
                    # but authorship must contain values
                    if sub_field == "authorship":
                        errors.append({
                            "error": "Field 'contributions: authorship' is empty."
                        })

    else:
        errors.append({
            "error": "Field 'contributions' is missing."
        })

    return metadata, errors