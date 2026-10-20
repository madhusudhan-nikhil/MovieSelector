# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find non-ascii chars
non_ascii = set(re.findall(r'[^\x00-\x7F]', text))
print("Unique non-ASCII characters remaining in index.html:")
for ch in sorted(list(non_ascii)):
    print(f"  Char: {repr(ch)} (U+{ord(ch):04X}) count={text.count(ch)}")
