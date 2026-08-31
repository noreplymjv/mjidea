# Cloudflare — GitHub-connected Workers (Mjidea)

Repo: https://github.com/noreplymjv/mjidea  
Dashboard: https://dash.cloudflare.com/85c151e7892b963ba71b833d338d0bb7/workers/services/view/mjidea2/production/settings#builds  
Live: **https://mjidea2.pages.dev** or **https://mjidea2.workers.dev** (or the Visit URL on the Cloudflare deployment)

## Why the last build failed

`npx wrangler deploy` ran with **no Astro build**, so there were no HTML files.

## What is fixed in git

- Root `wrangler.toml` publishes **`./cf-dist`** (prebuilt static site, same idea as GetMeBack’s `cf-dist`)
- **Retry deployment** with current dashboard settings (Build command None, Deploy `npx wrangler deploy`, Root `/`)

After this repo is on `main`, click **Retry** on the failed build.

## Optional: build on Cloudflare (faster later)

If you add a build command:

```
cd site && npm ci && ASTRO_TELEMETRY_DISABLED=1 npm run build && rm -rf ../cf-dist && cp -a dist ../cf-dist
```

Variable: `NODE_VERSION` = `22`

## Refresh cf-dist locally after content changes

```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"  # Mjidea repo root
npm run build
git add cf-dist && git commit -m "Refresh Cloudflare static build" && git push
```
