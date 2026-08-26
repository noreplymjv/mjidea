// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Cloudflare / local: default. GitHub Pages project site: ASTRO_BASE=/mjidea/ ASTRO_SITE=https://noreplymjv.github.io
const SITE = process.env.ASTRO_SITE || 'https://mjidea.pages.dev';
const BASE = process.env.ASTRO_BASE || '/';

export default defineConfig({
  site: SITE,
  base: BASE,
  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: 'github-dark' },
  },
});
