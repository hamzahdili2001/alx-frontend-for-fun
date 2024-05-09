#!/usr/bin/python3
"""Markdown to HTML"""
import sys
import os


args = sys.argv


def printerr(*arg, **kwargs):
    """Print to stderr"""
    print(*arg, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    if len(args) != 3:
        printerr("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    if not os.path.exists(input_filename):
        printerr("Missing {}".format(input_filename))
        sys.exit(1)

    sys.exit(0)
