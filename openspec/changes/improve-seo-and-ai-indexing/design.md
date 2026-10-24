# Design

## Context

The site is a Hugo static site (v0.155.2) for gestalt therapist Елена Бартош. `hugo.toml` currently disables sitemap generation (`disableKinds` includes `"sitemap"`), emits a minimal `robots.txt` (`User-agent: *` only), and `layouts/partials/head.html` provides only basic meta tags (charset, viewport, title, description, favicon, CSS). `baseURL` is `https://test.bartosh.org/` locally; production `baseURL` is supplied via `--baseURL` in CI for GitHub Pages at `gestalt.bartosh.org`. The `public/` directory is gitignored. See `proposal.md` for motivation and `specs/seo-indexing/spec.md` for requirements.

## Goals / Non-Goals

**Goals:**
- Publish a `sitemap.xml` listing all public pages.
- Publish a `robots.txt` with a `Sitemap:` directive and explicit rules for AI crawlers (GPTBot, Google-Extended, ClaudeBot).
- Add canonical URL, robots meta, Open Graph, and Twitter card tags to every page's `<head>`.
- Add JSON-LD structured data (Person / ProfessionalService) for the therapist practice.
- Keep production `baseURL` out of `hugo.toml` (supplied via CI `--baseURL`).

**Non-Goals:**
- Submitting the sitemap to Google Search Console / Yandex Webmaster (operational, after deploy).
- Keyword research or content changes.
- `hreflang` / multi-language support (site is Russian-only).

## Decisions

**D1: Re-enable sitemap in `hugo.toml`** — remove `"sitemap"` from `disableKinds`.
- Rationale: sitemap is the primary discovery mechanism for search engines; Hugo generates it automatically once enabled.
- Alternative considered: hand-write a static `sitemap.xml` — rejected, harder to keep in sync as pages are added.

**D2: Customize `robots.txt` via `static/robots.txt`** — rather than relying only on Hugo's generated minimal file.
- Rationale: Hugo's `enableRobotsTXT` emits only `User-agent: *`. A static file lets us add `Sitemap:` and AI crawler rules deterministically.
- Alternative considered: Hugo `robotsTXT` custom output format — rejected, more complex for a static site.

**D3: Add SEO meta tags in `layouts/partials/head.html`** — canonical, robots, Open Graph, Twitter.
- Rationale: `head.html` is included on every page, so one edit covers all page types and sections.
- Alternative considered: per-section partials — rejected, unnecessary duplication.

**D4: JSON-LD structured data as a partial included in `head.html`** — Person / ProfessionalService for the therapist, services, and location (Espoo / Helsinki, Finland).
- Rationale: helps search engines and AI understand the practice; one partial reused site-wide.

**D5: Keep `baseURL` as the test value in `hugo.toml`; pass production via CI `--baseURL`** — per the existing project plan.
- Rationale: avoids baking the production domain into the repo; CI controls the published URL.
- Canonical URLs will use `.Site.BaseURL`, so they follow whatever `baseURL` the build uses.

## Risks / Trade-offs

- [Risk] `static/robots.txt` may conflict with Hugo's auto-generated `robots.txt` if both are present → Mitigation: verify which file wins in `public/` after a local `hugo` build, then keep a single consistent source.
- [Risk] Local dev uses `test.bartosh.org` while production is `gestalt.bartosh.org` → Mitigation: canonical uses `.Site.BaseURL`, so it follows the build's baseURL; CI passes the production value.
- [Trade-off] Open Graph `og:image` needs a suitable image; using `banner.jpg` for all pages is acceptable but less specific per-page → Mitigation: use `banner.jpg` as the default site image.

## Migration Plan

- Apply changes to `hugo.toml`, `static/`, and `layouts/partials/head.html`.
- Build locally with `hugo` and verify `public/sitemap.xml`, `public/robots.txt`, and a sample page's `<head>`.
- Deploy via GitHub Pages with `--baseURL https://gestalt.bartosh.org/`; confirm `robots.txt` and `sitemap.xml` are served at the production domain.
- (Post-deploy, operational) submit the sitemap to Google Search Console and Yandex Webmaster.

## Open Questions

- None blocking.
