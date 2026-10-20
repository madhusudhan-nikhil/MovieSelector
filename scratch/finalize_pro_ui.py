# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update <title>
html = html.replace(
    '<title>StreamMood — Curated OTT Recommendations for India</title>',
    '<title>StreamMood &mdash; Curated OTT Recommendations for India</title>'
)

# 2. Update Settings Header icon
gear_svg = '''<span class="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-slate-800 text-slate-300">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </span>'''

html = html.replace('<span>⚙️</span> Settings &amp; Catalog Management', gear_svg + ' Settings &amp; Catalog Management')

# 3. Clean up renderWatchedView
html = html.replace("Watched ✓", "Watched &#10003;")
html = html.replace("${item.format === 'movie' ? '🎬 Movie' : '📺 Series'}", "${item.format === 'movie' ? 'Movie' : 'Web Series'}")
html = html.replace("· ★ ${item.imdb}", "&bull; &#9733; ${item.imdb}")

# 4. Clean up Roulette options
html = html.replace('{ emoji: "🍕", label: "Comedy", key: "comedy" }', '{ emoji: "😂", label: "Comedy", key: "comedy" }')
html = html.replace('document.getElementById("rouletteRating").textContent = `★ ${targetPick.imdb} IMDb`;', 'document.getElementById("rouletteRating").textContent = `&#9733; ${targetPick.imdb} IMDb`;')
html = html.replace("${targetPick.format === 'movie' ? '🎬 Feature Film' : '📺 Web Series'}", "${targetPick.format === 'movie' ? 'Feature Film' : 'Web Series'}")
html = html.replace('Watch Now →', 'Watch Now &rarr;')

# 5. Clean up Couple deck
html = html.replace('<span class="text-xs font-bold text-amber-400">★ ${item.imdb} IMDb</span>', '<span class="text-xs font-bold text-amber-400">&#9733; ${item.imdb} IMDb</span>')
html = html.replace("${item.format === 'movie' ? '🎬 Feature Film' : '📺 Web Series'}", "${item.format === 'movie' ? 'Feature Film' : 'Web Series'}")
html = html.replace("<span>🌐 ${item.langText}</span>", "<span>${item.langText}</span>")
html = html.replace("Swipe Right (❤️) to say YES, Left (✕) to pass", "Swipe Right (&hearts;) to say YES, Left (&times;) to pass")
html = html.replace("Swipe Right (❤️) or Left (✕)", "Swipe Right (&hearts;) or Left (&times;)")

# 6. Success text checkmarks
html = html.replace('✓ Refreshed!', '&#10003; Refreshed!')
html = html.replace('✓ Successfully', '&#10003; Successfully')
html = html.replace('✓ Catalog reset', '&#10003; Catalog reset')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Final polish applied successfully to index.html!")
