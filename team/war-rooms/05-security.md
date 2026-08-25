# Security War Room (≥5)

Members: Vera Knox, Omar Siddiq, Paige Quinn, Leon Hart, Nina Brooks (+ Chris Vale).

## Mission

Keep the site trustworthy: no XSS gifts, no secret leaks, honest cookies, sane headers.

## Checklist → `<slug>.security.md`

### Per-post
- [ ] No untrusted HTML/scripts in markdown
- [ ] External links use safe patterns
- [ ] No PII leaked from CEO idea
- [ ] Claims that could be defamatory flagged to PM

### Site-level (periodic)
- [ ] Dependencies audited (`npm audit`)
- [ ] No secrets in repo
- [ ] CSP / security headers plan for Cloudflare
- [ ] Analytics cookies: document in privacy note; prefer privacy-friendly (Cloudflare Web Analytics / Plausible)
- [ ] Forms (if any): rate limit, honeypot later

## Cookies note for hosting

If CEO said “use cookies from hosting”: prefer **first-party / privacy-first analytics** from Cloudflare Pages, document in `seo/PRIVACY-AND-COOKIES.md`. Do not install invasive ad trackers by default.
