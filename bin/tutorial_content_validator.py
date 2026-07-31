import os
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path
import argparse
from pprint import pprint

from check_metadata import parse_markdown_metadata
from check_blockquote import parse_blockquotes, validate_blockquote_types
from check_links import parse_inline_and_verify


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def get_args():
    parser = argparse.ArgumentParser(
        description="Training material validation. Example usage: python tutorial_content_validator.py --file_path=path/to/file.md --base_dir=~/Training-Materials"
        )
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
    return parser.parse_args()

def main():
    options = get_args()
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
        # validate file presence
        subfile_links, subfile_link_errors = parse_inline_and_verify(subfile, base_dir=Path(options.base_dir), references=None, timeout=10)

        result[0]["links"].append({
            "subfile":subfile_link, 
            "subfile_blockquotes":subfile_blockquote_errors, 
            "subfile_links":subfile_link_errors,
        })

    if result:
        subfiles = []
        for tutorial in result:
            print(f"\nTutorial: {tutorial_name}")
            print("=" * 80)
            for section in ("metadata", "blockquotes", "links"):
                issues = tutorial.get(section, [])
                if not issues:
                    continue
                
                print(f"\n{section.capitalize()}:")
                n = 1
                for issue in issues:
                    line = issue.get("line")
                    if "subfile" in issue:
                        subfiles.append(issue)
                        continue
                    if line:
                        print(f"  {n}. {issue['error']} (line {issue['line']})")
                    else:
                        print(f"  {n}. {issue['error']}")
                    n += 1

            # print subfile issues
            if subfiles:
                print("\nSubfile validation:")
                for subfile in subfiles:
                    has_issues = (
                        subfile.get("subfile_blockquotes") or subfile.get("subfile_links")
                    )

                    if not has_issues:
                        continue
                    print(f"\n {subfile['subfile']}")
                    if subfile["subfile_blockquotes"]:
                        print("    Blockquotes:")
                        for err in subfile["subfile_blockquotes"]:
                            print(f"      - {err['error']} (line {err['line']})")

                    if subfile["subfile_links"]:
                        print("    Links:")
                        for err in subfile["subfile_links"]:
                            line = err.get("line")
                            if line:
                                print(f"      - {err['error']} (line {line})")
                            else:
                                print(f"      - {err['error']}")


if __name__ == "__main__":
    main()