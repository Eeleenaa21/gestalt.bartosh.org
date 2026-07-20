#!/usr/bin/env python3
"""Download all articles from gestalt.bartosh.org and create Markdown files."""

import re
import os
import subprocess
import sys
import urllib.parse

ARTICLES = [
    ("chto-takoe-gestalt-terapiya", "Что такое гештальт-терапия?", "/статьи/что-такое-гештальт-терапия/"),
    ("ono-nastupit", "Оно наступит", "/статьи/оно-наступит/"),
    ("ya-ostrov", "Я — остров", "/статьи/я-остров/"),
    ("v-komnate-moej", "В комнате моей", "/статьи/в-комнате-моей/"),
    ("o-travme", "О травме", "/статьи/о-травме/"),
    ("prikazano-vyzhit", "Приказано выжить. Письмо счастья родителям подростков", "/статьи/приказано-выжить-письмо-счастья-родителям-подростков/"),
    ("depressiya-glazami-psihologa", "Депрессия глазами психолога", "/статьи/депрессия-глазами-психолога/"),
    ("depressiya-glazami-psihologa-2-chto-delat", "Депрессия глазами психолога-2. Что делать", "/статьи/депрессия-глазами-психолога-2-что-делать/"),
    ("materinstvo", "Материнство (О чём не пишут в глянцевых журналах)", "/статьи/материнство-о-чём-не-пишут-в-глянцевых-журналах/"),
    ("najti-soobshchnika", "Найти сообщника", "/статьи/найти-сообщника/"),
    ("pogovorit", "Поговорить", "/статьи/поговорить/"),
    ("ne-uhodi", "Не уходи", "/статьи/не-уходи/"),
    ("ya-budu-prodolzhat", "Я буду продолжать", "/статьи/я-буду-продолжать/"),
    ("ya-boyus-letat", "Я боюсь летать!", "/статьи/я-боюсь-летать/"),
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
    output_dir = "content/stati"
    os.makedirs(output_dir, exist_ok=True)

    for slug, title, url_path in ARTICLES:
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