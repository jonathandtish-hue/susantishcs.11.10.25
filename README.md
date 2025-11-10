# Website Content Scraper

A comprehensive, ethical web scraping tool designed for extracting and cleaning content from websites for redesign and content analysis projects.

## Features

✨ **Comprehensive Crawling**
- Automatically discovers and follows all internal links within a domain
- Handles redirects, broken links, and edge cases gracefully
- Configurable crawl depth and rate limiting

🧹 **Intelligent Content Cleaning**
- Removes navigation bars, headers, footers, and sidebars
- Filters out script tags, style elements, and other non-content elements
- Detects and removes repeated navigation/menu text
- Preserves meaningful content: headings, paragraphs, lists, and quotes

📄 **Multiple Output Formats**
- **JSON**: Structured data with metadata for programmatic use
- **Markdown**: Human-readable format with preserved formatting
- **Individual files**: Option to save each page as a separate markdown file

🤖 **Smart Features**
- Optional automatic summarization of each page
- Extraction of heading structure (h1-h3)
- Prioritizes `<main>` and `<article>` content areas
- Markdown-style formatting preserved in output

⚡ **Polite & Ethical**
- Configurable rate limiting (default: 1.5 seconds between requests)
- Respectful User-Agent identification
- Only scrapes pages you have permission to access
- Handles timeouts and errors gracefully

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Make the script executable (optional):**

```bash
chmod +x scrape_site.py
```

## Usage

### Basic Usage

Scrape a website starting from its homepage:

```bash
python scrape_site.py https://example.com
```

This will create two files:
- `site_content.json` - All content in JSON format
- `site_content.md` - All content in a combined Markdown file

### Advanced Options

**Control crawling speed and depth:**

```bash
# Slower crawling (2 seconds between requests)
python scrape_site.py https://example.com --rate-limit 2.0

# Limit crawl depth to 3 levels
python scrape_site.py https://example.com --max-depth 3

# Both
python scrape_site.py https://example.com --rate-limit 2.0 --max-depth 3
```

**Generate summaries for each page:**

```bash
python scrape_site.py https://example.com --generate-summaries
```

**Save each page as a separate file:**

```bash
python scrape_site.py https://example.com --separate-files
```

This creates a directory `site_content_pages/` with individual markdown files for each page.

**Custom output filenames:**

```bash
python scrape_site.py https://example.com --output my_website
```

Creates `my_website.json` and `my_website.md`

**JSON only (skip markdown):**

```bash
python scrape_site.py https://example.com --json-only
```

**Include URL query parameters:**

```bash
# By default, URLs like /page?id=1 and /page?id=2 are treated as the same
# Use this flag to treat them as different pages
python scrape_site.py https://example.com --include-query-params
```

**Adjust timeout:**

```bash
python scrape_site.py https://example.com --timeout 15
```

### Complete Example

```bash
python scrape_site.py https://my-mothers-website.com \
  --rate-limit 2.0 \
  --max-depth 5 \
  --generate-summaries \
  --separate-files \
  --output mothers_site
```

This will:
- Crawl with a 2-second delay between requests
- Go up to 5 levels deep
- Generate automatic summaries for each page
- Create individual markdown files for each page
- Save everything with the prefix "mothers_site"

## Output Format

### JSON Structure

```json
[
  {
    "url": "https://example.com/",
    "title": "Home - Example Site",
    "content": "Welcome to our healing practice...",
    "summary": "This page introduces the healing practice and its philosophy.",
    "headings": [
      {"level": 1, "text": "Welcome"},
      {"level": 2, "text": "Our Approach"}
    ],
    "status_code": 200
  },
  {
    "url": "https://example.com/about",
    "title": "About Us",
    "content": "Our practice was founded in...",
    "summary": "Information about the practice's history and practitioners.",
    "headings": [
      {"level": 1, "text": "About Our Practice"}
    ],
    "status_code": 200
  }
]
```

### Markdown Structure

The markdown output includes:
- Header with source URL, page count, and timestamp
- Each page as a section with:
  - Page number and title
  - URL
  - Optional summary (if `--generate-summaries` used)
  - Heading structure
  - Clean content with markdown formatting

## Content Cleaning Details

The scraper intelligently cleans content by:

