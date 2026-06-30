import os
import re
import requests
from typing import Dict, List, Tuple, Any
from pathlib import Path
import json
import argparse


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def parse_markdown_metadata(markdown_text: str) -> Dict[str, Any]:
    """
    Parses the frontmatter metadata block delimited by '---' at the top 
    of a Markdown file into a dictionary.
    
    Args:
        markdown_text (str): The raw markdown string content.
        
    Returns:
        Dict[str, Any]: A dictionary containing the parsed metadata keys and values.
    """
    metadata = {}
    errors = []
    # extend metadata fields if needed
    REQUIRED_FIELDS = {"layout", "title", "description", "time_estimation", "level", "questions", "objectives", "key_points", "version", "life_cycle", 
                       "contributions", "authorship", "editing", "funding"}

    LIST_FIELDS = {"questions", "objectives", "key_points", "authorship", "editing", "funding"}
    KV_RE = re.compile(r"^([a-zA-Z0-9_-]+):\s*(.+)$", re.MULTILINE)
        
    # check if markdown file is empty
    lines = markdown_text.strip().splitlines()
    
    if not lines:
        return {}, [{"error": "Empty document."}]

    # check if metdata present
    if not re.match(r'^---\s*$', lines[0].strip()):
        return {}, [{"error": "Missing metadata part."}]

    # find the closing '---' delimiter
    end_idx = -1
    for i in range(1, len(lines)):
        if re.match(r'^---\s*$', lines[i].strip()):
            end_idx = i
            break

    # if no closing delimiter is found, it's not valid metadata
    if end_idx == -1:
        return {}, [{"error": "Unclosed metadata."}]

    # parse the lines within the metadata
    current_key = None
    parent_key = None  # Tracks nested scopes like 'contributions'
    
    for line_number, line in enumerate(lines[1:end_idx], start=2):
        raw = line.rstrip()
        # skip empty lines or comments
        if not raw.strip() or raw.strip().startswith("#"):
            continue

        stripped_line = raw.strip()
        indentation = len(raw) - len(raw.lstrip())

        if indentation == 0:
            parent_key = None
            
            
        if stripped_line.startswith("- "):
            value = stripped_line[2:].strip().strip('"').strip("'")
            # determine which key this list item belongs to
            if current_key in LIST_FIELDS:
                if current_key not in metadata:
                    metadata[current_key] = []
                if value:
                    metadata[current_key].append(value)
                
            elif parent_key == "contributions" and current_key:
                if parent_key not in metadata:
                    metadata[parent_key] = {}
                if current_key not in metadata[parent_key]:
                    metadata[parent_key][current_key] = []
                if value:
                    metadata[parent_key][current_key].append(value)
            continue   
        
            
        # metadata field and values
        if ":" in stripped_line:
            key, value = stripped_line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # indentation for nested metadata fields
            if indentation > 0 and key in {"authorship", "editing", "funding"}:
                parent_key = "contributions"
                current_key = key
                if parent_key not in metadata:
                    metadata[parent_key] = {}
                metadata[parent_key][current_key] = [] if not value else [value]
                continue
            elif key == "contributions":
                parent_key = "contributions"
                current_key = None
                metadata[key] = {}
                continue

            current_key = key

            if current_key in LIST_FIELDS:
                metadata[current_key] = []
                if value:
                    if value.startswith("- "):
                        value = value[2:].strip()
                    metadata[current_key].append(value)
            else:
                metadata[current_key] = value

    # validate required fields
    for field in REQUIRED_FIELDS:
        # Check presence
        if field not in metadata:
            errors.append({"error": f"Field '{field}' is missing."})
            continue
            
        field_value = metadata[field]
        if field_value == "" or field_value == {}:
            errors.append({"error": f"Field '{field}' is empty."})
            continue
    
        if field in LIST_FIELDS and isinstance(field_value, list) and len(field_value) == 0:
            errors.append({"error": f"Field '{field}' is empty."})
            continue
    
        if field == "contributions" and isinstance(field_value, dict):
            sub_fields = ["authorship", "editing", "funding"]
            for sub_field in sub_fields:
                if sub_field in field_value:
                    if field_value[sub_field] == "" or (isinstance(field_value[sub_field], list) and len(field_value[sub_field]) == 0):
                        errors.append({"error": f"Field 'contributions: {sub_field}' is empty."})
                else:
                    # authorship/editing/funding are completely missing inside contributions
                    errors.append({"error": f"Sub-field '{sub_field}' missing inside contributions."})
    
    return metadata, errors


