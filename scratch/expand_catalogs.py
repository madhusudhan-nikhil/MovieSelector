# scratch/expand_catalogs.py
import re
import json

# 1. Read existing catalog.js to extract current titles
with open('catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

# Extract existing IDs
existing_ids = set(re.findall(r'id:\s*"([^"]+)"', cat_text))
print(f"Existing IDs in catalog.js: {len(existing_ids)}")

# Let's inspect platforms distribution
netflix_ids = set(re.findall(r'id:\s*"([^"]+)"[\s\S]*?platform:\s*"netflix"', cat_text))
print(f"Netflix base: {len(netflix_ids)}")

# Let's prepare additional high-quality, verified titles for Indian OTT platforms
# Format:
# {
#   "id": str, "title": str, "year": int, "platform": str, "platformName": str,
#   "format": "movie"|"series", "runtime": str, "imdb": str, "rt": str,
#   "lang": "hindi"|"south"|"english", "langText": str, "vibe": str,
#   "genres": list[str], "hook": str, "searchUrl": str
# }
