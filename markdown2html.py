#!/usr/bin/python3
"""Markdown to HTML"""
import sys
import os
import re
import hashlib


args = sys.argv


def printerr(*arg, **kwargs):
    """Print to stderr"""
    print(*arg, file=sys.stderr, **kwargs)


def md5_hash(text):
    """
    Convert to MD5 hash.
    """
    return hashlib.md5(text.encode()).hexdigest()


def remove_all_c(text):
    """
    Remove all 'c' (case-insensitive)
    """
    return re.sub(r"[cC]", "", text)


def parse_special_syntax(line):
    """
    Handle special syntax conversions:
    - [[text]] -> MD5 hash of text
    - ((text)) -> text with all 'c' removed
    """
    # Convert [[text]] to MD5
    line = re.sub(
        r"\[\[(.*?)\]\]", lambda m: md5_hash(m.group(1)), line
    )

    # Convert ((text)) to text with all 'c' removed
    line = re.sub(
        r"\(\((.*?)\)\)", lambda m: remove_all_c(m.group(1)), line
    )

    return line


def parse_bold_and_italic(line):
    """
    Convert Markdown bold and italic to HTML.
    """

    line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)

    line = re.sub(r"__(.*?)__", r"<em>\1</em>", line)

    return line


def parse_headline(line):
    """Parse headline"""
    line = parse_special_syntax(line)
    heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
    if heading_match:
        level = len(heading_match.group(1))
        # content = heading_match.group(2)
        content = parse_bold_and_italic(heading_match.group(2))
        return "<h{level}>{content}</h{level}>".format(
            level=level, content=content
        )
    return None


def parse_unordered_list(lines):
    """parse unordered lists"""

    list_items = []
    line_count = 0

    for line in lines:
        line = parse_special_syntax(line)
        unordered_list_match = re.match(r"^\-\s+(.*)$", line)
        if unordered_list_match:
            # content = unordered_list_match.group(1)
            content = parse_bold_and_italic(
                unordered_list_match.group(1)
            )
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
        line = parse_special_syntax(line)
        ordered_list_match = re.match(r"^\*\s+(.*)$", line)
        if ordered_list_match:
            # content = ordered_list_match.group(1)
            content = parse_bold_and_italic(
                ordered_list_match.group(1)
            )
            list_items.append(f"<li>{content}</li>")
            line_count += 1
        else:
            break

    if list_items:
        html_list = "<ol>\n" + "\n".join(list_items) + "\n</ol>"
        return html_list, line_count
    else:
        return None, 0


def parse_paragraph(lines):
    """parse paragraph"""
    paragraph_lines = []
    line_count = 0

    for line in lines:
        stripped_line = line.rstrip()
        if stripped_line == "":  # End of paragraph
            break
        # content = parse_bold_and_italic(line.strip())
        content = parse_special_syntax(line.strip())
        # paragraph_lines.append(content)
        paragraph_lines.append(parse_bold_and_italic(content))
        line_count += 1

    if paragraph_lines:
        paragraph_content = "<br />\n".join(paragraph_lines)
        html_paragraph = f"<p>\n{paragraph_content}\n</p>"
        return html_paragraph, line_count
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

        # parse paragraph
        paragraph_html, count = parse_paragraph(md_lines[i:])
        if paragraph_html:
            lines.append(paragraph_html)
            i += count
            continue

        # lines.append(line)
        # lines.append(parse_bold_and_italic(line))
        lines.append(
            parse_bold_and_italic(parse_special_syntax(line))
        )
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
