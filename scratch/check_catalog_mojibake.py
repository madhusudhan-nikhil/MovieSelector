# -*- coding: utf-8 -*-
with open('catalog.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
mojibake_cat1 = re.findall(r'ð[^\s<"]+', text)
mojibake_cat2 = re.findall(r'â[^\s<"]+', text)
print('catalog.js ð count:', len(mojibake_cat1), mojibake_cat1[:5])
print('catalog.js â count:', len(mojibake_cat2), mojibake_cat2[:5])
