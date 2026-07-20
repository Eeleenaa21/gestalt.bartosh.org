#!/usr/bin/env python3
"""Download all cases from gestalt.bartosh.org and create Markdown files."""

import re
import os
import subprocess
import urllib.parse

SLUCHAI = [
    ("ya-tebya-proshchayu", "Я тебя прощаю", "/случаи-из-практики/я-тебя-прощаю/"),
    ("kameshki-v-okean", "Камешки в океан", "/случаи-из-практики/камешки-в-океан/"),
    ("malchik", "Мальчик", "/случаи-из-практики/мальчик/"),
    ("begemoterapiya", "Бегемототерапия", "/случаи-из-практики/бегемототерапия/"),
    ("ne-skazhu", "Не скажу", "/случаи-из-практики/не-скажу/"),
    ("spasenie-na-vodah", "Спасение на водах, а также в горах и в небесах", "/случаи-из-практики/спасение-на-водах-а-также-в-горах-и-небесах/"),
    ("nichego-osobennogo", "Ничего особенного", "/случаи-из-практики/ничего-особенного/"),
    ("golosa", "Голоса", "/случаи-из-практики/голоса/"),
    ("veronika-reshaet-uletet", "Вероника решает улететь", "/случаи-из-практики/вероника-решает-улететь/"),
    ("s-drugoi-storony", "С другой стороны", "/случаи-из-практики/с-другой-стороны/"),
]

BASE_URL = "https://gestalt.bartosh.org"

def extract_text_from_html(html):
    """Extract text from the article page."""
    start = html.find('<div id="content_start"></div>')
    if start == -1:
        return None

    end_markers = [
        '<div id="cc-tp-sidebar"',
        '<div data-container="navigation">',
        '<div id="cc-matrix-1779556094"',
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

def download_article(url_path):
    """Download article page and return HTML."""
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
    output_dir = "content/sluchai"
    os.makedirs(output_dir, exist_ok=True)

    for slug, title, url_path in SLUCHAI:
        print(f"Downloading: {title}")
        print(f"  URL: {url_path}")

        html = download_article(url_path)
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

        # Remove the title from the beginning of the text if present
        if text.startswith(title):
            text = text[len(title):].lstrip('\n').lstrip()

        filename = f"{output_dir}/{slug}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f'title: "{title}"\n')
            f.write(f'url: "{url_path}"\n')
            f.write("draft: false\n")
            f.write("---\n\n")
            f.write(text)
            f.write("\n")

        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  OK: {filename} ({size} bytes)")
        else:
            print(f"  FAILED: file not created")

    print("\nDone!")

if __name__ == "__main__":
    main()