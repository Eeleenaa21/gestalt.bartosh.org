#!/usr/bin/env python3
"""Download all articles from gestalt.bartosh.org and create Markdown files."""

import re
import os
import subprocess
import sys
import urllib.parse

ARTICLES = [
    # 1
    ("chto-takoe-gestalt-terapiya", "Что такое гештальт-терапия?", "/статьи/что-такое-гештальт-терапия/"),
    # 2
    ("ono-nastupit", "Оно наступит", "/статьи/оно-наступит/"),
    # 3
    ("kotiki", "Котики", "/статьи/котики/"),
    # 4
    ("ya-ostrov", "Я — остров", "/статьи/я-остров/"),
    # 5
    ("takzhe-chelovek", "Тоже человек", "/статьи/тоже-человек/"),
    # 6
    ("v-komnate-moej", "В комнате моей", "/статьи/в-комнате-моей/"),
    # 7
    ("o-travme", "О травме", "/статьи/о-травме/"),
    # 8
    ("prikazano-vyzhit", "Приказано выжить. Письмо счастья родителям подростков", "/статьи/приказано-выжить-письмо-счастья-родителям-подростков/"),
    # 9
    ("depressiya-glazami-psihologa", "Депрессия глазами психолога", "/статьи/депрессия-глазами-психолога/"),
    # 10
    ("depressiya-glazami-psihologa-2-chto-delat", "Депрессия глазами психолога-2. Что делать", "/статьи/депрессия-глазами-психолога-2-что-делать/"),
    # 11
    ("materinstvo", "Материнство (О чём не пишут в глянцевых журналах)", "/статьи/материнство-о-чём-не-пишут-в-глянцевых-журналах/"),
    # 12
    ("najti-soobshchnika", "Найти сообщника", "/статьи/найти-сообщника/"),
    # 13
    ("pogovorit", "Поговорить", "/статьи/поговорить/"),
    # 14
    ("ne-uhodi", "Не уходи", "/статьи/не-уходи/"),
    # 15
    ("ya-budu-prodolzhat", "Я буду продолжать", "/статьи/я-буду-продолжать/"),
    # 16
    ("ya-boyus-letat", "Я боюсь летать!", "/статьи/я-боюсь-летать/"),
    # 17
    ("propisnye-istiny-pamyatka-klientu", "Прописные истины. Памятка клиенту", "/статьи/прописные-истины-памятка-клиенту/"),
    # 18
    ("igryaushchiy-terapevt", "Играющий терапевт", "/статьи/играющий-терапевт/"),
    # 19
    ("bes", "Бессилие", "/статьи/бессилие/"),
    # 20
    ("inozemcy", "Иноземцы", "/статьи/иноземцы/"),
    # 21
    ("ya-zdes-manifest", "Я здесь. Манифест", "/статьи/я-здесь-манифест/"),
    # 22
    ("sinye-s-mjagkim-ili-kiki-i-buba", "Синее с мягким, или Кики и Буба", "/статьи/синее-с-мягким-или-кики-и-буба/"),
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

    for i, (slug, title, url_path) in enumerate(ARTICLES, 1):
        print(f"Downloading: {title}")
        print(f"  URL: {url_path}")
        print(f"  Weight: {i}")

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
            f.write(f'weight: {i}\n')
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