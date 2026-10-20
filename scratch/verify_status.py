# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open('catalog.js', 'r', encoding='utf-8') as f:
    cat = f.read()
with open('scratch/pool_snippet.js', 'r', encoding='utf-8') as f:
    pool = f.read()

base_ids = set(re.findall(r'id:\s*"([^"]+)"', cat))
pool_ids = set(re.findall(r'id:\s*"([^"]+)"', pool))
overlap = base_ids.intersection(pool_ids)

print(f"Base IDs: {len(base_ids)}")
print(f"Pool IDs: {len(pool_ids)}")
print(f"Overlap: {len(overlap)} (Must be 0)")
print(f"Total Offline Library: {len(base_ids) + len(pool_ids)}")
