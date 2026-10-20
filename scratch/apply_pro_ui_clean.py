# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Taste Profile Active Banner (lines ~120)
old_banner_icon = '<span class="text-sm">⚡</span>'
new_banner_icon = '''<span class="inline-flex items-center justify-center w-5 h-5 rounded-md bg-amber-500/20 text-amber-400">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"/></svg>
        </span>'''

html = html.replace(old_banner_icon, new_banner_icon)
html = html.replace('Manage in Settings →', 'Manage in Settings &rarr;')

# 2. Update Headline & Share Button (lines ~140-150)
old_headline = '''          <h2 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
            <span>🎭</span> What are you in the mood for tonight?
          </h2>'''

new_headline = '''          <h2 class="text-base sm:text-lg font-black text-white">
            What are you in the mood for tonight?
          </h2>'''

html = html.replace(old_headline, new_headline)

old_share_btn = '''        <button id="copyShareLink" class="hidden sm:flex px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold items-center gap-1.5 border border-slate-700 transition-all">
          <span>🔗</span> Share Vibe Link
        </button>'''

new_share_btn = '''        <button id="copyShareLink" class="hidden sm:flex px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold items-center gap-1.5 border border-slate-700 transition-all">
          <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
          <span>Share Vibe Link</span>
        </button>'''

html = html.replace(old_share_btn, new_share_btn)

# 3. Replace Vibe Cards with professional SVG icons & badges
old_vibe_container = '''      <!-- 6 Engaging Visual Vibe Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4" id="vibeCardContainer">

        <!-- Card 1: Edge-of-Seat Thriller -->
        <button data-vibe="thriller" class="vibe-card vibe-card-selected p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">😱</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-blue-400 transition-colors">
            Edge-of-Seat Thrills
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Heart-pounding suspense, ticking clocks & shocking murder twists.
          </p>
        </button>

        <!-- Card 2: Feel Good & Laughs -->
        <button data-vibe="comedy" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">🍕</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-amber-400 transition-colors">
            Comfort & Pure Laughs
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Wholesome chuckles, quirky desi humor & zero emotional stress.
          </p>
        </button>

        <!-- Card 3: Mind-Melting Sci-Fi -->
        <button data-vibe="mindfuck" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">🤯</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-purple-400 transition-colors">
            Mind-Melting Puzzle
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Time loops, parallel dimensions & high-IQ cryptographic enigmas.
          </p>
        </button>

        <!-- Card 4: Gritty Underworld & Noir -->
        <button data-vibe="crime" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">🕶️</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-rose-400 transition-colors">
            Gritty Desi Noir
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Rustic gangsters, corrupt cops, raw power & morally gray chaos.
          </p>
        </button>

        <!-- Card 5: Popcorn Action & Swagger -->
        <button data-vibe="action" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">💥</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-orange-400 transition-colors">
            High-Octane Popcorn
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Spectacular action set-pieces, swagger, heists & adrenaline rush.
          </p>
        </button>

        <!-- Card 6: Emotional Depth & Heart -->
        <button data-vibe="drama" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="text-2xl sm:text-3xl mb-2">❤️</div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-emerald-400 transition-colors">
            Deep Emotion & Heart
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Soul-stirring journeys, timeless romance & unforgettable acting.
          </p>
        </button>

      </div>'''

