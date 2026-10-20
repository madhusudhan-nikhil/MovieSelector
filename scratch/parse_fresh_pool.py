# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('const freshPullPool = [')
end = html.find('const baseCatalog =', start)

pool_str = html[start:end]

pattern = r'\{\s*id:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*year:\s*(\d+),\s*platform:\s*"([^"]+)",\s*platformName:\s*"([^"]+)",\s*format:\s*"([^"]+)",\s*runtime:\s*"([^"]+)",\s*imdb:\s*"([^"]+)",\s*rt:\s*"([^"]+)",\s*lang:\s*"([^"]+)",\s*langText:\s*"([^"]+)",\s*vibe:\s*"([^"]+)",\s*genres:\s*\[([^\]]*)\],\s*hook:\s*"([^"]+)",\s*searchUrl:\s*"([^"]+)"\s*\}'

matches = re.findall(pattern, pool_str)
print(f"Parsed {len(matches)} structured items from freshPullPool")
pool_ids = {m[0] for m in matches}
print(f"Total pool IDs: {len(pool_ids)}")
