#!/usr/bin/env python3
"""
Simple test script for the web scraper.
Tests basic functionality with a publicly accessible test site.
"""

import sys
import json
from scrape_site import WebsiteCrawler


def test_basic_functionality():
    """Test basic crawling functionality."""
    print("=" * 70)
    print("Testing Web Scraper - Basic Functionality")
    print("=" * 70)
    
    # Use example.com as it's designed for testing
    test_url = "https://example.com"
    
    print(f"\n🧪 Testing with: {test_url}")
    print("This should be a quick test (1 page only)\n")
    
    try:
        # Create crawler with conservative settings
        crawler = WebsiteCrawler(
            base_url=test_url,
            rate_limit=1.0,
            max_depth=0,  # Just the home page
            timeout=10,
            generate_summaries=True
        )
        
        # Perform crawl
        pages = crawler.crawl()
        
        # Validate results
        print("\n" + "=" * 70)
        print("Test Results:")
        print("=" * 70)
        
        assert len(pages) > 0, "❌ No pages were scraped"
        print(f"✅ Successfully scraped {len(pages)} page(s)")
        
        # Check first page structure
        first_page = pages[0]
        
        assert 'url' in first_page, "❌ Missing 'url' field"
        print("✅ URL field present")
        
        assert 'title' in first_page, "❌ Missing 'title' field"
        print(f"✅ Title field present: '{first_page['title']}'")
        
        assert 'content' in first_page, "❌ Missing 'content' field"
        print(f"✅ Content field present ({len(first_page['content'])} characters)")
        
        assert 'summary' in first_page, "❌ Missing 'summary' field"
        print(f"✅ Summary field present: '{first_page['summary'][:50]}...'")
        
        # Test JSON save
        test_json_file = "test_output.json"
        crawler.save_json(test_json_file)
        
        # Verify JSON is valid
        with open(test_json_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            assert len(loaded_data) == len(pages), "❌ JSON data mismatch"
        print(f"✅ JSON output valid and saved")
        
        # Test Markdown save
        test_md_file = "test_output.md"
        crawler.save_markdown(test_md_file)
        
        # Verify Markdown exists and has content
        with open(test_md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            assert len(md_content) > 0, "❌ Empty markdown file"
            assert first_page['title'] in md_content, "❌ Title not in markdown"
        print(f"✅ Markdown output valid and saved")
        
        print("\n" + "=" * 70)
        print("🎉 All Tests Passed!")
        print("=" * 70)
        
        # Show sample output
        print("\n📋 Sample Page Data:")
        print(f"URL: {first_page['url']}")
        print(f"Title: {first_page['title']}")
        print(f"Content length: {len(first_page['content'])} characters")
        print(f"Summary: {first_page.get('summary', 'N/A')}")
        
        print("\n💡 You can now test with your own website:")
        print(f"   python scrape_site.py https://your-website.com")
        
        return True
        
    except AssertionError as e:
        print(f"\n{str(e)}")
        print("\n❌ Tests Failed")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_content_cleaning():
    """Test that content cleaning works properly."""
    print("\n" + "=" * 70)
    print("Testing Content Cleaning")
    print("=" * 70)
    
    from bs4 import BeautifulSoup
    
    # Create a test HTML page with navigation elements
    test_html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <header>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
            </nav>
        </header>
        
        <main>
            <h1>Main Content Title</h1>
            <p>This is the main content of the page that should be extracted.</p>
            <p>This is another paragraph with useful information.</p>
            
            <h2>Section Title</h2>
            <ul>
                <li>First item in list</li>
                <li>Second item in list</li>
            </ul>
        </main>
        
        <footer>
            <p>Copyright 2025</p>
            <nav>
                <a href="/privacy">Privacy</a>
                <a href="/terms">Terms</a>
            </nav>
        </footer>
    </body>
    </html>
    """
    
    # Create a crawler instance
    crawler = WebsiteCrawler(base_url="https://example.com")
    
    # Parse the test HTML
    soup = BeautifulSoup(test_html, 'html.parser')
    
    # Extract content
    content_data = crawler.extract_content(soup)
    clean_content = content_data['clean']
    
    print("\n📄 Extracted Clean Content:")
    print("-" * 70)
    print(clean_content)
    print("-" * 70)
    
    # Validate cleaning
    assert 'Main Content Title' in clean_content, "❌ Main heading not extracted"
    print("✅ Main heading extracted")
    
    assert 'main content of the page' in clean_content, "❌ Paragraph not extracted"
    print("✅ Paragraph content extracted")
    
    assert 'First item in list' in clean_content, "❌ List items not extracted"
    print("✅ List items extracted")
    
    # These should NOT be in the cleaned content
    assert 'Copyright' not in clean_content, "❌ Footer not removed"
    print("✅ Footer removed")
    
    assert 'Privacy' not in clean_content or 'Terms' not in clean_content, "❌ Footer nav not removed"
    print("✅ Footer navigation removed")
    
    print("\n✅ Content cleaning tests passed!")
    return True


if __name__ == "__main__":
    print("\n🧪 Web Scraper Test Suite\n")
    
    # Run tests
    test1_passed = test_basic_functionality()
    test2_passed = test_content_cleaning()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Basic Functionality: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Content Cleaning: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The scraper is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        sys.exit(1)


