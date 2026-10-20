# -*- coding: utf-8 -*-
with open('index.html', 'rb') as f:
    raw = f.read()

# Let's check the first 500 bytes
print("First 200 bytes:", raw[:200])

# Let's search for "What are you in the mood"
idx = raw.find(b"What are you in the mood")
if idx != -1:
    snippet = raw[max(0, idx-50):idx+50]
    print("Snippet around mood headline:", snippet)
