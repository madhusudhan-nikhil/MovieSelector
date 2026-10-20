# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?:\s+src="[^"]*")?>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} inline script blocks.")

for i, s in enumerate(scripts):
    s = s.strip()
    if not s:
        continue
    # Check brace balance
    open_curly = s.count('{')
    close_curly = s.count('}')
    open_square = s.count('[')
    close_square = s.count(']')
    open_paren = s.count('(')
    close_paren = s.count(')')
    print(f"Script {i}: curly {{{open_curly}/{close_curly}}}, square [{open_square}/{close_square}], paren ({open_paren}/{close_paren})")
    if open_curly != close_curly or open_square != close_square:
        print("WARNING: Mismatched brackets in script", i)
    else:
        print("OK: All brackets match perfectly in script", i)
