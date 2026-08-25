# Cloudflare — fix the failed mjidea build (Workers + GitHub)

Repo: https://github.com/noreplymjv/mjidea  
Service: https://dash.cloudflare.com/85c151e7892b963ba71b833d338d0bb7/workers/services/view/mjidea  
Live URL after success: **https://mjidea.pages.dev** (or the `*.workers.dev` URL Cloudflare shows)

## What went wrong

Build settings were:

| Setting | Was | Problem |
|---------|-----|---------|
| Build command | None | Astro never ran → no HTML |
| Deploy command | `npx wrangler deploy` | Looked for static files that did not exist |
| Root directory | `/` | OK if build writes `site/dist` |

Error: *Could not detect a directory containing static files*

## Fix (2 minutes) — change Build settings

Open:  
https://dash.cloudflare.com/85c151e7892b963ba71b833d338d0bb7/workers/services/view/mjidea  

→ **Settings** → **Build** / **Build configuration**

Set exactly:

| Box | Type this |
|-----|-----------|
| **Root directory** | `/` (leave as root) |
| **Build command** | `cd site && npm ci && ASTRO_TELEMETRY_DISABLED=1 npm run build` |
| **Deploy command** | `npx wrangler deploy` |

**Build variables / Environment variables** (add if there is a Variables section):

| Name | Value |
|------|--------|
| `NODE_VERSION` | `22` |

Save → **Deployments** → **Retry deployment** / **Create deployment**

The repo now has a root `wrangler.toml` that tells Wrangler to publish `./site/dist` as static assets.

## How you know it worked

- Build log shows `astro build` and hundreds of pages
- Then wrangler uploads assets (not the “no static files” error)
- Open https://mjidea.pages.dev or the Visit link on the deployment

## Still broken?

Paste the new build log (last 40 lines).
