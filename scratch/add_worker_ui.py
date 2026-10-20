# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Edge Worker drawer in Settings
edge_drawer_html = '''        <!-- Cloudflare Edge Worker API Settings (Non-Python Serverless Backend) -->
        <div class="pt-1">
          <details id="edgeWorkerDetailsDrawer" class="text-xs text-slate-400 group bg-slate-900/60 p-3 rounded-xl border border-slate-800">
            <summary class="cursor-pointer hover:text-slate-200 font-semibold select-none flex items-center justify-between">
              <span class="flex items-center gap-2">
                <span class="text-orange-400 font-bold">&#9729; Cloudflare Edge Worker:</span> Non-Python Serverless Backend (TypeScript / Hono)
              </span>
              <span class="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-slate-300">Expand &#9662;</span>
            </summary>
            <div class="mt-3 space-y-2.5 pt-2 border-t border-slate-800/80">
              <p class="text-[11px] text-slate-400 leading-relaxed">
                Connect your deployed Cloudflare Edge Worker (<code class="text-slate-300 font-mono">/worker</code> in repository) to pull live Indian OTT titles from your global edge cache with zero Python and zero server costs.
              </p>
              <div class="flex gap-2">
                <input type="url" id="edgeWorkerUrlInput" placeholder="https://streammood-edge.yourname.workers.dev" class="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono">
                <button id="saveEdgeWorkerUrlBtn" class="px-3.5 py-1.5 bg-orange-600 hover:bg-orange-500 text-white rounded-lg font-bold text-xs transition-all">
                  Connect Worker
                </button>
              </div>
              <div id="edgeWorkerStatus" class="text-[11px] text-emerald-400 font-semibold hidden"></div>
            </div>
          </details>
        </div>
'''

if 'id="edgeWorkerDetailsDrawer"' not in html:
    html = html.replace(
        '<!-- External Feed URL (Optional custom endpoint pull) -->',
        edge_drawer_html + '\n        <!-- External Feed URL (Optional custom endpoint pull) -->'
    )

# 2. Add Edge Worker UI logic in JavaScript (inside initTmdbUi or separate initEdgeWorkerUi)
edge_worker_js = '''
    function initEdgeWorkerUi() {
      const savedUrl = localStorage.getItem('sm_edge_worker_url') || '';
      const input = document.getElementById("edgeWorkerUrlInput");
      const status = document.getElementById("edgeWorkerStatus");
      const saveBtn = document.getElementById("saveEdgeWorkerUrlBtn");

      if (input && savedUrl) {
        input.value = savedUrl;
        if (status) {
          status.textContent = "✓ Connected to Cloudflare Edge Worker (" + savedUrl + ")";
          status.classList.remove("hidden");
        }
      }

      if (saveBtn) {
        saveBtn.addEventListener("click", () => {
          let val = (input ? input.value : "").trim();
          if (val) {
            if (val.endsWith('/')) val = val.slice(0, -1);
            localStorage.setItem('sm_edge_worker_url', val);
            if (status) {
              status.textContent = "✓ Connected to Cloudflare Edge Worker (" + val + ")";
              status.classList.remove("hidden");
            }
          } else {
            localStorage.removeItem('sm_edge_worker_url');
            if (status) {
              status.textContent = "Edge Worker cleared. Using direct browser TMDB API.";
              status.classList.remove("hidden");
            }
          }
        });
      }
    }
'''

if 'function initEdgeWorkerUi' not in html:
    html = html.replace('// Catalog Statistics Breakdown', edge_worker_js + '\n    // Catalog Statistics Breakdown')

# 3. Call initEdgeWorkerUi() in initial run
if 'initEdgeWorkerUi();' not in html:
    html = html.replace('initTmdbUi();', 'initTmdbUi();\n    initEdgeWorkerUi();')

# 4. In triggerActivePull, check for edge worker URL
old_sync_logic = '''      const tmdbKey = (localStorage.getItem('sm_tmdb_key') || '').trim();
      let liveItems = [];'''

new_sync_logic = '''      const tmdbKey = (localStorage.getItem('sm_tmdb_key') || '').trim();
      const edgeWorkerUrl = (localStorage.getItem('sm_edge_worker_url') || '').trim();
      const tmdbDepth = parseInt(localStorage.getItem('sm_tmdb_depth') || '5');
      let liveItems = [];

      // Check if Cloudflare Edge Worker is connected
      if (edgeWorkerUrl) {
        progressStatus.innerHTML = `<span class="inline-block w-3 h-3 border-2 border-orange-400 border-t-transparent rounded-full animate-spin"></span> Querying Cloudflare Edge Worker (${edgeWorkerUrl}/api/catalog)...`;
        progressBar.style.width = "40%";
        progressPercent.textContent = "40%";
        try {
          const edgeRes = await fetch(`${edgeWorkerUrl}/api/catalog?depth=${tmdbDepth}&api_key=${encodeURIComponent(tmdbKey)}`);
          if (edgeRes.ok) {
            const edgeData = await edgeRes.json();
            if (edgeData.titles && edgeData.titles.length > 0) {
              liveItems = edgeData.titles;
            }
          }
        } catch (edgeErr) {
          console.warn("Edge worker fetch failed, falling back to direct browser TMDB pull", edgeErr);
        }
      }'''

html = html.replace(old_sync_logic, new_sync_logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added Edge Worker support to index.html successfully!")
