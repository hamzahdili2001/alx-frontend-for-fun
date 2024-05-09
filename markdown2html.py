#!/usr/bin/python3
"""Markdown to HTML"""
import sys
import os
import re


args = sys.argv


def printerr(*arg, **kwargs):
    """Print to stderr"""
    print(*arg, file=sys.stderr, **kwargs)


def parse_headline(line):
    """Parse headline"""
    heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2)
        return "<h{level}>{content}</h{level}>".format(
            level=level, content=content
        )
    return None


def parse_unordered_list(lines):
    """parse unordered lists"""

    list_items = []
    line_count = 0

    for line in lines:
        unordered_list_match = re.match(r"^\-\s+(.*)$", line)
        if unordered_list_match:
            content = unordered_list_match.group(1)
            list_items.append(f"<li>{content}</li>")
            line_count += 1
        else:
            break

    if list_items:
        html_list = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
        return html_list, line_count
    else:
        return None, 0


def parse_ordered_list(lines):
    """parse ordered lists"""
    list_items = []
    line_count = 0

    for line in lines:
        ordered_list_match = re.match(r"^\*\s+(.*)$", line)
        if ordered_list_match:
            content = ordered_list_match.group(1)
            list_items.append(f"<li>{content}</li>")
            line_count += 1
        else:
            break

    if list_items:
        html_list = "<ol>\n" + "\n".join(list_items) + "\n</ol>"
        return html_list, line_count
    else:
        return None, 0


def markdown_to_html(md_lines):
    """Convert markdown to html"""
    lines = []
    i = 0

    while i < len(md_lines):
        line = md_lines[i].rstrip()

        # parse heading
        html_heading = parse_headline(line)
        if html_heading:
            lines.append(html_heading)
            i += 1
            continue

        # parse unordered list
        unordered_list_html, count = parse_unordered_list(
            md_lines[i:]
        )
        if unordered_list_html:
            lines.append(unordered_list_html)
            i += count
            continue

        # parse ordered list
        ordered_list_html, count = parse_ordered_list(md_lines[i:])
        if ordered_list_html:
            lines.append(ordered_list_html)
            i += count
            continue

        lines.append(line)
        i += 1

    return lines


if __name__ == "__main__":
    if len(args) != 3:
        printerr("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    if not os.path.exists(input_filename):
        printerr("Missing {}".format(input_filename))
        sys.exit(1)

    try:
        with open(
            input_filename, "r", encoding="utf-8"
        ) as input_file, open(
            output_filename, "w", encoding="utf-8"
        ) as output_file:
            markdown_lines = input_file.readlines()
            html_lines = markdown_to_html(markdown_lines)

            for html_line in html_lines:
                output_file.write(html_line + "\n")

    except Exception as e:
        printerr("An error occurred:", str(e))
        sys.exit(1)

    sys.exit(0)
