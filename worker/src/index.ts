import { Hono } from 'hono';
import { cors } from 'hono/cors';

export interface Env {
  STREAMMOOD_KV?: KVNamespace;
  TMDB_API_KEY?: string;
  ENVIRONMENT?: string;
  DEFAULT_WATCH_REGION?: string;
}

export interface StreamMoodItem {
  id: string;
  title: string;
  year: number;
  platform: 'netflix' | 'prime' | 'hotstar' | 'sonyliv' | 'zee5';
  platformName: string;
  format: 'movie' | 'series';
  runtime: string;
  imdb: string;
  rt: string;
  lang: string;
  langText: string;
  vibe: 'thriller' | 'comedy' | 'mindfuck' | 'crime' | 'action' | 'drama';
  genres: string[];
  hook: string;
  searchUrl: string;
}

const TMDB_PROVIDERS: Record<string, { id: number; name: string }> = {
  netflix: { id: 8, name: 'Netflix' },
  prime: { id: 119, name: 'Prime Video' },
  hotstar: { id: 122, name: 'JioHotstar' },
  sonyliv: { id: 237, name: 'SonyLIV' },
  zee5: { id: 232, name: 'Zee5' },
};

function mapTmdbToVibe(genreIds?: number[]): StreamMoodItem['vibe'] {
  if (!genreIds || genreIds.length === 0) return 'drama';
  const g = new Set(genreIds);
  if (g.has(53) || g.has(27)) return 'thriller'; // Thriller, Horror
  if (g.has(80)) return 'crime'; // Crime
  if (g.has(35)) return 'comedy'; // Comedy
  if (g.has(878) || g.has(9648)) return 'mindfuck'; // Sci-Fi, Mystery
  if (g.has(28) || g.has(12)) return 'action'; // Action, Adventure
  return 'drama';
}

function mapLanguage(langCode?: string): { lang: string; langText: string } {
  if (langCode === 'hi') return { lang: 'hindi', langText: 'Hindi (Original)' };
  if (['ta', 'te', 'ml', 'kn'].includes(langCode || '')) {
    const langNames: Record<string, string> = { ta: 'Tamil', te: 'Telugu', ml: 'Malayalam', kn: 'Kannada' };
    return { lang: 'south', langText: `${langNames[langCode || 'ta']} (Regional)` };
  }
  if (langCode === 'en') return { lang: 'english', langText: 'English (Original)' };
  return { lang: 'hindi', langText: `${(langCode || 'hi').toUpperCase()} Stream` };
}

async function fetchFromTmdb(apiKey: string, maxPages: number = 3): Promise<StreamMoodItem[]> {
  const items: StreamMoodItem[] = [];

  for (const [key, prov] of Object.entries(TMDB_PROVIDERS)) {
    // 1. Fetch Movies
    for (let page = 1; page <= maxPages; page++) {
      try {
        const movieUrl = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&watch_region=IN&with_watch_providers=${prov.id}&with_watch_monetization_types=flatrate|free|ads&sort_by=popularity.desc&page=${page}`;
        const res = await fetch(movieUrl);
        if (!res.ok) break;
        const data = await res.json() as any;
        const results = data.results || [];
        if (results.length === 0) break;

        for (const item of results) {
          const langInfo = mapLanguage(item.original_language);
          items.push({
            id: `tmdb-m-${item.id}`,
            title: item.title,
            year: item.release_date ? parseInt(item.release_date.split('-')[0]) : 2024,
            platform: key as any,
            platformName: prov.name,
            format: 'movie',
            runtime: 'Feature Film',
            imdb: (item.vote_average || 7.5).toFixed(1),
            rt: `TMDB ${Math.round((item.vote_average || 7.5) * 10)}%`,
            lang: langInfo.lang,
            langText: langInfo.langText,
            vibe: mapTmdbToVibe(item.genre_ids),
            genres: ['live edge pull', prov.name.toLowerCase()],
            hook: item.overview ? item.overview.slice(0, 180) + '...' : `Top-rated title currently streaming on ${prov.name} India.`,
            searchUrl: `https://www.google.com/search?q=${encodeURIComponent(item.title + ' ' + prov.name + ' watch')}`
          });
        }
        if (page >= (data.total_pages || 1)) break;
      } catch (err) {
        console.warn(`TMDB movie fetch failed for ${key} page ${page}`, err);
        break;
      }
    }

    // 2. Fetch TV Series
    for (let page = 1; page <= maxPages; page++) {
      try {
        const tvUrl = `https://api.themoviedb.org/3/discover/tv?api_key=${apiKey}&watch_region=IN&with_watch_providers=${prov.id}&with_watch_monetization_types=flatrate|free|ads&sort_by=popularity.desc&page=${page}`;
        const res = await fetch(tvUrl);
        if (!res.ok) break;
        const data = await res.json() as any;
        const results = data.results || [];
        if (results.length === 0) break;

        for (const item of results) {
          const langInfo = mapLanguage(item.original_language);
          items.push({
            id: `tmdb-tv-${item.id}`,
            title: item.name,
            year: item.first_air_date ? parseInt(item.first_air_date.split('-')[0]) : 2024,
            platform: key as any,
            platformName: prov.name,
            format: 'series',
            runtime: 'Web Series',
            imdb: (item.vote_average || 7.5).toFixed(1),
            rt: `TMDB ${Math.round((item.vote_average || 7.5) * 10)}%`,
            lang: langInfo.lang,
            langText: langInfo.langText,
            vibe: mapTmdbToVibe(item.genre_ids),
            genres: ['live edge pull', prov.name.toLowerCase(), 'series'],
            hook: item.overview ? item.overview.slice(0, 180) + '...' : `Critically acclaimed series currently streaming on ${prov.name} India.`,
            searchUrl: `https://www.google.com/search?q=${encodeURIComponent(item.name + ' ' + prov.name + ' watch')}`
          });
        }
        if (page >= (data.total_pages || 1)) break;
      } catch (err) {
        console.warn(`TMDB TV fetch failed for ${key} page ${page}`, err);
        break;
      }
    }
  }

  return items;
}

