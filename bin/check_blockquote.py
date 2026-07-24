import re

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

        # allow both "hands_on" and "hands-on" for the hands_on blockquote
        if (
            (blockquote_type == "hands_on" and title_type in {"hands_on", "hands-on"})
            or title_type == blockquote_type):
            continue

        errors.append({
            "line": line,
            "error": (
                f"Blockquote type '{blockquote_type}' "
                f"does not match title tag '{title_type}-title'"
                )
        })

    return errors