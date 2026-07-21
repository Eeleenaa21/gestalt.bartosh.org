#!/usr/bin/env python3
"""Download rasskaziki from gestalt.bartosh.org and create Markdown file."""

import re
import os
import subprocess
import urllib.parse

BASE_URL = "https://gestalt.bartosh.org"
URL_PATH = "/rasskaziki/"

def extract_text_from_html(html):
    """Extract text from the page."""
    start = html.find('<div id="content_start"></div>')
    if start == -1:
        return None

    end_markers = [
        '<div id="cc-tp-sidebar"',
        '<div data-container="navigation">',
    ]

    end = len(html)
    for marker in end_markers:
        pos = html.find(marker, start)
        if pos != -1 and pos < end:
            end = pos

    content = html[start:end]

    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', content)

    text = text.replace('&nbsp;', ' ')
    text = text.replace('&', '&')
    text = text.replace('<', '<')
    text = text.replace('>', '>')
    text = text.replace('"', '"')

    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)

    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)

    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def download_page(url_path):
    """Download page and return HTML."""
    encoded_path = urllib.parse.quote(url_path, safe='/')
    url = BASE_URL + encoded_path
    result = subprocess.run(
        ["curl", "-s", "-L", url],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        print(f"  ERROR: curl failed: {result.stderr}")
        return None
    return result.stdout

def main():
    output_file = "content/rasskaziki.md"

    print(f"Downloading: Рассказики")
    print(f"  URL: {URL_PATH}")

    html = download_page(URL_PATH)
    if not html:
        print(f"  FAILED: no HTML received")
        return

    if "Page Not Found" in html or "Oops!" in html:
        print(f"  FAILED: page returned 404")
        return

    text = extract_text_from_html(html)
    if not text:
        print(f"  FAILED: could not extract text from HTML")
        return

    # Remove the intro text if present
    intro = 'А это мои рассказики. Они  не про работу, но всё равно по мотивам. Такие крошечные зарисовки из одного предложения. Про жизнь.'
    if intro in text:
        text = text[text.find(intro) + len(intro):].lstrip()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write('title: "Рассказики"\n')
        f.write('description: "Короткие рассказы из жизни"\n')
        f.write('url: "/rasskaziki/"\n')
        f.write("draft: false\n")
        f.write("---\n\n")
        f.write("![Елена Бартош](/images/photo.png)\n\n")
        f.write("А это мои рассказики. Они не про работу, но всё равно по мотивам. Такие крошечные зарисовки из одного предложения. Про жизнь.\n\n")
        f.write(text)
        f.write("\n")

    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        print(f"  OK: {output_file} ({size} bytes)")
    else:
        print(f"  FAILED: file not created")

    print("\nDone!")

if __name__ == "__main__":
    main()