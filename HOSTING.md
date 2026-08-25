# Hosting — Mjidea

## Winner: Cloudflare Pages

Best fit for a philosophy/ideas blog you want **fast, findable, cheap, portable**.

| Need | Cloudflare Pages |
|------|------------------|
| Cost | Free tier is enough to start |
| SEO | Global CDN, HTTP/3, great TTFB |
| Custom domain | Easy |
| Analytics cookies | Cloudflare Web Analytics (privacy-friendly, light cookies) |
| Deploy from this folder | `npx wrangler pages deploy site/dist` |
| Security headers | Configurable at edge |

### Runner-ups

- **Vercel** — excellent DX; also fine
- **Netlify** — fine; forms easy
- **Ghost Pro** — if you want hosted CMS UI (less portable)
- **WordPress** — avoid unless you need a plugin zoo

## Cookies / analytics stance

Security team default: **privacy-first**. Use Cloudflare Web Analytics or Plausible. Document in `seo/PRIVACY-AND-COOKIES.md`. No ad-tech pile-on until Growth + CEO explicitly approve.

## Deploy steps (first time)

1. Create free Cloudflare account
2. `cd site && npm run build`
3. Pages → Create → Upload `dist/` OR connect git later
4. Add custom domain when ready
5. Optional: set `AUTO_DEPLOY=1` in your shell profile once PM trusts the pipeline

## Why not “biggest host”

Big shared hosting (cPanel PHP) fights this portable Astro setup. You want static + edge.