def parse_blockquotes(markdown_text: str):
    """
    Parses custom markdown blockquotes and their attribute types (e.g. {: .comment}).

    Args:
        markdown_text: The raw markdown string to parse.

    Returns:
        A list of dicts, each containing 'content' (str), 'blockquote_type' 
        (str or None), and 'line' (int) starting from 1.
    """

    BLOCKQUOTE_RE = re.compile(r'^(>\s?)(.*)$') # learning box title
    ATTRIBUTE_RE = re.compile(r'^\{:\s*\.([a-zA-Z0-9_-]+)\s*\}$') # learning box type

    NESTED_BLOCKQUOTE_RE = re.compile(r'^(>>\s?)(.*)$') # nested learning box title
    NESTED_ATTRIBUTE_RE = re.compile(r'^>\{:\s*\.([a-zA-Z0-9_-]+)\s*\}$') # nested learning box type
    
    lines = markdown_text.split('\n')
    length = len(lines)
    
    tokens = [] # store final dict for error message
    nested_tokens = [] # error message for nested boxes
    
    pos = 0
    while pos < length:
        start = pos
        line = lines[pos]

        # check nested blockquote first
        if NESTED_BLOCKQUOTE_RE.match(line): 
            nested_content_lines = []
            blockquote_type = None

            while pos < length and NESTED_BLOCKQUOTE_RE.match(lines[pos]):
                nm = NESTED_BLOCKQUOTE_RE.match(lines[pos])
                nested_content_lines.append(nm.group(2))
                pos += 1

            # check for trailing nested attribute
            if pos < length:
                n_am = NESTED_ATTRIBUTE_RE.match(lines[pos].strip())
                if n_am:
                    blockquote_type = n_am.group(1)
                    pos += 1

            nested_tokens.append({
                "content": "\n".join(nested_content_lines), 
                "blockquote_type": blockquote_type, 
                "line": start + 1,
            })

        # check for standard blockquote
        elif BLOCKQUOTE_RE.match(line):
            content_lines = []
            blockquote_type = None
            # keep consuming standard blockquotes (stop if hit a nested one)
            while pos < length and BLOCKQUOTE_RE.match(lines[pos]) and not NESTED_BLOCKQUOTE_RE.match(lines[pos]):
                bm = BLOCKQUOTE_RE.match(lines[pos])
                content_lines.append(bm.group(2))
                pos += 1

            # check for trailing standard attribute
            if pos < length:
                am = ATTRIBUTE_RE.match(lines[pos].strip())
                if am:
                    blockquote_type = am.group(1)
                    pos += 1
                    
            tokens.append({
                "content": "\n".join(content_lines), 
                "blockquote_type": blockquote_type, 
                "line": start + 1,
            })
        else:
            pos += 1

    # merge final results
    tokens.extend(nested_tokens)
  
    return tokens

