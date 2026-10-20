# -*- coding: utf-8 -*-
import json
import re

# Read catalog.js to get existing titles
with open('catalog.js', 'r', encoding='utf-8') as f:
    cat_raw = f.read()

# Extract existing objects in catalog.js
pattern = r'\{\s*id:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*year:\s*(\d+),\s*platform:\s*"([^"]+)",\s*platformName:\s*"([^"]+)",\s*format:\s*"([^"]+)",\s*runtime:\s*"([^"]+)",\s*imdb:\s*"([^"]+)",\s*rt:\s*"([^"]+)",\s*lang:\s*"([^"]+)",\s*langText:\s*"([^"]+)",\s*vibe:\s*"([^"]+)",\s*genres:\s*\[([^\]]*)\],\s*hook:\s*"([^"]+)",\s*searchUrl:\s*"([^"]+)"\s*\}'

matches = re.findall(pattern, cat_raw)
print(f"Parsed {len(matches)} structured items from catalog.js")

existing_ids = {m[0] for m in matches}
print(f"Total existing IDs: {len(existing_ids)}")
