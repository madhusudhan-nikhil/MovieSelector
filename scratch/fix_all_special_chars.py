# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's map each corrupted token to its clean, professional replacement:
REPLACEMENTS = {
    # Large composite emojis and corrupted sequences
    'ðŸ•µï¸\x8fâ€\x8dâ™‚ï¸\x8f': '🔍',
    'ðŸ“±âž¡ï¸\x8f': '📱 →',
    'ðŸ‘\x81ï¸\x8f': '👁️',
    'ðŸ•¶ï¸\x8f': '🕶️',
    'ðŸ—£ï¸\x8f': '🌐',
    'âš™ï¸\x8f': '⚙️',
    'â\x9d¤ï¸\x8f': '❤️',
    'ðŸ\x8d¿': '🍿',
    'ðŸ¤\x9d': '🤝',
    'ðŸŒ\x8d': '🌐',
    'ðŸ\x8d•': '🍕',
    'ðŸŽ\xad': '🎭',
    'ðŸ˜±': '😱',
    'ðŸ’¥': '💥',
    'ðŸ¤¯': '🤯',
    'ðŸŒ´': '🌴',
    'ðŸ”—': '🔗',
    'ðŸŽ¬': '🎬',
    'ðŸ“º': '📺',
    'ðŸŽ‰': '🎉',
    'ðŸŽ°': '🎰',
    'ðŸ”„': '🔄',
    'ðŸ‡®ðŸ‡³': '🇮🇳',
    'ðŸ‡¬ðŸ‡§': '🇬🇧',

    # Corrupted punctuation and symbols
    'â†’': '→',
    'â˜…': '★',
    'â€”': '—',
    'âš¡': '⚡',
    'âœ“': '✓',
    'â™¥': '♥',
    'â†—': '↗',
    'âœ•': '✕',
    'Â·': '·',
    '•': '•'
}

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

count_fixed = 0
for bad, good in REPLACEMENTS.items():
    if bad in content:
        num = content.count(bad)
        content = content.replace(bad, good)
        count_fixed += num
        print(f"Replaced {repr(bad)} -> {repr(good)} ({num} times)")

print(f"Total replacements made: {count_fixed}")

# Check if any other non-ascii tokens remain
import re
remaining_tokens = re.findall(r'[ðâÃŸŽœ™š\x80-\x9f\ufffd]', content)
print(f"Remaining suspicious characters: {len(remaining_tokens)}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved cleaned index.html!")
