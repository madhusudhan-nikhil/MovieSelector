# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('catalog.js', 'r', encoding='utf-8') as f:
    text = f.read()

non_ascii = set(re.findall(r'[^\x00-\x7F]', text))
print("Unique non-ASCII characters in catalog.js:")
for ch in sorted(list(non_ascii)):
    print(f"  Char: {repr(ch)} (U+{ord(ch):04X}) count={text.count(ch)}")
