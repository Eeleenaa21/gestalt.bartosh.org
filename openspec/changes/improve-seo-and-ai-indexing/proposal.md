# Proposal

## Why

The gestalt-therapist site (Елена Бартош) is not effectively discoverable by search engines or AI crawlers. Hugo emits only a minimal `robots.txt` (`User-agent: *`), sitemap generation is disabled in `hugo.toml`, and page `<head>` sections lack canonical URLs, robots directives, and Open Graph / social meta tags. Search engines and AI systems therefore cannot efficiently discover the site's pages or understand its content, which limits visibility for Russian-speaking clients seeking therapy in Finland or online.

## What Changes

- Re-enable sitemap generation by removing `"sitemap"` from `disableKinds` in `hugo.toml`, so search engines can discover all pages and sections.
- Keep `enableRobotsTXT = true` and enrich robots output with a `Sitemap:` directive plus rules for AI crawlers (e.g., GPTBot, Google-Extended, ClaudeBot).
- Add SEO `<head>` meta tags in `layouts/partials/head.html`: canonical URL, `meta name="robots"`, Open Graph tags (`og:title`, `og:description`, `og:image`, `og:type`, `og:url`, `og:site_name`), and Twitter card tags.
- Add JSON-LD structured data (Person / ProfessionalService) for the therapist so search engines and AI can understand the practice, services, and location.
- Leave `baseURL` in `hugo.toml` as the local/test value; production `baseURL` continues to be supplied via `--baseURL` in CI for GitHub Pages at `gestalt.bartosh.org`.

## Capabilities

### New Capabilities

- `seo-indexing`: Site discoverability and indexing behavior — sitemap generation, robots.txt (including AI crawler rules), canonical URLs, robots meta, Open Graph/Twitter cards, and JSON-LD structured data for search engines and AI crawlers.

### Modified Capabilities

- (none — no existing specs in the project)

## Impact

- `hugo.toml` (`disableKinds`, robots/sitemap settings)
- `layouts/partials/head.html` (SEO meta tags)
- Possible `static/robots.txt` or layout additions for structured data
- Deploy: production `baseURL` via CI `--baseURL` flag unchanged
