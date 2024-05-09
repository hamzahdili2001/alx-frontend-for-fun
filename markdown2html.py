#!/usr/bin/python3
"""Markdown to HTML"""
import sys
import os


args = sys.argv

if len(args) != 3:
    print("Usage: ./markdown2html.py README.md README.html")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

if not os.path.exists(input_filename):
    print(f"Missing {input_filename}\n")
    sys.exit(1)

sys.exit(0)
