# Hosting — Mjidea

## Winner: Cloudflare Pages (GitHub-connected)

Same pattern as GetMeBack: push to GitHub → Cloudflare builds and hosts.

| Need | Cloudflare Pages |
|------|------------------|
| Cost | Free tier is enough to start |
| SEO | Global CDN, HTTP/3, great TTFB |
| Custom domain | Easy |
| Analytics | Cloudflare Web Analytics (privacy-friendly) |
| Auto deploy | On every push to `main` |

**Repo:** https://github.com/noreplymjv/mjidea  
**Expected URL:** https://mjidea.pages.dev  

### Do this once

Read and follow the click steps: **`CLOUDFLARE_HOSTING.md`**

Build settings (Root = `site`):

- Build command: `npm run build`
- Output directory: `dist`
- Node: `22`

### Local preview / manual deploy

```bash
cd site
ASTRO_TELEMETRY_DISABLED=1 npm run build
# optional direct upload (needs wrangler login):
npx wrangler pages deploy dist --project-name=mjidea
```

## Cookies / analytics stance

Privacy-first. See `seo/PRIVACY-AND-COOKIES.md`. No ad-tech until Growth + CEO approve.

## Runner-ups

Vercel · Netlify · Ghost Pro. Avoid WordPress for this stack.
