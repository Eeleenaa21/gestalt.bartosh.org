#!/usr/bin/env python3
"""Download chitatelskiy dnevnik sub-pages from gestalt.bartosh.org."""

import re
import os
import subprocess
import urllib.parse

BASE_URL = "https://gestalt.bartosh.org"

# Sub-pages with their URL slugs and titles
SUB_PAGES = [
    ("2014", "2014"),
    ("январь-2015", "Январь 2015"),
    ("февраль-2015", "Февраль 2015"),
    ("март-2015", "Март 2015"),
    ("апрель-2015", "Апрель 2015"),
    ("май-2015", "Май 2015"),
    ("лето-2015", "Лето 2015"),
    ("сентябрь-2015", "Сентябрь 2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
]

def extract_text_from_html(html):
    """Extract text from the page content area."""
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
    text = re.sub(r'<[^>]+>', '\n', content)

    text = text.replace('&nbsp;', ' ')
    text = text.replace('&', '&')
    text = text.replace('<', '<')
    text = text.replace('>', '>')
    text = text.replace('"', '"')

    # Remove leading numbers/asterisks/empty lines
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # Remove the title line (first line)
    if lines:
        lines = lines[1:]

    text = '\n\n'.join(lines)

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
    output_dir = "content/chitatelskiy-dnevnik"
    os.makedirs(output_dir, exist_ok=True)

    for slug, title in SUB_PAGES:
        url_path = f"/chitatelskiy-dnevnik/{slug}/"
        filename = f"{slug}.md"
        filepath = os.path.join(output_dir, filename)

        print(f"Downloading: {title}")
        print(f"  URL: {url_path}")

        html = download_page(url_path)
        if not html:
            print(f"  FAILED: no HTML received")
            continue

        if "Page Not Found" in html or "Oops!" in html:
            print(f"  FAILED: page returned 404")
            continue

        text = extract_text_from_html(html)
        if not text:
            print(f"  FAILED: could not extract text from HTML")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f'title: "{title}"\n')
            f.write(f'url: "/chitatelskiy-dnevnik/{slug}/"\n')
            f.write("draft: false\n")
            f.write("---\n\n")
            f.write(text)
            f.write("\n")

        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  OK: {filepath} ({size} bytes)")

    print("\nDone!")

if __name__ == "__main__":
    main()