def validate_blockquote_types(tokens: list):
    """
    Validate that blockquote class corresponds to its title tag.

    Example:
        blockquote_type='comment'
        <comment-title>Note</comment-title>

    Returns:
        list of validation errors
    """
    
    TITLE_RE = re.compile(r'<([a-zA-Z0-9_-]+)-title>(.*?)</\1-title>', re.DOTALL)
    OPEN_TITLE_RE = re.compile(r'<([a-zA-Z0-9_-]+)-title>')
    
    errors = []

    for i in tokens:
        content = i.get("content", "")
        blockquote_type = i.get("blockquote_type")
        line = i.get("line")

        if not blockquote_type:
            continue

        # 1. Try valid full match first
        match = TITLE_RE.search(content)

        if not match:
            open_match = OPEN_TITLE_RE.search(content)

            if open_match:

                errors.append({
                    "line": line,
                    "error": (
                        f"Malformed title tag for blockquote type '{blockquote_type}': "
                        f"missing or incorrect closing tag. "
                        f"Correct tag: <{blockquote_type}-title></{blockquote_type}-title>"
                    )
                })
            else:
                errors.append({
                    "line": line,
                    "error": f"Missing title tag for blockquote type '{blockquote_type}'"
                })

            continue

        # 2. Validate type consistency
        title_type = match.group(1)

        if title_type != blockquote_type:
            errors.append({
                "line": line,
                "error": (
                    f"Blockquote type '{blockquote_type}' "
                    f"does not match title tag '{title_type}-title'"
                )
            })

    return errors

def parse_inline_and_verify(
    text: str, 
    base_dir: str, 
    references: Dict[str, str] = None,
    timeout: int = 5
) -> Tuple[Dict[str, List[Any]], List[Dict[str, str]]]:
    """
    Finds links (URLs, Liquid images, Liquid file includes) in a markdown file string.
    Verifies HTTP accessibility for URLs and presence for local files.
    
    Args:
        text (str): The markdown or document content string.
        base_dir (str): Root directory of the project to check local file relative paths.
        references (dict): Dictionary mapping lowercased reference IDs to URLs.
        timeout (int): Seconds to wait before timing out a web request.
    """
    
    result = {
        "text_links": [],
        "image_links": [],
        "file_links": []
    }
    errors = []
    references = references or {}

    # Captures  ![image_title]({{ "/tutorials/path/image.png" | relative_url }}){: .responsive-img }
    IMAGE_RE = re.compile(
        r'(!?\[([^\]]*)\])'
        r'(?:\((.*?)\)|\[([^\]]+)\])'
        r'(?:\{\:\s*\.([a-zA-Z0-9_-]+)\s*\})?'
    )
    # Liquid template file include matching: {% include _tutorials/path/file.md %}
    LIQUID_INCLUDE_RE = re.compile(r'{%\s*include\s+([\w\-/_\.]+)\s*%}')
    # Path inside an image relative_url wrap: ![image_title]({{ "/tutorials/path/image.png" | relative_url }}){: .responsive-img }
    LIQUID_URL_PATH_RE = re.compile(r'["\']([^"\']+)["\']')

    for mm in IMAGE_RE.finditer(text):
        line_number = text.count('\n', 0, mm.start()) + 1
        prefix = mm.group(1)
        inner_text = mm.group(2) or ""
        url = mm.group(3)
        ref_id = mm.group(4)
        css_class = mm.group(5) # captures 'responsive-img' from {: .responsive-img }
        is_image = prefix.startswith('!')

        if ref_id and ref_id.lower() in references:
            url = references[ref_id.lower()]
        if not url:
            continue
            
        url = url.strip()
        
        # Clean up Liquid syntax inside image tags if present
        # e.g., transforms {{ "/img/pic.png" | relative_url }} -> /img/pic.png
        if "| relative_url" in url or "site.baseurl" in url:
            path_match = LIQUID_URL_PATH_RE.search(url)
            if path_match:
                url = path_match.group(1)

        if is_image:
            if css_class == "responsive-img":
                image_meta = {
                    "alt_text": inner_text,
                    "url": url,
                    "line": line_number,
                }
                result["image_links"].append(image_meta)
            else:
                errors.append({"error": f"Image Liquid class is incorrect: line {line_number}"})
            
            # Verify image path
            if url.startswith(('http://', 'https://')):
                _verify_web_url(url, errors, timeout)
            else:
                _verify_local_file(url, base_dir, errors, line=line_number)
        else:
            item = {
                "text": inner_text, 
                "url": url,
                "line": line_number,
            }
            result["text_links"].append(item)
            
            # Verify text link url
            if url.startswith(('http://', 'https://')):
                _verify_web_url(url, errors, timeout, line_number)

    # 3. Extract and verify Liquid/Jekyll include files
    for fm in LIQUID_INCLUDE_RE.finditer(text):
        line_number = text.count('\n', 0, fm.start()) + 1
        file_path = fm.group(1).strip()
        result["file_links"].append({
            "file_path": file_path,
            "line": line_number,
        })
        
        # Verify inclusion target exists on disk
        _verify_local_file(file_path, base_dir, errors, line=line_number)

    return result, errors


