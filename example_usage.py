#!/usr/bin/env python3
"""
Example usage of the WebsiteCrawler class for programmatic access.

This demonstrates how to use the crawler in your own Python scripts
rather than via the command line.
"""

from scrape_site import WebsiteCrawler

# Example 1: Basic usage
def basic_example():
    """Simple crawl with default settings."""
    print("=" * 70)
    print("Example 1: Basic Crawl")
    print("=" * 70)
    
    crawler = WebsiteCrawler(
        base_url="https://example.com",
        rate_limit=1.5  # Wait 1.5 seconds between requests
    )
    
    # Perform the crawl
    pages = crawler.crawl()
    
    # Save outputs
    crawler.save_json("example1_output.json")
    crawler.save_markdown("example1_output.md")
    
    print(f"\n✅ Crawled {len(pages)} pages")
    return pages


# Example 2: Advanced usage with all options
def advanced_example():
    """Crawl with summaries, depth limit, and custom settings."""
    print("\n" + "=" * 70)
    print("Example 2: Advanced Crawl with Summaries")
    print("=" * 70)
    
    crawler = WebsiteCrawler(
        base_url="https://example.com",
        rate_limit=2.0,              # Slower, more polite
        max_depth=3,                 # Only go 3 levels deep
        timeout=15,                  # Wait up to 15 seconds per page
        generate_summaries=True,     # Auto-generate summaries
        include_query_params=False   # Ignore query parameters
    )
    
    # Perform the crawl
    pages = crawler.crawl()
    
    # Save in multiple formats
    crawler.save_json("example2_output.json")
    crawler.save_markdown("example2_output.md")
    crawler.save_individual_markdown_files("example2_pages")
    
    print(f"\n✅ Crawled {len(pages)} pages with summaries")
    return pages


# Example 3: Processing the scraped data
def process_data_example():
    """Show how to access and process the scraped data."""
    print("\n" + "=" * 70)
    print("Example 3: Processing Scraped Data")
    print("=" * 70)
    
    crawler = WebsiteCrawler(
        base_url="https://example.com",
        rate_limit=1.5,
        max_depth=2,
        generate_summaries=True
    )
    
    # Crawl the site
    pages = crawler.crawl()
    
    # Process the results
    print("\n📊 Analysis:")
    print(f"Total pages: {len(pages)}")
    
    # Find longest content
    longest_page = max(pages, key=lambda p: len(p.get('content', '')))
    print(f"Longest page: {longest_page['url']} ({len(longest_page['content'])} chars)")
    
    # Count pages with specific headings
    pages_with_h1 = sum(1 for p in pages if any(
        h['level'] == 1 for h in p.get('headings', [])
    ))
    print(f"Pages with H1 headings: {pages_with_h1}")
    
    # List all unique h1 headings
    print("\n📝 All H1 Headings:")
    for page in pages:
        for heading in page.get('headings', []):
            if heading['level'] == 1:
                print(f"  - {heading['text']} (from {page['url']})")
    
    # Show summaries if available
    if pages and pages[0].get('summary'):
        print("\n📄 First 3 Page Summaries:")
        for i, page in enumerate(pages[:3], 1):
            print(f"\n{i}. {page['title']}")
            print(f"   {page.get('summary', 'No summary')}")
    
    return pages


# Example 4: Error handling and partial saves
def error_handling_example():
    """Demonstrate proper error handling."""
    print("\n" + "=" * 70)
    print("Example 4: Error Handling")
    print("=" * 70)
    
    crawler = WebsiteCrawler(
        base_url="https://example.com",
        rate_limit=1.0,
        timeout=5  # Short timeout to demonstrate handling
    )
    
    try:
        pages = crawler.crawl()
        crawler.save_json("example4_output.json")
        print(f"\n✅ Successfully crawled {len(pages)} pages")
        
    except KeyboardInterrupt:
        print("\n⚠️  Crawl interrupted!")
        if crawler.pages_data:
            print(f"Saving {len(crawler.pages_data)} pages collected so far...")
            crawler.save_json("example4_partial.json")
            
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        if crawler.pages_data:
            print(f"Saving {len(crawler.pages_data)} pages collected so far...")
            crawler.save_json("example4_partial.json")
    
    return crawler.pages_data


# Example 5: Custom filtering and processing
def custom_filtering_example():
    """Filter and process pages based on custom criteria."""
    print("\n" + "=" * 70)
    print("Example 5: Custom Filtering")
    print("=" * 70)
    
    crawler = WebsiteCrawler(
        base_url="https://example.com",
        rate_limit=1.5
    )
    
    pages = crawler.crawl()
    
    # Filter pages by content length
    substantial_pages = [
        p for p in pages 
        if len(p.get('content', '')) > 500
    ]
    
    print(f"\n📏 Content length analysis:")
    print(f"Total pages: {len(pages)}")
    print(f"Pages with >500 chars: {len(substantial_pages)}")
    
    # Filter pages by title keywords
    keyword = "about"
    matching_pages = [
        p for p in pages 
        if keyword.lower() in p.get('title', '').lower()
    ]
    
    print(f"\nPages with '{keyword}' in title: {len(matching_pages)}")
    for page in matching_pages:
        print(f"  - {page['title']}: {page['url']}")
    
    # Create a custom JSON output with only substantial pages
    import json
    with open('example5_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(substantial_pages, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved {len(substantial_pages)} filtered pages to example5_filtered.json")
    
    return substantial_pages


if __name__ == "__main__":
    print("Website Crawler - Usage Examples")
    print("=" * 70)
    print("\nThese examples demonstrate various ways to use the WebsiteCrawler.")
    print("Uncomment the example you want to run below.")
    print("\n⚠️  WARNING: These examples use 'example.com' which is a demo domain.")
    print("Replace with a real URL you have permission to scrape.")
    print("=" * 70)
    
    # Uncomment the example you want to run:
    
    # basic_example()
    # advanced_example()
    # process_data_example()
    # error_handling_example()
    # custom_filtering_example()
    
    print("\n" + "=" * 70)
    print("💡 Tip: Modify these examples for your specific use case!")
    print("=" * 70)