const app = new Hono<{ Bindings: Env }>();

// Enable CORS for all origins (native browser friendly)
app.use('*', cors({
  origin: '*',
  allowMethods: ['GET', 'POST', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
}));

// Root Health & API Info
app.get('/', (c) => {
  return c.json({
    service: 'StreamMood India Serverless Edge API',
    runtime: 'Cloudflare Workers (TypeScript / Hono)',
    status: 'online',
    region: 'IN (India OTT Feeds)',
    endpoints: {
      catalog: 'GET /api/catalog?depth=3&refresh=false',
      sync: 'POST /api/sync',
      providers: 'GET /api/providers',
      search: 'GET /api/search?q={query}',
    }
  });
});

app.get('/api/health', (c) => {
  return c.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// GET /api/providers
app.get('/api/providers', (c) => {
  return c.json({
    region: 'IN',
    providers: TMDB_PROVIDERS
  });
});

// GET /api/catalog
app.get('/api/catalog', async (c) => {
  const depth = parseInt(c.req.query('depth') || '3');
  const forceRefresh = c.req.query('refresh') === 'true';
  const apiKey = c.req.query('api_key') || c.env.TMDB_API_KEY || '';

  const cacheKey = `catalog_in_d${depth}`;

  // Check Cloudflare KV if available
  if (c.env.STREAMMOOD_KV && !forceRefresh) {
    try {
      const cached = await c.env.STREAMMOOD_KV.get(cacheKey, 'json');
      if (cached) {
        return c.json({
          source: 'cloudflare-kv-edge-cache',
          cachedAt: new Date().toISOString(),
          titles: cached
        });
      }
    } catch (e) {
      console.warn('KV read failed', e);
    }
  }

  if (!apiKey) {
    return c.json({
      source: 'offline-starter-feed',
      message: 'Connect a TMDB API Key to unlock unlimited live cloud sync via edge worker.',
      providers: Object.keys(TMDB_PROVIDERS),
      titles: []
    });
  }

  // Fetch live titles from TMDB across 5 platforms
  const titles = await fetchFromTmdb(apiKey, depth);

  // Store in KV cache for 24 hours (86,400s)
  if (c.env.STREAMMOOD_KV && titles.length > 0) {
    try {
      await c.env.STREAMMOOD_KV.put(cacheKey, JSON.stringify(titles), { expirationTtl: 86400 });
    } catch (e) {
      console.warn('KV write failed', e);
    }
  }

  return c.json({
    source: 'live-tmdb-edge-sync',
    count: titles.length,
    depthPages: depth,
    timestamp: new Date().toISOString(),
    titles
  });
});

// POST /api/sync (Trigger background sync)
app.post('/api/sync', async (c) => {
  const body = await c.req.json().catch(() => ({})) as any;
  const apiKey = body.apiKey || c.env.TMDB_API_KEY || '';
  const depth = body.depth || 3;

  if (!apiKey) {
    return c.json({ error: 'Missing TMDB API key' }, 400);
  }

  const titles = await fetchFromTmdb(apiKey, depth);

  if (c.env.STREAMMOOD_KV && titles.length > 0) {
    await c.env.STREAMMOOD_KV.put(`catalog_in_d${depth}`, JSON.stringify(titles), { expirationTtl: 86400 });
  }

  return c.json({
    status: 'synced',
    count: titles.length,
    timestamp: new Date().toISOString()
  });
});

// Search endpoint (Single title lookup)
app.get('/api/search', async (c) => {
  const q = c.req.query('q');
  const apiKey = c.req.query('api_key') || c.env.TMDB_API_KEY || '';

  if (!q) return c.json({ error: 'Missing search query ?q=' }, 400);
  if (!apiKey) return c.json({ error: 'Missing TMDB API key' }, 400);

  try {
    const searchUrl = `https://api.themoviedb.org/3/search/multi?api_key=${apiKey}&query=${encodeURIComponent(q)}&include_adult=false`;
    const res = await fetch(searchUrl);
    const data = await res.json() as any;
    return c.json(data);
  } catch (err) {
    return c.json({ error: 'Search failed', details: String(err) }, 500);
  }
});

// Export default worker with scheduled cron trigger
export default {
  fetch: app.fetch,
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    console.log('Automated Daily StreamMood Cron Trigger running...', event.cron);
    if (!env.TMDB_API_KEY) return;
    try {
      const titles = await fetchFromTmdb(env.TMDB_API_KEY, 5);
      if (env.STREAMMOOD_KV && titles.length > 0) {
        await env.STREAMMOOD_KV.put('catalog_in_d5', JSON.stringify(titles), { expirationTtl: 86400 });
        console.log(`Successfully refreshed catalog: ${titles.length} titles stored in edge KV.`);
      }
    } catch (err) {
      console.error('Scheduled cron refresh failed', err);
    }
  }
};
