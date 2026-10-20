# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total lines in index.html: {len(lines)}")

mojibake_lines = []
for i, line in enumerate(lines, 1):
    if re.search(r'[ðâÃŸŽœ™š\x80-\x9f\ufffd]', line):
        # show raw bytes or repr
        mojibake_lines.append((i, line.strip()))

print(f"Total lines with potential mojibake: {len(mojibake_lines)}")
for line_no, content in mojibake_lines:
    # print safely using ascii representation
    print(f"Line {line_no}: {content.encode('ascii', 'backslashreplace').decode('ascii')[:120]}")
