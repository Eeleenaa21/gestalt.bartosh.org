#!/usr/bin/env python3
"""Generate content/stati/_index.md from individual article files."""

import os
import re
import glob

ARTICLES_DIR = "content/stati"
OUTPUT_FILE = "content/stati/_index.md"


def read_front_matter_and_body(filepath):
    """Parse a markdown file with front matter.
    Returns (front_matter_dict, body_text)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match YAML front matter between --- markers
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, None

    yaml_text = match.group(1)
    body = match.group(2).strip()

    # Parse simple YAML fields
    fm = {}
    for line in yaml_text.split('\n'):
        line = line.strip()
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            fm[key] = value

    return fm, body


def make_summary(text, url, word_limit=70):
    """Create a Hugo-like summary from the article text.
    Returns text without HTML tags, first ~word_limit words,
    with 'читать дальше' link (Markdown-style)."""
    # Strip any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace but keep paragraph breaks (\n\n)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # single newlines -> space
    text = re.sub(r'[ \t]+', ' ', text)  # collapse spaces
    text = text.strip()

    if not text:
        return ''

    # Count total words
    all_words = text.split()
    if len(all_words) <= word_limit:
        return text

    words = all_words[:word_limit]
    summary_text = ' '.join(words) + f' [читать дальше]({url})'
    return summary_text


def main():
    articles = []

    # Read all article files except _index.md
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.md')))
    for filepath in files:
        basename = os.path.basename(filepath)
        if basename == '_index.md':
            continue

        fm, body = read_front_matter_and_body(filepath)
        if fm is None:
            print(f"WARNING: Could not parse {filepath}, skipping")
            continue

        title = fm.get('title', basename.replace('.md', ''))
        url = fm.get('url', f'/stati/{basename.replace(".md", "")}/')
        weight = int(fm.get('weight', 99))

        articles.append({
            'title': title,
            'url': url,
            'weight': weight,
            'body': body,
        })

    # Sort by weight
    articles.sort(key=lambda a: a['weight'])

    # Build the Markdown content
    md_parts = ['![Елена Бартош](/images/photo.png)']

    for article in articles:
        title = article['title']
        url = article['url']
        body = article['body']

        # Generate the link: heading with link
        md_parts.append(f'## [{title}]({url})')

        if body:
            summary = make_summary(body, url)
            md_parts.append(summary)

    md_body = '\n\n'.join(md_parts)

    # Read existing _index.md to preserve its front matter
    existing_fm = {}
    if os.path.exists(OUTPUT_FILE):
        fm, _ = read_front_matter_and_body(OUTPUT_FILE)
        if fm:
            existing_fm = fm

    # Build the new _index.md content with minimal front matter
    output = f'''---
title: "{existing_fm.get('title', 'Статьи')}"
url: "{existing_fm.get('url', '/stati/')}"
draft: false
---

{md_body}
'''

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated {OUTPUT_FILE} with {len(articles)} articles")


if __name__ == '__main__':
    main()