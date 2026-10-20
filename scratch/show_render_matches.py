# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('function renderVibeMatches()')
end_idx = text.find('function renderWatchedView()')

print("renderVibeMatches span:", start_idx, end_idx)
lines = text[start_idx:end_idx].split('\n')
for i, l in enumerate(lines[:85]):
    print(f"{i+1}: {l}")