new_vibe_container = '''      <!-- 6 Engaging Visual Vibe Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4" id="vibeCardContainer">

        <!-- Card 1: Edge-of-Seat Thriller -->
        <button data-vibe="thriller" class="vibe-card vibe-card-selected p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-red-950/70 border border-red-500/30 flex items-center justify-center mb-2.5 text-red-400 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-blue-400 transition-colors">
            Edge-of-Seat Thrills
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Heart-pounding suspense, ticking clocks & shocking murder twists.
          </p>
        </button>

        <!-- Card 2: Feel Good & Laughs -->
        <button data-vibe="comedy" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-amber-950/70 border border-amber-500/30 flex items-center justify-center mb-2.5 text-amber-400 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-amber-400 transition-colors">
            Comfort & Pure Laughs
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Wholesome chuckles, quirky desi humor & zero emotional stress.
          </p>
        </button>

        <!-- Card 3: Mind-Melting Sci-Fi -->
        <button data-vibe="mindfuck" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-purple-950/70 border border-purple-500/30 flex items-center justify-center mb-2.5 text-purple-400 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-purple-400 transition-colors">
            Mind-Melting Puzzle
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Time loops, parallel dimensions & high-IQ cryptographic enigmas.
          </p>
        </button>

        <!-- Card 4: Gritty Underworld & Noir -->
        <button data-vibe="crime" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-slate-800/80 border border-slate-600/40 flex items-center justify-center mb-2.5 text-slate-300 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-rose-400 transition-colors">
            Gritty Desi Noir
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Rustic gangsters, corrupt cops, raw power & morally gray chaos.
          </p>
        </button>

        <!-- Card 5: Popcorn Action & Swagger -->
        <button data-vibe="action" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-orange-950/70 border border-orange-500/30 flex items-center justify-center mb-2.5 text-orange-400 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-orange-400 transition-colors">
            High-Octane Popcorn
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Spectacular action set-pieces, swagger, heists & adrenaline rush.
          </p>
        </button>

        <!-- Card 6: Emotional Depth & Heart -->
        <button data-vibe="drama" class="vibe-card p-4 rounded-2xl border border-slate-800 bg-slate-900 text-left transition-all hover:border-slate-700 group relative overflow-hidden">
          <div class="w-10 h-10 rounded-xl bg-pink-950/70 border border-pink-500/30 flex items-center justify-center mb-2.5 text-pink-400 group-hover:scale-105 transition-transform">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/></svg>
          </div>
          <h3 class="text-xs sm:text-sm font-black text-white group-hover:text-emerald-400 transition-colors">
            Deep Emotion & Heart
          </h3>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">
            Soul-stirring journeys, timeless romance & unforgettable acting.
          </p>
        </button>

      </div>'''

html = html.replace(old_vibe_container, new_vibe_container)

# 4. Clean up Format & Language filter pills (lines ~225-240)
old_pills = '''        <!-- Format Pills -->
        <div class="flex items-center gap-1.5">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Format:</span>
          <button data-format="all" class="format-pill active px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white">All</button>
          <button data-format="movie" class="format-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">🎬 Movies</button>
          <button data-format="series" class="format-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">📺 Series</button>
        </div>

        <!-- Language Pills -->
        <div class="flex items-center gap-1.5">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Language:</span>
          <button data-lang="all" class="lang-pill active px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white">All</button>
          <button data-lang="hindi" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">🇮🇳 Hindi</button>
          <button data-lang="south" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">🌴 South</button>
          <button data-lang="english" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">🇬🇧 English</button>
        </div>'''

new_pills = '''        <!-- Format Pills -->
        <div class="flex items-center gap-1.5">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Format:</span>
          <button data-format="all" class="format-pill active px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white">All</button>
          <button data-format="movie" class="format-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">Movies</button>
          <button data-format="series" class="format-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">Web Series</button>
        </div>

        <!-- Language Pills -->
        <div class="flex items-center gap-1.5">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Language:</span>
          <button data-lang="all" class="lang-pill active px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white">All</button>
          <button data-lang="hindi" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">Hindi</button>
          <button data-lang="south" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">South Indian</button>
          <button data-lang="english" class="lang-pill px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">English &amp; Intl</button>
        </div>'''

html = html.replace(old_pills, new_pills)

# 5. Clean up Card template in renderVibeMatches to use clean ASCII entities and SVGs
old_card_meta = "<span>${item.format === 'movie' ? '🎬 Movie' : '📺 Series'} (${item.year})</span>"
new_card_meta = "<span>${item.format === 'movie' ? 'Movie' : 'Web Series'} (${item.year})</span>"
html = html.replace(old_card_meta, new_card_meta)

old_lang_meta = "<span>🌐 ${item.langText}</span>"
new_lang_meta = "<span class=\"font-medium text-slate-300\">${item.langText}</span>"
html = html.replace(old_lang_meta, new_lang_meta)

old_watched_btn = "<span>${isWatched ? '✓ Watched' : '👁️ Mark Watched'}</span>"
new_watched_btn = "<span>${isWatched ? '&#10003; Watched' : 'Mark Watched'}</span>"
html = html.replace(old_watched_btn, new_watched_btn)

old_imdb_star = "★ ${item.imdb} IMDb"
new_imdb_star = "&#9733; ${item.imdb} IMDb"
html = html.replace(old_imdb_star, new_imdb_star)

old_boost_icon = "<span>⚡</span>"
new_boost_icon = "<span class=\"text-emerald-400 font-bold\">&bull;</span>"
html = html.replace(old_boost_icon, new_boost_icon)

old_watch_arrow = "<span>↗</span>"
new_watch_arrow = "<span>&rarr;</span>"
html = html.replace(old_watch_arrow, new_watch_arrow)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Professional UI enhancements applied successfully to index.html!")
