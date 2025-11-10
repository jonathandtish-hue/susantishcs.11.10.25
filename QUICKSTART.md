# Quick Start Guide

Get up and running with the Website Content Scraper in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - for making HTTP requests
- `beautifulsoup4` - for parsing HTML

## Step 2: Test the Installation

```bash
python test_scraper.py
```

This runs a quick test to ensure everything is working correctly.

## Step 3: Run Your First Scrape

**Basic scrape (recommended for first run):**

```bash
python scrape_site.py https://your-website.com --max-depth 2
```

This will:
- Crawl up to 2 levels deep
- Create `site_content.json` and `site_content.md`
- Wait 1.5 seconds between requests (polite default)

## Step 4: Review the Output

Two files are created:

1. **`site_content.json`** - Machine-readable data:
   ```json
   [
     {
       "url": "https://your-site.com/",
       "title": "Home",
       "content": "Welcome to..."
     }
   ]
   ```

2. **`site_content.md`** - Human-readable Markdown:
   ```markdown
   ## Page 1: Home
   
   **URL:** https://your-site.com/
   
   **Content:**
   
   Welcome to...
   ```

## Common Use Cases

### For Website Redesign
```bash
# Crawl everything with summaries and individual files
python scrape_site.py https://your-site.com \
  --generate-summaries \
  --separate-files \
  --rate-limit 2.0
```

Output:
- `site_content.json` - All data
- `site_content.md` - Combined markdown
- `site_content_pages/` - Individual page files

### For Quick Content Audit
```bash
# Fast crawl, JSON only
python scrape_site.py https://your-site.com \
  --max-depth 3 \
  --json-only \
  --rate-limit 1.0
```

### For Large Sites
```bash
# Slower, more polite crawling
python scrape_site.py https://your-site.com \
  --rate-limit 3.0 \
  --timeout 20 \
  --max-depth 5
```

## Tips

1. **Start small**: Use `--max-depth 2` for your first run
2. **Be polite**: Increase `--rate-limit` for busy sites
3. **Test first**: Try one page before crawling everything
4. **Check output**: Review a few pages to ensure quality
5. **Handle interrupts**: Press Ctrl+C to stop (partial results will be saved)

## Troubleshooting

**Problem: "No pages were scraped"**
- Check the URL is accessible in a browser
- Try increasing `--timeout 20`

**Problem: "Too slow"**
- Reduce `--max-depth`
- Check your internet connection
- The site might have rate limiting

**Problem: "Content looks messy"**
- The site has complex navigation - this is common
- Review the output and adjust as needed
- Some cleanup may be needed manually

## Next Steps

1. Read the full [README.md](README.md) for all options
2. Check [example_usage.py](example_usage.py) for programmatic use
3. Modify the scraper for your specific needs

## Getting Help

1. Run with `--help` to see all options:
   ```bash
   python scrape_site.py --help
   ```

2. Run tests to verify installation:
   ```bash
   python test_scraper.py
   ```

3. Check that you have permission to scrape the site!

---

**Ready to go?** Run this command with your website:

```bash
python scrape_site.py https://your-mothers-website.com \
  --generate-summaries \
  --separate-files \
  --rate-limit 2.0 \
  --output mothers_website
```

This creates:
- `mothers_website.json`
- `mothers_website.md`
- `mothers_website_pages/` directory with individual files

Perfect for redesign projects! 🎨


