# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Find all tokens with non-ascii chars
tokens = re.findall(r'[^\x00-\x7F]+', text)
unique_tokens = sorted(list(set(tokens)), key=len, reverse=True)
print(f"Total non-ascii tokens: {len(tokens)}, Unique: {len(unique_tokens)}")

for t in unique_tokens:
    # let's try to reverse cp1252
    try:
        rev = t.encode('cp1252').decode('utf-8')
    except Exception as e:
        rev = f"<FAILED: {e}>"
    print(f"Token: {repr(t)} -> Reversed: {repr(rev)}")
