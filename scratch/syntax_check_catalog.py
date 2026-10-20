# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open('catalog.js', 'r', encoding='utf-8') as f:
    s = f.read()

open_curly = s.count('{')
close_curly = s.count('}')
open_square = s.count('[')
close_square = s.count(']')
print(f"catalog.js: curly {{{open_curly}/{close_curly}}}, square [{open_square}/{close_square}]")
if open_curly == close_curly and open_square == close_square:
    print("OK: catalog.js is syntactically balanced!")
