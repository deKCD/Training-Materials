import os
import re
import requests
from typing import Dict, List, Tuple, Any
from pathlib import Path
import json
import argparse

from check_metadata import parse_markdown_metadata
from check_blockquote import parse_blockquotes, validate_blockquote_types
from check_links import parse_inline_and_verify


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def get_args():
    parser = argparse.ArgumentParser(description="Training material validation. Example usage: python tutorial_content_validator.py --file_path=path/to/file.md --base_dir=~/Training-Materials --outfile=validation_results.json")
    parser.add_argument(
        "-f", "--file_path",
        type=str,
        required=True,
        help="Path to markdown file"
    )
    parser.add_argument(
        "-b", "--base_dir",
        type=str,
        required=True,
        help="Tutorial directory for local file validation"
    )
    parser.add_argument(
        "-o", "--outfile",
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


    # validate "partial" files if present, e.g. part_01.md
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