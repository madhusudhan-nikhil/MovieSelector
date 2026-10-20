# StreamMood India — Serverless Edge Worker (Cloudflare Workers + Hono.js)

A non-Python, 100% TypeScript serverless edge microservice for StreamMood India. Runs on Cloudflare's global edge network across 300+ cities with sub-15ms response times.

---

## Features
- **Zero Python Runtime:** 100% modern TypeScript / Web Standards (`fetch`, `Request`, `Response`).
- **Zero Servers to Manage:** Automatically scales from 0 to millions of requests with a permanent free tier (100,000 requests/day).
- **Global Edge Caching:** Caches Indian OTT titles across Netflix, Prime Video, JioHotstar, SonyLIV, and Zee5 in Cloudflare KV.
- **Automated Daily Cron Refresh:** Runs automatically every night at 03:00 AM IST (21:30 UTC) to pull new releases into the edge cache.
- **Native CORS:** Built-in Hono CORS middleware allowing direct calls from browser frontends (`file:///` or `https://...`).

---

## Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and endpoint overview |
| `GET` | `/api/health` | Healthcheck and timestamp |
| `GET` | `/api/providers` | India OTT streaming providers and IDs |
| `GET` | `/api/catalog?depth=3&api_key=...` | Returns cached/live streaming catalog |
| `POST` | `/api/sync` | Trigger on-demand deep background sync |
| `GET` | `/api/search?q=Mirzapur&api_key=...` | Live multi-search for Indian titles |

---

## Quickstart

### 1. Install Dependencies
```bash
cd worker
npm install
```

### 2. Run Locally in Development Mode
```bash
npm run dev
# Starts local edge simulation at http://localhost:8787
```

### 3. Deploy to Cloudflare (Free)
```bash
npx wrangler login
npm run deploy
```
Your worker will be live immediately at:
`https://streammood-edge.<your-subdomain>.workers.dev`

---

## Connecting to StreamMood Frontend
In [index.html](file:///c:/Users/Nikhil/Documents/antigravity/hopeful-davinci/index.html):
1. Open the **Settings & Library Management** tab.
2. In the **Live Cloud Pull** drawer, enter your worker's URL:
   `https://streammood-edge.<your-subdomain>.workers.dev`
3. Click **"Refresh & Pull All Titles"** to ingest live streaming titles directly from your edge backend!