1. **Removing HTML elements:**
   - `<script>`, `<style>`, `<meta>`, `<link>`, `<noscript>`
   - `<header>`, `<footer>`, `<nav>`, `<aside>`
   - `<iframe>`, `<embed>`, `<object>`

2. **Removing by class/id patterns:**
   - Elements with "nav", "menu", "sidebar" in class or id
   - Elements with "header", "footer", "breadcrumb" in class or id
   - Elements with "pagination", "social", "widget" in class or id

3. **Prioritizing main content:**
   - Looks for `<main>`, `<article>`, or `[role="main"]` first
   - Falls back to `<body>` if no semantic content area found

4. **Preserving structure:**
   - Headings are preserved with markdown formatting
   - Lists are converted to bullet points
   - Blockquotes are preserved
   - Paragraphs maintain natural reading flow

5. **Deduplication:**
   - Removes consecutive duplicate lines
   - Filters out very short snippets (< 10 characters)
   - Normalizes excessive whitespace

## Command-Line Reference

```
usage: scrape_site.py [-h] [--rate-limit RATE_LIMIT] [--max-depth MAX_DEPTH]
                      [--include-query-params] [--timeout TIMEOUT]
                      [--output OUTPUT] [--json-only] [--generate-summaries]
                      [--separate-files]
                      url

positional arguments:
  url                   Base URL to start crawling from

optional arguments:
  -h, --help            show this help message and exit
  --rate-limit RATE_LIMIT
                        Seconds to wait between requests (default: 1.5)
  --max-depth MAX_DEPTH
                        Maximum crawl depth (default: unlimited)
  --include-query-params
                        Treat URLs with different query parameters as unique pages
  --timeout TIMEOUT     Request timeout in seconds (default: 10)
  --output OUTPUT       Output filename prefix (default: site_content)
  --json-only           Only output JSON file (skip Markdown)
  --generate-summaries  Generate automatic summaries for each page
  --separate-files      Save each page as a separate Markdown file
```

## Use Cases

This tool is perfect for:

- 🎨 **Website Redesign Projects**: Extract all content from an existing site to migrate to a new design
- 📝 **Content Audits**: Review and analyze all content across a website
- 🔄 **Content Migration**: Move content from one CMS to another
- 📊 **Content Analysis**: Analyze content structure and organization
- 📚 **Documentation**: Create offline documentation from web content
- 🔍 **SEO Analysis**: Review content quality and structure across pages

## Ethical Use

This tool is designed for ethical use only:

- ✅ **Do** use it on websites you own or have permission to scrape
- ✅ **Do** respect robots.txt and rate limits
- ✅ **Do** use appropriate rate limiting (default is already conservative)
- ❌ **Don't** use it to scrape websites without permission
- ❌ **Don't** use it for competitive intelligence without permission
- ❌ **Don't** overwhelm servers with aggressive scraping

## Error Handling

The scraper handles various errors gracefully:

- **Timeouts**: Noted in output, page skipped
- **HTTP Errors** (404, 500, etc.): Logged with status code, page skipped
- **Network Errors**: Logged and page skipped
- **Keyboard Interrupt** (Ctrl+C): Saves partial results before exiting

## Tips & Best Practices

1. **Start with a test run**: Try with `--max-depth 2` first to see the structure
2. **Check robots.txt**: Ensure you're allowed to scrape the site
3. **Use appropriate rate limiting**: Increase `--rate-limit` for slower servers
4. **Review the output**: Check a few pages to ensure content quality is good
5. **Incremental crawling**: For large sites, use `--max-depth` to crawl in stages
6. **Summaries are extractive**: The summary feature takes the first 2 sentences; review them for quality

## Requirements

- Python 3.7+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0

## License

This tool is provided for ethical use in web redesign and content analysis projects. Use responsibly and only on sites you have permission to access.

## Support

For issues or questions:
1. Check that the website is accessible (try in a browser)
2. Try increasing `--timeout` for slow sites
3. Try increasing `--rate-limit` if getting blocked
4. Ensure you have the latest dependencies installed

## Contributing

Suggestions for improvements are welcome! Some ideas for future enhancements:
- Support for authentication (login-protected pages)
- Robots.txt compliance checking
- Sitemap.xml parsing for discovery
- Export to additional formats (CSV, HTML)
- Language detection and translation
- Image downloading and cataloging


