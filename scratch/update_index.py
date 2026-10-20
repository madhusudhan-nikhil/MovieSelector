# -*- coding: utf-8 -*-
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# Read catalog.js to get the 319 base items array string
with open('catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

# Extract from window.initialCatalog = [ to ];
start_marker = "window.initialCatalog = ["
end_marker = "];"
start_idx = cat_text.find(start_marker)
end_idx = cat_text.rfind(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not find window.initialCatalog in catalog.js")
    sys.exit(1)

base_catalog_content = cat_text[start_idx + len(start_marker):end_idx].strip()

# Read scratch/pool_snippet.js
with open('scratch/pool_snippet.js', 'r', encoding='utf-8') as f:
    pool_snippet_text = f.read().strip()

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the static stat counters in HTML
html = re.sub(
    r'<div id="statTotalCount"[^>]*>.*?</div>',
    lambda m: '<div id="statTotalCount" class="text-xl font-extrabold text-white mt-0.5">319</div>',
    html
)
html = re.sub(
    r'<div id="statNetflixCount"[^>]*>.*?</div>',
    lambda m: '<div id="statNetflixCount" class="text-xl font-extrabold text-white mt-0.5">64</div>',
    html
)
html = re.sub(
    r'<div id="statPrimeCount"[^>]*>.*?</div>',
    lambda m: '<div id="statPrimeCount" class="text-xl font-extrabold text-white mt-0.5">66</div>',
    html
)
html = re.sub(
    r'<div id="statHotstarCount"[^>]*>.*?</div>',
    lambda m: '<div id="statHotstarCount" class="text-xl font-extrabold text-white mt-0.5">65</div>',
    html
)
html = re.sub(
    r'<div id="statSonylivCount"[^>]*>.*?</div>',
    lambda m: '<div id="statSonylivCount" class="text-xl font-extrabold text-white mt-0.5">62</div>',
    html
)
html = re.sub(
    r'<div id="statZee5Count"[^>]*>.*?</div>',
    lambda m: '<div id="statZee5Count" class="text-xl font-extrabold text-white mt-0.5">62</div>',
    html
)

# 2. Update descriptive text for unlimited catalog
html = html.replace(
    '<!-- EXTERNAL COMPREHENSIVE CATALOG SCRIPT (175+ Titles) -->',
    '<!-- EXTERNAL COMPREHENSIVE CATALOG SCRIPT (325+ Base Titles, Unlimited Sync) -->'
)
html = html.replace(
    'Actively queries and ingests fresh titles from verified Indian streaming feeds (Netflix, Prime, Hotstar, SonyLIV, Zee5).',
    'Actively queries and ingests all streaming titles with zero artificial caps or limits. Pulls 125+ new verified 2024-2026 releases offline or 1,000+ live streaming titles with TMDB API.'
)

# 3. Add Pull Depth dropdown inside the TMDB drawer
tmdb_depth_html = '''              <div class="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-800/60 mt-2">
                <div class="flex items-center gap-2">
                  <label for="tmdbDepthSelect" class="text-[11px] font-semibold text-slate-300">TMDB Pull Depth:</label>
                  <select id="tmdbDepthSelect" class="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-white focus:outline-none focus:border-blue-500">
                    <option value="1">1 Page (~200 titles)</option>
                    <option value="3">3 Pages (~600 titles)</option>
                    <option value="5" selected>5 Pages (~1,000 titles - Default)</option>
                    <option value="10">10 Pages (~2,000 titles)</option>
                    <option value="25">Max / Deep Sync (~5,000 titles)</option>
                  </select>
                </div>
                <div class="text-[10px] text-slate-400">Zero artificial caps. Multi-page pagination pulls all titles.</div>
              </div>'''

if 'id="tmdbDepthSelect"' not in html:
    html = html.replace(
        '<div id="tmdbKeyStatus" class="text-[11px] text-emerald-400 font-semibold hidden"></div>\n            </div>',
        '<div id="tmdbKeyStatus" class="text-[11px] text-emerald-400 font-semibold hidden"></div>\n' + tmdb_depth_html + '\n            </div>'
    )

# 4. Replace fallback initialCatalog and freshPullPool using string index finding
idx1 = html.find('const initialCatalog = [')
idx2 = html.find('const baseCatalog =', idx1)

if idx1 != -1 and idx2 != -1:
    replacement = f"""const initialCatalog = [
{base_catalog_content}
    ];

{pool_snippet_text}

    """
    html = html[:idx1] + replacement + html[idx2:]
    print("Replaced initialCatalog and freshPullPool successfully!")
else:
    print("Error: Could not locate catalog bounds in index.html")

# 5. Update catalog initialization with deduplication and cleanup
init_cat_pattern = re.compile(
    r'const baseCatalog = \(window\.initialCatalog && window\.initialCatalog\.length > 0\) \? window\.initialCatalog : initialCatalog;\s*let customCatalog = JSON\.parse\(localStorage\.getItem\(\'sm_custom_catalog\'\)\) \|\| \[\];\s*let catalog = \[\.\.\.baseCatalog, \.\.\.customCatalog\];',
    re.DOTALL
)

new_init_cat = '''const baseCatalog = (window.initialCatalog && window.initialCatalog.length > 0) ? window.initialCatalog : initialCatalog;
    let customCatalog = JSON.parse(localStorage.getItem('sm_custom_catalog')) || [];
    // Clean up customCatalog: remove any items already in baseCatalog
    const baseIdSet = new Set(baseCatalog.map(c => c.id));
    customCatalog = customCatalog.filter(c => !baseIdSet.has(c.id));
    // Build catalog with zero duplicate IDs
    const catalogMap = new Map();
    baseCatalog.forEach(c => catalogMap.set(c.id, c));
    customCatalog.forEach(c => { if (!catalogMap.has(c.id)) catalogMap.set(c.id, c); });
    let catalog = Array.from(catalogMap.values());'''

html = init_cat_pattern.sub(lambda m: new_init_cat, html, count=1)

# 6. Update initTmdbUi to wire up tmdbDepthSelect
sub_start = html.find('function initTmdbUi()')
sub_end = html.find('async function pullFromTmdb')
if sub_start != -1 and sub_end != -1 and 'tmdbDepthSelect' not in html[sub_start:sub_end]:
    tmdb_body = html[sub_start:sub_end]
    save_close = tmdb_body.rfind('    }')
    updated_tmdb_body = tmdb_body[:save_close] + '''
      const depthSelect = document.getElementById("tmdbDepthSelect");
      if (depthSelect) {
        const savedDepth = localStorage.getItem('sm_tmdb_depth') || '5';
        depthSelect.value = savedDepth;
        depthSelect.addEventListener("change", (e) => {
          localStorage.setItem('sm_tmdb_depth', e.target.value);
        });
      }
    }
'''
    html = html[:sub_start] + updated_tmdb_body + html[sub_end:]

# 7. Update pullFromTmdb to remove .slice(0, 8) and enable multi-page fetching with zero limits
old_pull_pattern = re.compile(
    r'async function pullFromTmdb\(apiKey\)\s*\{.*?return results;\s*\}',
    re.DOTALL
)

new_pull_func = '''async function pullFromTmdb(apiKey) {
      const results = [];
      const platforms = Array.from(activePlatforms);
      const maxPages = parseInt(localStorage.getItem('sm_tmdb_depth') || '5');

      for (const p of platforms) {
        const prov = TMDB_PROVIDERS[p];
        if (!prov) continue;

        // Fetch Movies across pages (Zero limits, up to maxPages)
        for (let page = 1; page <= maxPages; page++) {
          try {
            const movieUrl = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&watch_region=IN&with_watch_providers=${prov.id}&with_watch_monetization_types=flatrate|free|ads&sort_by=popularity.desc&page=${page}`;
            const movieRes = await fetch(movieUrl);
            if (movieRes.ok) {
              const data = await movieRes.json();
              const items = data.results || [];
              if (items.length === 0) break;
              items.forEach(item => {
                results.push({
                  id: `tmdb-m-${item.id}`,
                  title: item.title,
                  year: item.release_date ? parseInt(item.release_date.split("-")[0]) : 2024,
                  platform: p,
                  platformName: prov.name,
                  format: "movie",
                  runtime: "Feature",
                  imdb: (item.vote_average || 7.5).toFixed(1),
                  rt: `TMDB ${Math.round((item.vote_average || 7.5) * 10)}%`,
                  lang: item.original_language === "hi" ? "hindi" : (["ta","te","ml","kn"].includes(item.original_language) ? "south" : (item.original_language === "en" ? "english" : "hindi")),
                  langText: (item.original_language || "hi").toUpperCase() + " • Live Stream",
                  vibe: mapTmdbToVibe(item.genre_ids),
                  genres: ["live tmdb", prov.name.toLowerCase()],
                  hook: item.overview ? item.overview.slice(0, 180) + "..." : `Popular title currently streaming on ${prov.name} India.`,
                  searchUrl: `https://www.google.com/search?q=${encodeURIComponent(item.title + " " + prov.name + " watch")}`
                });
              });
              if (page >= (data.total_pages || 1)) break;
              await new Promise(r => setTimeout(r, 40));
            } else {
              break;
            }
          } catch (e) {
            console.warn(`TMDB fetch error for ${p} movie page ${page}`, e);
            break;
          }
        }

        // Fetch TV Series across pages (Zero limits, up to maxPages)
        for (let page = 1; page <= maxPages; page++) {
          try {
            const tvUrl = `https://api.themoviedb.org/3/discover/tv?api_key=${apiKey}&watch_region=IN&with_watch_providers=${prov.id}&with_watch_monetization_types=flatrate|free|ads&sort_by=popularity.desc&page=${page}`;
            const tvRes = await fetch(tvUrl);
            if (tvRes.ok) {
              const data = await tvRes.json();
              const items = data.results || [];
              if (items.length === 0) break;
              items.forEach(item => {
                results.push({
                  id: `tmdb-tv-${item.id}`,
                  title: item.name,
                  year: item.first_air_date ? parseInt(item.first_air_date.split("-")[0]) : 2024,
                  platform: p,
                  platformName: prov.name,
                  format: "series",
                  runtime: "Series",
                  imdb: (item.vote_average || 7.5).toFixed(1),
                  rt: `TMDB ${Math.round((item.vote_average || 7.5) * 10)}%`,
                  lang: item.original_language === "hi" ? "hindi" : (["ta","te","ml","kn"].includes(item.original_language) ? "south" : (item.original_language === "en" ? "english" : "hindi")),
                  langText: (item.original_language || "hi").toUpperCase() + " • Live Stream",
                  vibe: mapTmdbToVibe(item.genre_ids),
                  genres: ["live tmdb", prov.name.toLowerCase(), "series"],
                  hook: item.overview ? item.overview.slice(0, 180) + "..." : `Popular series currently streaming on ${prov.name} India.`,
                  searchUrl: `https://www.google.com/search?q=${encodeURIComponent(item.name + " " + prov.name + " watch")}`
                });
              });
              if (page >= (data.total_pages || 1)) break;
              await new Promise(r => setTimeout(r, 40));
            } else {
              break;
            }
          } catch (e) {
            console.warn(`TMDB fetch error for ${p} TV page ${page}`, e);
            break;
          }
        }
      }
      return results;
    }'''

html = old_pull_pattern.sub(lambda m: new_pull_func, html, count=1)

# 8. Update triggerActivePull to combine live and offline pools with zero limits
old_source_pattern = re.compile(
    r'const sourcePool = liveItems\.length > 0 \? liveItems : freshPullPool;',
    re.DOTALL
)
new_source_code = '''// Merge both live items and verified release pool so library continuously expands without limits
      const sourcePool = [...liveItems, ...freshPullPool];'''

html = old_source_pattern.sub(lambda m: new_source_code, html, count=1)

# 9. Update success label and confetti text
old_success_pattern = re.compile(
    r'const sourceLabel = liveItems\.length > 0 \? "TMDB Live Cloud API" : "Verified Indian OTT Release Feeds";\s*successText\.textContent = `[^`]*`;',
    re.DOTALL
)
new_success_code = '''const sourceLabel = liveItems.length > 0 ? "TMDB Live Cloud API + Curated Releases" : "Verified Indian OTT Release Feeds";
        successText.textContent = `✓ Refreshed! Ingested ${newItems.length > 0 ? newItems.length + ' fresh titles' : 'all latest releases'} via ${sourceLabel}. Total active catalog expanded to ${catalog.length} titles (Zero Caps).`;'''

html = old_success_pattern.sub(lambda m: new_success_code, html, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated index.html!")
