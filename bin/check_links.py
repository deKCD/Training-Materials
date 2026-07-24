import re
import os
from typing import Dict, List, Tuple, Any
import requests

def parse_inline_and_verify(
    text: str, 
    base_dir: str, 
    references: Dict[str, str] = None,
    timeout: int = 5) -> Tuple[Dict[str, List[Any]], List[Dict[str, str]]]:
    """
    Finds links (URLs, Liquid images, Liquid file includes) in a markdown file string.
    Verifies accessibility for URLs and presence for local files.
    
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