def _verify_web_url(url: str, errors: list, timeout: int, line: int):
    """Helper to safely ping web URLs and collect errors."""
    try:
        # Use standard HEAD request for performance; fallback to GET if blocked
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        if resp.status_code == 405:
            resp = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
            
        if resp.status_code >= 400:
            errors.append({"error": f"URL broken or inaccessible (HTTP {resp.status_code}): {url}. Line {line}"})
    except requests.RequestException as e:
        errors.append({"error": f"URL connection failed: {url}. Details: {str(e)}. Line {line}"})


def _verify_local_file(target_path: str, base_dir: str, errors: list, line: int):
    """Helper to safely check local workspace files and collect errors."""

    file_path = target_path.replace("/tutorials", "/_tutorials", 1).lstrip("/")
    full_path = base_dir / file_path

    if not os.path.exists(full_path):
        errors.append({"error": f"Missing file at expected location: {full_path}. Line {line}"})


def get_args():
    parser = argparse.ArgumentParser(description="Training material validation. Example usage: python tutorial_content_validator.py --file_path=path/to/file.md --base_dir=~/Training-Materials --outfile=validation_results.json")
    parser.add_argument(
        "--file_path",
        type=str,
        required=True,
        help="Path to markdown file"
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        required=True,
        help="Tutorial directory for local file validation"
    )
    parser.add_argument(
        "--outfile",
        type=str,
        required=True,
        help="Path to output JSON file"
    )
    return parser.parse_args()


def main():
    options = get_args()
    print(f"Content validation: {options.file_path}")
    tutorial_name = options.file_path.split("_tutorials/")[1]

    result = []
    
    # load markdown file
    file = load_file(options.file_path)
    
    # validate metadata
    metadata, metadata_errors = parse_markdown_metadata(file)
    
    # validate blockquotes
    tokens = parse_blockquotes(file)
    blockquote_errors = validate_blockquote_types(tokens)
    
    # validate links and file presence
    links, link_errors = parse_inline_and_verify(file, base_dir=Path(options.base_dir), references=None, timeout=10)
    
    # collect error messages
    result.append({
        "tutorial": tutorial_name,
        "metadata": metadata_errors,
        "blockquotes": blockquote_errors,
        "links": link_errors,
    })


    # validate files if present, e.g. part_01.md
    for i in links["file_links"]:
        subfile_link = i.get("file_path") # link to included file
        subfile_path = Path(options.base_dir) / Path(subfile_link)
        # load included file
        subfile = load_file(subfile_path)
        # validate blockquotes
        tokens = parse_blockquotes(subfile)
        subfile_blockquote_errors = validate_blockquote_types(tokens)
        subfile_links, subfile_link_errors = parse_inline_and_verify(subfile, base_dir=Path(options.base_dir), references=None, timeout=10)

        result[0]["links"].append({
            "subfile":subfile_link, 
            "subfile_blockquotes":subfile_blockquote_errors, 
            "subfile_links":subfile_link_errors,
        })
    
    with open(options.outfile, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()