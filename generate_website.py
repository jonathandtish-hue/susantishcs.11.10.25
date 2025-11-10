#!/usr/bin/env python3
"""
Generate a beautiful Tailwind CSS website from scraped JSON data.
Creates a modern, responsive multi-page website.
"""

import json
import os
import re
from pathlib import Path


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def get_page_slug(url):
    """Extract page slug from URL."""
    if url.endswith('/'):
        url = url[:-1]
    parts = url.split('/')
    # If the last part contains a domain, it's the home page
    last_part = parts[-1] if parts[-1] else ''
    if '.' in last_part and 'html' not in last_part:
        return 'home'
    return last_part if last_part else 'home'


def create_navigation(pages, current_slug):
    """Generate navigation HTML."""
    nav_items = []
    
    # Define page order and labels - LOGICAL USER JOURNEY ORDER
    page_order = {
        'home': 'Home',
        'about': 'About',
        'services': 'Services',
        'spiritual-healing': 'Spiritual Healing',
        'inspiration': 'Inspiration',
        'contact': 'Contact'
    }
    
    for page in pages:
        slug = get_page_slug(page['url'])
        label = page_order.get(slug, page['title'])
        
        # Skip if not in defined order
        if slug not in page_order:
            continue
        
        active_class = 'text-blue-600 border-b-2 border-blue-600' if slug == current_slug else 'text-gray-600 hover:text-blue-600'
        
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        
        nav_items.append(f'''
            <a href="{filename}" class="{active_class} px-3 py-2 text-sm font-medium transition-colors duration-200">
                {label}
            </a>
        ''')
    
    return ''.join(nav_items)


def create_mobile_navigation(pages, current_slug):
    """Generate mobile navigation HTML."""
    nav_items = []
    
    page_order = {
        'home': 'Home',
        'about': 'About',
        'services': 'Services',
        'spiritual-healing': 'Spiritual Healing',
        'inspiration': 'Inspiration',
        'contact': 'Contact'
    }
    
    for page in pages:
        slug = get_page_slug(page['url'])
        label = page_order.get(slug, page['title'])
        
        if slug not in page_order:
            continue
        
        active_class = 'bg-blue-50 text-blue-600' if slug == current_slug else 'text-gray-600 hover:bg-gray-50'
        
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        
        nav_items.append(f'''
            <a href="{filename}" class="{active_class} block px-4 py-2 text-base font-medium rounded-md transition-colors">
                {label}
            </a>
        ''')
    
    return ''.join(nav_items)


