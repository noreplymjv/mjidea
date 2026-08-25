# Cloudflare Pages — GitHub connect (like GetMeBack)

Mjidea is already on GitHub: **https://github.com/noreplymjv/mjidea**  
Cloudflare account (same as GetMeBack): `85c151e7892b963ba71b833d338d0bb7`

## Preferred: Connect GitHub in the dashboard (5 minutes)

1. Open Cloudflare Workers & Pages for your account:  
   https://dash.cloudflare.com/85c151e7892b963ba71b833d338d0bb7/workers-and-pages

2. Click **Create** → **Pages** → **Connect to Git**

3. Authorize / pick GitHub account **noreplymjv** → select repo **mjidea**

4. Set build exactly like this:

   | Setting | Value |
   |---------|--------|
   | Production branch | `main` |
   | Root directory | `site` |
   | Framework preset | **Astro** (or None) |
   | Build command | `npm run build` |
   | Build output directory | `dist` |
   | Node version (Environment variables) | `NODE_VERSION` = `22` |

5. Click **Save and Deploy**

6. Wait for **Success**. Visit the URL Cloudflare shows — usually:  
   **https://mjidea.pages.dev**

### After first success

- Every push to `main` auto-redeploys
- Optional: **Custom domains** → add your domain
- Optional: **Analytics** → Cloudflare Web Analytics (privacy-first; see `seo/PRIVACY-AND-COOKIES.md`)

---

## Alternate: GitHub Actions deploy (no dashboard Git connect)

Same pattern as GetMeBack’s `deploy-cloudflare-pages.yml`.

1. Cloudflare → **My Profile** → **API Tokens** → Create Token  
   Use template **Edit Cloudflare Workers** (includes Pages) or custom with Account → Cloudflare Pages → Edit
2. Copy **Account ID** from the right sidebar of any Workers/Pages page  
   (yours: `85c151e7892b963ba71b833d338d0bb7`)
3. GitHub repo → **Settings** → **Secrets and variables** → **Actions** → add:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
4. Workflow template is at `pipeline/deploy-cloudflare-pages.yml.pending`  
   Copy it to `.github/workflows/deploy-cloudflare-pages.yml` after `gh auth refresh -s workflow` (or paste via GitHub UI).
5. Push to `main` or run **Actions** → **Deploy Cloudflare Pages** → **Run workflow**

Create the Pages project once if needed:

```bash
cd "/media/mj/My Passport/mjI/Mjidea/site"
npx wrangler login
npx wrangler pages project create mjidea --production-branch main
```

---

## How you know it worked

- Build log shows Astro finishing **~500+ pages**
- https://mjidea.pages.dev opens with **Mjidea** hero
- `/ideas/` lists essays and search works

## Still broken?

Paste the last 40 lines of the Cloudflare build log (or GitHub Actions log) and we’ll fix it.
