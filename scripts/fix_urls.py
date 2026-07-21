#!/usr/bin/env python3
"""Replace Cyrillic URLs with Latin equivalents in content files."""

import os

print("=== stati: set url = /stati/<filename> ===")
for f in os.listdir('content/stati'):
    if not f.endswith('.md') or f == '_index.md':
        continue
    path = os.path.join('content/stati', f)
    with open(path) as fh:
        c = fh.read()
    # Find url: line and replace it
    lines = c.split('\n')
    new_lines = []
    changed = False
    slug = f[:-3]  # remove .md
    for line in lines:
        if line.startswith('url:'):
            new_line = f'url: "/stati/{slug}/"'
            if line != new_line:
                changed = True
                line = new_line
        new_lines.append(line)
    if changed:
        with open(path, 'w') as fh:
            fh.write('\n'.join(new_lines))
        print(f'  {f} -> /stati/{slug}/')

print("=== sluchai: set url = /sluchai-iz-praktiki/<filename> ===")
for f in os.listdir('content/sluchai'):
    if not f.endswith('.md') or f == '_index.md':
        continue
    path = os.path.join('content/sluchai', f)
    with open(path) as fh:
        c = fh.read()
    lines = c.split('\n')
    new_lines = []
    changed = False
    slug = f[:-3]
    for line in lines:
        if line.startswith('url:'):
            new_line = f'url: "/sluchai-iz-praktiki/{slug}/"'
            if line != new_line:
                changed = True
                line = new_line
        new_lines.append(line)
    if changed:
        with open(path, 'w') as fh:
            fh.write('\n'.join(new_lines))
        print(f'  {f} -> /sluchai-iz-praktiki/{slug}/')

print("=== voprosy: set url = /voprosy-i-otvety/<category>/<number>/ ===")
# Files are named like chsto-so-mnoy-N.md, deti-N.md etc.
# Category is the prefix before -N
for f in os.listdir('content/voprosy'):
    if not f.endswith('.md') or f == '_index.md':
        continue
    path = os.path.join('content/voprosy', f)
    with open(path) as fh:
        c = fh.read()
    lines = c.split('\n')
    new_lines = []
    changed = False
    # Extract number from filename: e.g. chsto-so-mnoy-2.md -> 2
    parts = f[:-3].split('-')
    num = parts[-1]
    cat_part = '-'.join(parts[:-1])
    # Map to latin category
    cat_map = {
        'chto-so-mnoy': 'chto-so-mnoj',
        'deti': 'deti',
        'krizisy': 'krizisy-travmy-gore',
        'otnosheniya': 'otnosheniya',
        'raznoe': 'raznoe',
        'samoocenka': 'samoocenka',
        'trevozhnost': 'trevozhnost',
        'vzroslye-deti': 'vzroslye-deti',
    }
    if cat_part not in cat_map:
        print(f'  WARNING: unknown category {cat_part} in {f}')
        continue
    new_url = f'url: "/voprosy-i-otvety/{cat_map[cat_part]}/{num}/"'
    for line in lines:
        new_line = line
        if line.startswith('url:'):
            new_line = new_url
            if line != new_line:
                changed = True
        new_lines.append(new_line)
    if changed:
        with open(path, 'w') as fh:
            fh.write('\n'.join(new_lines))
        print(f'  {f} -> {new_url.strip()}')

print("=== chitatelskiy-dnevnik: set url ===")
for f in os.listdir('content/chitatelskiy-dnevnik'):
    if not f.endswith('.md') or f == '_index.md':
        continue
    path = os.path.join('content/chitatelskiy-dnevnik', f)
    with open(path) as fh:
        c = fh.read()
    lines = c.split('\n')
    new_lines = []
    changed = False
    slug = f[:-3]
    new_url = f'url: "/chitatelskiy-dnevnik/{slug}/"'
    for line in lines:
        if line.startswith('url:'):
            if line != new_url:
                changed = True
                line = new_url
        new_lines.append(line)
    if changed:
        with open(path, 'w') as fh:
            fh.write('\n'.join(new_lines))
        print(f'  {f} -> {new_url.strip()}')

print("\nDone")