def format_content(content):
    """Convert markdown-style content to HTML."""
    if not content:
        return ''
    
    lines = content.split('\n')
    html_parts = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append('<div class="h-4"></div>')
            continue
        
        # Headings
        if line.startswith('######'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h6 class="text-sm font-semibold text-gray-900 uppercase tracking-wide mt-6 mb-2">{text}</h6>')
        elif line.startswith('#####'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h5 class="text-base font-semibold text-gray-900 mt-6 mb-2">{text}</h5>')
        elif line.startswith('####'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h4 class="text-xl font-semibold text-gray-900 mt-8 mb-3">{text}</h4>')
        elif line.startswith('###'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h3 class="text-2xl font-bold text-gray-900 mt-10 mb-4">{text}</h3>')
        elif line.startswith('##'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h2 class="text-3xl font-bold text-gray-900 mt-12 mb-6">{text}</h2>')
        # Bullet points
        elif line.startswith('•') or line.startswith('-'):
            text = line[1:].strip()
            if not in_list:
                html_parts.append('<ul class="space-y-2 ml-4">')
                in_list = True
            html_parts.append(f'<li class="text-gray-700 leading-relaxed flex items-start"><span class="text-blue-600 mr-2">•</span><span>{text}</span></li>')
        # Regular paragraph
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<p class="text-gray-700 leading-relaxed mb-4">{line}</p>')
    
    if in_list:
        html_parts.append('</ul>')
    
    return '\n'.join(html_parts)


def create_page_template(page, pages, all_pages):
    """Create HTML page from template."""
    slug = get_page_slug(page['url'])
    title = page['title']
    content = page.get('content', '')
    summary = page.get('summary', '')
    
    # Format content
    formatted_content = format_content(content)
    
    # Special handling for home page
    is_home = slug == 'home'
    
    # Create hero section for home page
    hero_section = ''
    if is_home and summary:
        hero_section = f'''
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
                <div class="text-center">
                    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
                        Welcome to Spiritual Healing
                    </h1>
                    <p class="text-xl sm:text-2xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
                        {summary}
                    </p>
                    <div class="mt-10">
                        <a href="contact.html" class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors shadow-lg">
                            Get in Touch
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    # Create contact section for contact page
    contact_section = ''
    if slug == 'contact':
        contact_section = '''
        <div class="bg-blue-50 rounded-lg p-8 mt-8">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">Contact Information</h3>
            <div class="space-y-4">
                <div class="flex items-center">
                    <svg class="w-6 h-6 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    <a href="mailto:susantishcs@gmail.com" class="text-blue-600 hover:text-blue-800">susantishcs@gmail.com</a>
                </div>
                <div class="flex items-center">
                    <svg class="w-6 h-6 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                    <a href="tel:734-693-5946" class="text-blue-600 hover:text-blue-800">734-693-5946</a>
                </div>
                <div class="flex items-center">
                    <svg class="w-6 h-6 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                    <span class="text-gray-700">Skype: susantishcs</span>
                </div>
            </div>
        </div>
        '''
    
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{summary[:160] if summary else title}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <a href="index.html" class="text-2xl font-bold text-blue-600">
                        Susan Tish
                    </a>
                </div>
                
                <!-- Desktop Navigation -->
                <div class="hidden md:flex space-x-1">
                    {create_navigation(pages, slug)}
                </div>
                
                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button type="button" id="mobile-menu-button" class="text-gray-600 hover:text-gray-900 focus:outline-none">
                        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </nav>
        
        <!-- Mobile menu -->
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-200">
            <div class="px-4 pt-2 pb-3 space-y-1">
                {create_mobile_navigation(pages, slug)}
            </div>
        </div>
    </header>

    <!-- Hero Section (Home page only) -->
    {hero_section}

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <article class="bg-white rounded-lg shadow-md p-8 lg:p-12">
            {"" if is_home else f'<h1 class="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">{title.split("|")[0].strip()}</h1>'}
            
            {f'<div class="bg-blue-50 border-l-4 border-blue-600 p-6 mb-8"><p class="text-lg text-gray-700 italic">{summary}</p></div>' if summary and not is_home else ''}
            
            <div class="prose prose-lg max-w-none">
                {formatted_content}
            </div>
            
            {contact_section}
        </article>
        
        <!-- CTA Section -->
        {f'''
        <div class="mt-12 bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-8 text-center text-white">
            <h2 class="text-3xl font-bold mb-4">Ready to Begin Your Healing Journey?</h2>
            <p class="text-xl text-blue-100 mb-6">Contact me today for a consultation</p>
            <a href="contact.html" class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors shadow-lg">
                Get in Touch
            </a>
        </div>
        ''' if slug != 'contact' else ''}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4">Susan Tish</h3>
                    <p class="text-gray-400">Christian Science Practitioner</p>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-2">
                        <li><a href="spiritual-healing.html" class="text-gray-400 hover:text-white transition-colors">Spiritual Healing</a></li>
                        <li><a href="services.html" class="text-gray-400 hover:text-white transition-colors">Services</a></li>
                        <li><a href="about.html" class="text-gray-400 hover:text-white transition-colors">About</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Contact</h3>
                    <ul class="space-y-2 text-gray-400">
                        <li>Email: <a href="mailto:susantishcs@gmail.com" class="hover:text-white transition-colors">susantishcs@gmail.com</a></li>
                        <li>Phone: <a href="tel:734-693-5946" class="hover:text-white transition-colors">734-693-5946</a></li>
                        <li>Skype: susantishcs</li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                <p>&copy; 2025 Susan Tish. All rights reserved. | Design by Jonathan Tish</p>
            </div>
        </div>
    </footer>

    <!-- Mobile Menu Script -->
    <script>
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        
        mobileMenuButton.addEventListener('click', () => {{
            mobileMenu.classList.toggle('hidden');
        }});
    </script>
</body>
</html>'''
    
    return template


def generate_website(json_file='site_content.json', output_dir='website'):
    """Generate complete website from JSON data."""
    print("🎨 Generating Tailwind CSS Website")
    print("=" * 70)
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        pages = json.load(f)
    
    print(f"📄 Loaded {len(pages)} pages from {json_file}")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Created output directory: {output_dir}/")
    
    # Sort pages by URL for consistent order
    pages_sorted = sorted(pages, key=lambda p: get_page_slug(p['url']))
    
    # Generate pages
    for page in pages_sorted:
        slug = get_page_slug(page['url'])
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        filepath = Path(output_dir) / filename
        
        html = create_page_template(page, pages_sorted, pages)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated: {filename}")
    
    print("=" * 70)
    print(f"🎉 Website generated successfully!")
    print(f"📂 Location: {output_dir}/")
    print(f"\n💡 To view your website:")
    print(f"   open {output_dir}/index.html")


if __name__ == "__main__":
    generate_website()

