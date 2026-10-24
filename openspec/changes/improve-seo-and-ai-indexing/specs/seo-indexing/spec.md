# Spec Delta

## Purpose

Ensure the Елена Бартош gestalt-therapy site is discoverable and correctly indexed by search engines and AI crawlers through a sitemap, robots directives, canonical URLs, social meta tags, and structured data.

## ADDED Requirements

### Requirement: Sitemap is published

The site SHALL generate and publish a `sitemap.xml` at the site root listing every public page.

#### Scenario: Sitemap contains all public pages
- **WHEN** the site is built with `hugo`
- **THEN** a `sitemap.xml` exists at the site root and lists every rendered page URL

### Requirement: Robots.txt declares sitemap and AI crawler rules

The site SHALL publish a `robots.txt` that references the sitemap and specifies access rules for AI crawlers.

#### Scenario: Robots.txt references the sitemap
- **WHEN** a crawler fetches `/robots.txt`
- **THEN** the response includes a `Sitemap:` directive pointing to `sitemap.xml`

#### Scenario: AI crawlers are addressed
- **WHEN** a crawler identifies as GPTBot, Google-Extended, or ClaudeBot
- **THEN** `robots.txt` contains an explicit rule for that user-agent

### Requirement: Canonical URL on every page

Each page SHALL include a `<link rel="canonical">` pointing to its absolute production URL.

#### Scenario: Canonical URL is present
- **WHEN** a page is rendered
- **THEN** the page `<head>` contains a canonical link with the page's absolute URL

### Requirement: Robots meta allows indexing

Public pages SHALL carry `meta name="robots" content="index, follow"` unless explicitly excluded.

#### Scenario: Robots meta permits indexing
- **WHEN** a public page is rendered
- **THEN** the page `<head>` contains `meta name="robots" content="index, follow"`

### Requirement: Open Graph tags on every page

Each page SHALL include Open Graph meta tags: `og:title`, `og:description`, `og:image`, `og:type`, `og:url`, `og:site_name`.

#### Scenario: Open Graph tags present
- **WHEN** a page is rendered
- **THEN** the page `<head>` contains `og:title`, `og:description`, `og:image`, `og:type`, `og:url`, and `og:site_name`

### Requirement: Twitter card tags on every page

Each page SHALL include Twitter card meta tags: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.

#### Scenario: Twitter card tags present
- **WHEN** a page is rendered
- **THEN** the page `<head>` contains Twitter card meta tags

### Requirement: JSON-LD structured data for the therapist

The site SHALL include JSON-LD structured data (Person / ProfessionalService) describing the therapist, services, and location.

#### Scenario: Structured data present
- **WHEN** a page is rendered
- **THEN** the page includes JSON-LD structured data for the therapist practice

### Requirement: Production baseURL supplied in CI

The production deploy SHALL pass `--baseURL https://gestalt.bartosh.org/` to `hugo`.

#### Scenario: Production baseURL is set
- **WHEN** the production GitHub Pages deploy runs
- **THEN** `hugo` is invoked with `--baseURL https://gestalt.bartosh.org/`
