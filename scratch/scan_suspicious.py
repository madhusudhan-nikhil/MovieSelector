# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['index.html', 'catalog.js']:
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    # Search for any cp1252 artifact chars or replacement char
    matches = re.findall(r'[ðâÃŸŽœ™š\ufffd]', text)
    print(f"{fname}: suspicious chars found: {len(matches)}")
    if matches:
        print("Samples:", matches[:10])
