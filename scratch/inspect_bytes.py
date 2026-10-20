# -*- coding: utf-8 -*-
with open('index.html', 'rb') as f:
    raw = f.read()

idx = raw.find(b"What are you in the mood")
span = raw[idx-35:idx+35]
print("Span bytes:", span)
print("Hex:", span.hex(' '))
