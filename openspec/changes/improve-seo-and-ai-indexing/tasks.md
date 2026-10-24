# Tasks

## 1. Sitemap and robots.txt

- [x] 1.1 Remove `"sitemap"` from `disableKinds` in `hugo.toml` and verify `hugo` build emits `public/sitemap.xml`
- [x] 1.2 Add `static/robots.txt` with a `Sitemap:` directive and explicit rules for AI crawlers (GPTBot, Google-Extended, ClaudeBot), and verify it is copied to `public/robots.txt` on build
- [x] 1.3 Confirm `public/robots.txt` and `public/sitemap.xml` exist and are accessible after a local `hugo` build

## 2. Page-level SEO meta tags

- [x] 2.1 Add canonical `<link rel="canonical">`, `meta name="robots" content="index, follow"`, Open Graph tags (`og:title`, `og:description`, `og:image`, `og:type`, `og:url`, `og:site_name`), and Twitter card tags to `layouts/partials/head.html`
- [x] 2.2 Build the site and verify a rendered page's `<head>` contains the canonical URL, robots meta, Open Graph, and Twitter card tags

## 3. JSON-LD structured data

- [x] 3.1 Create a JSON-LD partial (Person / ProfessionalService) describing the therapist practice, services, and location (Espoo / Helsinki, Finland)
- [x] 3.2 Include the structured-data partial in `layouts/partials/head.html` and verify it renders on pages

## 4. Production baseURL and final verification

- [x] 4.1 Confirm `hugo.toml` keeps `baseURL` as the local/test value and that production baseURL is supplied via CI `--baseURL https://gestalt.bartosh.org/`
- [x] 4.2 Run `hugo server --disableFastRender` locally and verify SEO output (sitemap, robots, meta tags, structured data) on multiple page types

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
- Verify the archived result.
