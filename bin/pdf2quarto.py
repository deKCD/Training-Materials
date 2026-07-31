import pymupdf
from PIL import Image, ImageStat
import io
import os
from textwrap import dedent
import argparse

# quarto slide size
SLIDE_WIDTH = 1050
SLIDE_HEIGHT = 700

# quarto slide delimiter
SLIDE_DELIMITER = "\n---\n"

# quarto slide metadata
metadata_placeholder = dedent("""\
---
title: "Your Presentation Title"
subtitle: "Your Subtitle"
author: "Your Name"
date: "2026-06-26"
format: 
  revealjs:
    width: 1050
    height: 700
    theme: default
    slide-number: true
    chalkboard: true
---
""")

def get_args():
    parser = argparse.ArgumentParser(description="Convert PDF to Quarto markdown.")
    parser.add_argument(
        "-s", "--source",
        type=str,
        required=True,
        help="Path to PDF file"
    )
    parser.add_argument(
        "-o", "--outfile",
        type=str,
        required=True,
        help="Path to output qmd file"
    )
    parser.add_argument(
        "-i", "--images",
        type=str,
        required=True,
        help="Path to extracted images directory"
        )
    return parser.parse_args()

# check if the image is mostly one color
def check_image_color(block):
    img = Image.open(io.BytesIO(block["image"]))
    stat = ImageStat.Stat(img.convert("L"))
    return stat.stddev[0]

def main():
    options = get_args()

    os.makedirs(options.images, exist_ok=True)

    doc = pymupdf.open(options.source)

    with open(options.outfile, "w", encoding="utf-8") as out:
        # write quarto metadata
        out.write(f"{metadata_placeholder}\n")

        image_index = 0

        for page_index, page in enumerate(doc):
            if page_index > 0:
                out.write(SLIDE_DELIMITER)

            # get PDF page size
            page_width, page_height = page.rect.width, page.rect.height
            # calculate scaling factors to fit the slide dimensions
            scale_x = SLIDE_WIDTH / page_width
            scale_y = SLIDE_HEIGHT / page_height

            # extract text and images from the page
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0: # text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()

                            if not text:
                                continue

                            # extract text position
                            x0, y0, x1, y1 = span["bbox"]

                            # scale the text position to fit the slide dimensions
                            x0 *= scale_x
                            y0 *= scale_y
                            x1 *= scale_x
                            y1 *= scale_y

                            text_position = (
                                f"left:{x0:.1f}px; "
                                f"top:{y0:.1f}px; "
                                f"font-size:{span['size']*scale_y:.1f}px;"
                            )

                            font_style = ""

                            if "Bold" in span["font"]:
                                font_style += "font-weight:bold;"

                            if "Italic" in span["font"]:
                                font_style += "font-style:italic;"

                            text_placeholder = (
                                f'\n<div style="position:absolute; '
                                f'{text_position} '
                                f'{font_style}">'
                                f'{text}'
                                f'</div>\n'
                            )

                            out.write(text_placeholder)

                elif block["type"] == 1: # image block
                    # check if the image is mostly one color
                    stat = check_image_color(block)
                    if stat < 1:
                        continue

                    image_index += 1
                    image_file = (
                        f"{options.images}/page_{page_index+1}"
                        f"-image_{image_index}.{block['ext']}"
                    )

                    with open(image_file, "wb") as img_out:
                        img_out.write(block["image"])

                    # extract image position and scale to fit the slide dimensions
                    x0, y0, x1, y1 = block["bbox"]
                    x0 *= scale_x
                    y0 *= scale_y
                    x1 *= scale_x
                    y1 *= scale_y

                    image_position = (
                        f"left:{x0:.1f}px; top:{y0:.1f}px; width:{x1-x0:.1f}px; height:{y1-y0:.1f}px; bottom:{y0-y1:.1f}px; right:{x1-x0:.1f}px; "
                        f"box-shadow:4px 4px 12px rgba(0,0,0,0.3);"
                    )

                    image_placeholder = (
                        f'\n![]({image_file})'
                        f'{{style="position:absolute; '
                        f'{image_position}"}}\n'
                    )       

                    out.write(
                        f"\n{image_placeholder}\n"
                    )      

if __name__ == "__main__":
    main()      