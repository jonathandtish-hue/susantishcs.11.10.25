#!/usr/bin/env python3
"""
Professional Web Crawler for Site Content Extraction
Ethically scrapes all pages from a website for analysis and redesign purposes.
"""

import argparse
import json
import re
import time
from collections import deque
from typing import Dict, List, Set
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


class WebsiteCrawler:
    """
    A polite web crawler that recursively discovers and extracts content
    from all pages within a given domain.
    """
    
    def __init__(
        self,
        base_url: str,
        rate_limit: float = 1.5,
        max_depth: int = None,
        include_query_params: bool = False,
        timeout: int = 10,
        generate_summaries: bool = False
    ):
        """
        Initialize the crawler.
        
        Args:
            base_url: Starting URL to crawl
            rate_limit: Seconds to wait between requests (default: 1.5)
            max_depth: Maximum crawl depth (None for unlimited)
            include_query_params: Whether to treat URLs with different query params as unique
            timeout: Request timeout in seconds
            generate_summaries: Whether to generate automatic summaries for each page
        """
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.max_depth = max_depth
        self.include_query_params = include_query_params
        self.timeout = timeout
        self.generate_summaries = generate_summaries
        
        # Parse base URL to get domain
        parsed = urlparse(base_url)
        self.domain = parsed.netloc
        self.scheme = parsed.scheme
        
        # Track visited URLs and queue for BFS
        self.visited_urls: Set[str] = set()
        self.queue = deque([(base_url, 0)])  # (url, depth)
        self.pages_data: List[Dict] = []
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebsiteCrawler/1.0; +ethical-scraping)'
        })
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize URL by removing fragments and optionally query parameters.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL string
        """
        parsed = urlparse(url)
        
        # Remove fragment
        if not self.include_query_params:
            # Remove query params too
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                '',  # params
                '',  # query
                ''   # fragment
            ))
        else:
            normalized = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                ''  # fragment
            ))
        
        # Remove trailing slash for consistency (except for root)
        if normalized.endswith('/') and len(parsed.path) > 1:
            normalized = normalized[:-1]
            
        return normalized
    
    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and belongs to the same domain.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL should be crawled
        """
        try:
            parsed = urlparse(url)
            
            # Must have same domain
            if parsed.netloc != self.domain:
                return False
            
            # Must be http or https
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Skip common non-HTML file extensions
            skip_extensions = [
                '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
                '.zip', '.tar', '.gz', '.mp4', '.mp3', '.avi', '.mov',
                '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.css', '.js', '.xml', '.json', '.csv'
            ]
            
            path_lower = parsed.path.lower()
            if any(path_lower.endswith(ext) for ext in skip_extensions):
                return False
            
            return True
            
        except Exception:
            return False
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """
        Extract all internal links from a page.
        
        Args:
            soup: BeautifulSoup object of the page
            current_url: Current page URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        links = []
        
        for anchor in soup.find_all('a', href=True):
            href = anchor.get('href', '').strip()
            
            if not href or href.startswith('#'):
                continue
            
            # Convert to absolute URL
            absolute_url = urljoin(current_url, href)
            
            # Normalize and validate
            normalized = self.normalize_url(absolute_url)
            
            if self.is_valid_url(normalized):
                links.append(normalized)
        
        return links
    
    def extract_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract clean text content from a page, removing navigation and repeated elements.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Dictionary with 'raw' and 'clean' content versions
        """
        # Create a copy to preserve original
        content_soup = BeautifulSoup(str(soup), 'html.parser')
        
        # Remove unwanted elements
        unwanted_tags = [
            'script', 'style', 'meta', 'link', 'noscript',
            'header', 'footer', 'nav', 'aside',
            'iframe', 'embed', 'object'
        ]
        for tag in unwanted_tags:
            for element in content_soup.find_all(tag):
                element.decompose()
        
        # Remove elements with common navigation/menu classes and IDs
        # Use word boundaries to avoid false positives (e.g., "with-sidebar" is not "sidebar")
        navigation_patterns = [
            r'\bnav\b', r'\bmenu\b', r'\bsidebar\b', r'\bheader\b', r'\bfooter\b',
            r'\bbreadcrumb', r'\bpagination\b', r'\bsocial\b', r'\bwidget\b'
        ]
        
        for element in content_soup.find_all(True):
            # Skip if not a tag element (e.g., NavigableString)
            if not hasattr(element, 'attrs') or element.attrs is None:
                continue
            
            # Check class and id attributes
            classes = element.get('class', [])
            elem_id = element.get('id', '')
            
            # Convert to strings for pattern matching
            class_str = ' '.join(classes).lower() if classes else ''
            id_str = elem_id.lower() if elem_id else ''
            
            # Remove if matches navigation patterns (with word boundaries)
            import re as regex_module
            combined_str = f"{class_str} {id_str}"
            if any(regex_module.search(pattern, combined_str) for pattern in navigation_patterns):
                # Don't remove if it's a wrapper (contains "-wrapper" or "with-")
                if 'wrapper' not in combined_str and 'with-' not in combined_str:
                    element.decompose()
        
        # Extract main content - prioritize main content areas
        main_content = None
        for tag in ['main', 'article', '[role="main"]']:
            main_content = content_soup.find(tag)
            if main_content:
                break
        
        # If no main content area found, use body or the whole soup
        if not main_content:
            main_content = content_soup.find('body') or content_soup
        
        # Extract structured text with preserved formatting
        clean_parts = []
        
        # Extract headings and paragraphs in order
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'blockquote', 'div']):
            text = element.get_text(separator=' ', strip=True)
            # Skip if element is just a container with other block elements
            if element.name == 'div' and element.find(['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                continue
            if text and len(text) > 15:  # Filter out very short snippets
                # Add markdown-style formatting
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(element.name[1])
                    clean_parts.append(f"{'#' * level} {text}")
                elif element.name in ['ul', 'ol']:
                    # Extract list items
                    for li in element.find_all('li', recursive=False):
                        li_text = li.get_text(separator=' ', strip=True)
                        if li_text:
                            clean_parts.append(f"• {li_text}")
                elif element.name == 'blockquote':
                    clean_parts.append(f"> {text}")
                else:
                    clean_parts.append(text)
        
        # Join and clean up
        clean_text = '\n\n'.join(clean_parts)
        
        # Remove duplicate consecutive lines (common in nav/footer remnants)
        lines = clean_text.split('\n')
        deduplicated_lines = []
        prev_line = None
        
        for line in lines:
            line = line.strip()
            if line and line != prev_line:
                deduplicated_lines.append(line)
                prev_line = line
        
        clean_text = '\n'.join(deduplicated_lines)
        
        # Normalize excessive whitespace
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
        clean_text = re.sub(r'[ \t]+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        # Also extract raw text (simpler version for fallback)
        raw_text = main_content.get_text(separator=' ', strip=True)
        raw_text = re.sub(r'\s+', ' ', raw_text).strip()
        
        return {
            'clean': clean_text,
            'raw': raw_text
        }
    
    def generate_summary(self, content: str, max_sentences: int = 2) -> str:
        """
        Generate a simple extractive summary from content.
        
        Args:
            content: Text content to summarize
            max_sentences: Maximum number of sentences to include
            
        Returns:
            Summary string
        """
        if not content:
            return ""
        
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+\s+', content)
        
        # Filter out very short sentences and clean
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            # Fallback: take first 150 characters
            return content[:150].strip() + "..."
        
        # Take the first N meaningful sentences
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences)
        
        # Ensure it ends with proper punctuation
        if summary and summary[-1] not in '.!?':
            summary += '.'
        
        return summary
    
    def scrape_page(self, url: str) -> Dict:
        """
        Scrape a single page and extract content.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with page data or None if error
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Check if content type is HTML
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title (prefer h1, fallback to title tag)
            title = None
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.get_text(strip=True)
            else:
                title_tag = soup.find('title')
                title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            
            # Extract main content
            content_data = self.extract_content(soup)
            content = content_data['clean']
            
            # Generate summary if requested
            summary = None
            if self.generate_summaries and content:
                summary = self.generate_summary(content)
            
            # Extract headings for metadata
            headings = []
            for i in range(1, 4):  # Only h1-h3 for cleaner output
                for heading in soup.find_all(f'h{i}'):
                    heading_text = heading.get_text(strip=True)
                    if heading_text and len(heading_text) > 3:
                        headings.append({
                            'level': i,
                            'text': heading_text
                        })
            
            # Extract links for crawling
            links = self.extract_links(soup, url)
            
            page_data = {
                'url': url,
                'title': title,
                'content': content,
                'links': links,
                'status_code': response.status_code
            }
            
            # Add optional fields
            if summary:
                page_data['summary'] = summary
            if headings:
                page_data['headings'] = headings
            
            return page_data
            
        except requests.exceptions.Timeout:
            print(f"⚠️  Timeout: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"⚠️  HTTP Error {e.response.status_code}: {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error: {url} - {str(e)}")
            return None
        except Exception as e:
            print(f"⚠️  Unexpected error: {url} - {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def crawl(self) -> List[Dict]:
        """
        Perform the full crawl starting from base_url.
        
        Returns:
            List of dictionaries containing page data
        """
        print(f"\n🚀 Starting crawl of: {self.base_url}")
        print(f"⚙️  Settings: Rate limit={self.rate_limit}s, Max depth={'unlimited' if self.max_depth is None else self.max_depth}")
        print("-" * 70)
        
        page_count = 0
        
        while self.queue:
            current_url, depth = self.queue.popleft()
            
            # Check depth limit
            if self.max_depth is not None and depth > self.max_depth:
                continue
            
            # Skip if already visited
            normalized = self.normalize_url(current_url)
            if normalized in self.visited_urls:
                continue
            
            self.visited_urls.add(normalized)
            page_count += 1
            
            # Polite delay
            if page_count > 1:
                time.sleep(self.rate_limit)
            
            # Progress update
            print(f"📄 [{page_count}] Scraping (depth {depth}): {current_url}")
            
            # Scrape the page
            page_data = self.scrape_page(current_url)
            
            if page_data:
                # Save page data (remove links from stored data)
                links = page_data.pop('links', [])
                self.pages_data.append(page_data)
                
                # Add new links to queue
                for link in links:
                    normalized_link = self.normalize_url(link)
                    if normalized_link not in self.visited_urls:
                        self.queue.append((normalized_link, depth + 1))
        
        print("-" * 70)
        print(f"✅ Crawl complete! Scraped {len(self.pages_data)} pages successfully.")
        
        return self.pages_data
    
    def save_json(self, filename: str = 'site_content.json'):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.pages_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved JSON data to: {filename}")
    
    def save_markdown(self, filename: str = 'site_content.md'):
        """Save scraped data to a combined Markdown file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Website Content Export\n\n")
            f.write(f"**Source:** {self.base_url}\n")
            f.write(f"**Pages scraped:** {len(self.pages_data)}\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, page in enumerate(self.pages_data, 1):
                f.write(f"## Page {i}: {page['title']}\n\n")
                f.write(f"**URL:** {page['url']}\n\n")
                
                # Write summary if present
                if page.get('summary'):
                    f.write(f"**Summary:** {page['summary']}\n\n")
                
                # Write headings if present
                if page.get('headings'):
                    f.write("**Headings:**\n")
                    for heading in page['headings']:
                        indent = "  " * (heading['level'] - 1)
                        f.write(f"{indent}- {heading['text']}\n")
                    f.write("\n")
                
                f.write("**Content:**\n\n")
                f.write(f"{page['content']}\n\n")
                f.write("---\n\n")
        
        print(f"💾 Saved Markdown file to: {filename}")
    
    def save_individual_markdown_files(self, output_dir: str = 'scraped_pages'):
        """Save each page as a separate Markdown file."""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        for i, page in enumerate(self.pages_data, 1):
            # Create safe filename from title
            safe_title = re.sub(r'[^\w\s-]', '', page['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            safe_title = safe_title.strip('-').lower()
            
            filename = f"{i:03d}_{safe_title[:50]}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {page['title']}\n\n")
                f.write(f"**URL:** {page['url']}\n\n")
                
                if page.get('summary'):
                    f.write(f"**Summary:** {page['summary']}\n\n")
                
                f.write("---\n\n")
                f.write(page['content'])
        
        print(f"💾 Saved {len(self.pages_data)} individual Markdown files to: {output_dir}/")


def main():
    """Command-line interface for the web crawler."""
    parser = argparse.ArgumentParser(
        description='Ethically scrape all pages from a website for content analysis and redesign.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic crawl
  python scrape_site.py https://example.com
  
  # With rate limiting and depth control
  python scrape_site.py https://example.com --rate-limit 2.0 --max-depth 3
  
  # Generate summaries and save as separate files
  python scrape_site.py https://example.com --generate-summaries --separate-files
  
  # Custom output with query params included
  python scrape_site.py https://example.com --output my_site --include-query-params
  
  # JSON only for programmatic use
  python scrape_site.py https://example.com --json-only
        """
    )
    
    parser.add_argument(
        'url',
        help='Base URL to start crawling from'
    )
    
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=1.5,
        help='Seconds to wait between requests (default: 1.5)'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        default=None,
        help='Maximum crawl depth (default: unlimited)'
    )
    
    parser.add_argument(
        '--include-query-params',
        action='store_true',
        help='Treat URLs with different query parameters as unique pages'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--output',
        default='site_content',
        help='Output filename prefix (default: site_content)'
    )
    
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only output JSON file (skip Markdown)'
    )
    
    parser.add_argument(
        '--generate-summaries',
        action='store_true',
        help='Generate automatic summaries for each page'
    )
    
    parser.add_argument(
        '--separate-files',
        action='store_true',
        help='Save each page as a separate Markdown file (in addition to combined file)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        return 1
    
    # Create crawler
    crawler = WebsiteCrawler(
        base_url=args.url,
        rate_limit=args.rate_limit,
        max_depth=args.max_depth,
        include_query_params=args.include_query_params,
        timeout=args.timeout,
        generate_summaries=args.generate_summaries
    )
    
    # Perform crawl
    try:
        crawler.crawl()
        
        # Save results
        json_filename = f"{args.output}.json"
        crawler.save_json(json_filename)
        
        if not args.json_only:
            md_filename = f"{args.output}.md"
            crawler.save_markdown(md_filename)
            
            if args.separate_files:
                crawler.save_individual_markdown_files(f"{args.output}_pages")
        
        print(f"\n✨ All done! You can now use these files for content analysis and redesign.")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Crawl interrupted by user.")
        if crawler.pages_data:
            print(f"Saving {len(crawler.pages_data)} pages scraped so far...")
            crawler.save_json(f"{args.output}_partial.json")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())

