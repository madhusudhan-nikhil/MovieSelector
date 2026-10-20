# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's test on the snippet:
snippet = text[text.find('What are you in the mood')-30:text.find('What are you in the mood')+35]
print("Original snippet:", repr(snippet))

try:
    fixed_snippet = snippet.encode('windows-1252').decode('utf-8')
    print("Fixed snippet (cp1252):", repr(fixed_snippet))
except Exception as e:
    print("Error with cp1252:", e)

try:
    fixed_latin1 = snippet.encode('latin1').decode('utf-8')
    print("Fixed snippet (latin1):", repr(fixed_latin1))
except Exception as e:
    print("Error with latin1:", e)
