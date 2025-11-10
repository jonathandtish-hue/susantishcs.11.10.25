#!/usr/bin/env python3
"""
Generate a beautiful Tailwind CSS website from scraped JSON data.
VERSION 2 - IMPROVED with all UX fixes.
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
    last_part = parts[-1] if parts[-1] else ''
    if '.' in last_part and 'html' not in last_part:
        return 'home'
    return last_part if last_part else 'home'


def clean_summary(summary):
    """Clean summary text from markdown artifacts."""
    if not summary:
        return ''
    # Remove markdown headings
    summary = re.sub(r'#{1,6}\s*', '', summary)
    # Remove leading dots and periods
    summary = re.sub(r'^\.\s*', '', summary)
    # Clean up multiple spaces
    summary = re.sub(r'\s+', ' ', summary)
    return summary.strip()


def create_navigation(pages, current_slug):
    """Generate navigation HTML with proper order."""
    nav_items = []
    
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('spiritual-healing', 'Spiritual Healing'),
        ('inspiration', 'Inspiration'),
        ('contact', 'Contact')
    ]
    
    for slug, label in page_order:
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
    
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('spiritual-healing', 'Spiritual Healing'),
        ('inspiration', 'Inspiration'),
        ('contact', 'Contact')
    ]
    
    for slug, label in page_order:
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
        
        # Clean up leading dots/periods
        line = re.sub(r'^\.\s+', '', line)
        
        # Headings
        if line.startswith('######'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h6 class="text-base font-semibold text-blue-600 uppercase tracking-wide mt-8 mb-3">{text}</h6>')
        elif line.startswith('#####'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h5 class="text-lg font-semibold text-gray-900 mt-8 mb-3">{text}</h5>')
        elif line.startswith('####'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h4 class="text-xl font-bold text-gray-900 mt-10 mb-4">{text}</h4>')
        elif line.startswith('###'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h3 class="text-2xl font-bold text-gray-900 mt-12 mb-5">{text}</h3>')
        elif line.startswith('##'):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            text = line.replace('#', '').strip()
            html_parts.append(f'<h2 class="text-3xl font-bold text-gray-900 mt-14 mb-6">{text}</h2>')
        # Bullet points
        elif line.startswith('•') or line.startswith('-'):
            text = line[1:].strip()
            if not in_list:
                html_parts.append('<ul class="space-y-3 my-6">')
                in_list = True
            html_parts.append(f'<li class="text-gray-700 leading-relaxed flex items-start"><svg class="w-5 h-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg><span>{text}</span></li>')
        # Regular paragraph
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            # Remove "click here" artifacts and trailing periods after punctuation
            line = re.sub(r'click here\s*\.?', '', line, flags=re.IGNORECASE)
            line = re.sub(r'\?\s*\.', '?', line)
            line = re.sub(r'!\s*\.', '!', line)
            html_parts.append(f'<p class="text-gray-700 text-lg leading-relaxed mb-5">{line}</p>')
    
    if in_list:
        html_parts.append('</ul>')
    
    return '\n'.join(html_parts)


def create_features_section():
    """Create features section for home page."""
    return '''
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 my-16">
            <div class="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Spiritual Healing</h3>
                <p class="text-gray-600">Permanent healing through prayer and understanding of divine laws.</p>
                <a href="spiritual-healing.html" class="text-blue-600 hover:text-blue-800 font-medium mt-4 inline-block">Learn More →</a>
            </div>
            
            <div class="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Professional Care</h3>
                <p class="text-gray-600">Over 12 years of full-time practice as a Christian Science Practitioner.</p>
                <a href="about.html" class="text-blue-600 hover:text-blue-800 font-medium mt-4 inline-block">About Susan →</a>
            </div>
            
            <div class="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Remote Sessions</h3>
                <p class="text-gray-600">Connect via phone, email, or Skype from anywhere in the world.</p>
                <a href="contact.html" class="text-blue-600 hover:text-blue-800 font-medium mt-4 inline-block">Get in Touch →</a>
            </div>
        </div>
    '''


def create_contact_form():
    """Create contact form HTML."""
    return '''
        <div class="bg-white rounded-lg shadow-md p-8 lg:p-12 mt-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">Send Me a Message</h2>
            <form class="space-y-6" action="mailto:susantishcs@gmail.com" method="GET" enctype="text/plain">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Your Name *</label>
                        <input type="text" id="name" name="name" required 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-colors">
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Your Email *</label>
                        <input type="email" id="email" name="email" required 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-colors">
                    </div>
                </div>
                <div>
                    <label for="subject" class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                    <input type="text" id="subject" name="subject" 
                           class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-colors">
                </div>
                <div>
                    <label for="message" class="block text-sm font-medium text-gray-700 mb-2">Your Message *</label>
                    <textarea id="message" name="body" rows="6" required 
                              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-colors"></textarea>
                </div>
                <div>
                    <button type="submit" 
                            class="w-full md:w-auto bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 transition-all transform hover:scale-105">
                        Send Message
                    </button>
                </div>
            </form>
        </div>
    '''


def create_page_template(page, pages, all_pages):
    """Create HTML page from template."""
    slug = get_page_slug(page['url'])
    title = page['title']
    content = page.get('content', '')
    summary = clean_summary(page.get('summary', ''))
    
    # Format content
    formatted_content = format_content(content)
    
    # Special handling for different pages
    is_home = slug == 'home'
    is_contact = slug == 'contact'
    
    # Create hero section for home page
    hero_section = ''
    if is_home and summary:
        hero_section = f'''
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
                <div class="text-center">
                    <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-8 leading-tight">
                        Welcome to<br>Spiritual Healing
                    </h1>
                    <p class="text-xl sm:text-2xl text-blue-50 max-w-3xl mx-auto leading-relaxed mb-10">
                        {summary}
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="contact.html" class="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-all shadow-lg transform hover:scale-105">
                            Get in Touch
                        </a>
                        <a href="services.html" class="inline-block bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-800 transition-all border-2 border-blue-400">
                            View Services
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    # Features section for home page
    features_section = create_features_section() if is_home else ''
    
    # Contact info card for contact page
    contact_card = '''
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-8 mb-8">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">Contact Information</h3>
            <div class="space-y-4">
                <div class="flex items-center bg-white rounded-lg p-4 shadow-sm">
                    <svg class="w-6 h-6 text-blue-600 mr-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    <div>
                        <p class="text-sm text-gray-600">Email</p>
                        <a href="mailto:susantishcs@gmail.com" class="text-blue-600 hover:text-blue-800 font-medium">susantishcs@gmail.com</a>
                    </div>
                </div>
                <div class="flex items-center bg-white rounded-lg p-4 shadow-sm">
                    <svg class="w-6 h-6 text-blue-600 mr-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                    <div>
                        <p class="text-sm text-gray-600">Phone</p>
                        <a href="tel:734-693-5946" class="text-blue-600 hover:text-blue-800 font-medium">734-693-5946</a>
                    </div>
                </div>
                <div class="flex items-center bg-white rounded-lg p-4 shadow-sm">
                    <svg class="w-6 h-6 text-blue-600 mr-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                    <div>
                        <p class="text-sm text-gray-600">Skype</p>
                        <span class="text-gray-700 font-medium">susantishcs</span>
                    </div>
                </div>
            </div>
        </div>
    ''' if is_contact else ''
    
    # Contact form for contact page
    contact_form = create_contact_form() if is_contact else ''
    
    # Clean meta description
    meta_description = clean_summary(summary[:160] if summary else title)
    
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
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
                    <a href="index.html" class="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
                        Susan Tish
                    </a>
                </div>
                
                <!-- Desktop Navigation -->
                <div class="hidden md:flex space-x-1">
                    {create_navigation(pages, slug)}
                </div>
                
                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button type="button" id="mobile-menu-button" class="text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-600 rounded-lg p-2">
                        <svg id="menu-icon" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                        <svg id="close-icon" class="h-6 w-6 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
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
        {features_section if is_home else ""}
        
        {"" if is_home else f'<article class="bg-white rounded-lg shadow-md p-8 lg:p-12">'}
            {'' if is_home else f'<h1 class="text-4xl sm:text-5xl font-bold text-gray-900 mb-6 leading-tight">{title.split("|")[0].strip()}</h1>'}
            
            {f'<div class="bg-blue-50 border-l-4 border-blue-600 p-6 mb-8"><p class="text-lg text-gray-700 leading-relaxed">{summary}</p></div>' if summary and not is_home else ''}
            
            <div class="prose prose-lg max-w-none">
                {formatted_content if not is_home else ''}
            </div>
            
            {contact_card}
            
        {"" if is_home else "</article>"}
        
        {contact_form}
        
        <!-- CTA Section -->
        {'' if is_contact else f'''
        <div class="mt-16 bg-gradient-to-r from-blue-600 to-blue-800 rounded-xl p-10 text-center text-white shadow-xl">
            <h2 class="text-3xl font-bold mb-4">Ready to Begin Your Healing Journey?</h2>
            <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">Contact me today for a free consultation</p>
            <a href="contact.html" class="inline-block bg-white text-blue-600 px-10 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-all shadow-lg transform hover:scale-105">
                Get in Touch
            </a>
        </div>
        '''}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-24">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4">Susan Tish</h3>
                    <p class="text-gray-400 mb-4">Christian Science Practitioner</p>
                    <p class="text-gray-400 text-sm">Providing spiritual healing services with over 12 years of experience.</p>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-2">
                        <li><a href="index.html" class="text-gray-400 hover:text-white transition-colors">Home</a></li>
                        <li><a href="about.html" class="text-gray-400 hover:text-white transition-colors">About</a></li>
                        <li><a href="services.html" class="text-gray-400 hover:text-white transition-colors">Services</a></li>
                        <li><a href="spiritual-healing.html" class="text-gray-400 hover:text-white transition-colors">Spiritual Healing</a></li>
                        <li><a href="inspiration.html" class="text-gray-400 hover:text-white transition-colors">Inspiration</a></li>
                        <li><a href="contact.html" class="text-gray-400 hover:text-white transition-colors">Contact</a></li>
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
                <p>&copy; 2025 Susan Tish. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Mobile Menu Script -->
    <script>
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        const menuIcon = document.getElementById('menu-icon');
        const closeIcon = document.getElementById('close-icon');
        
        mobileMenuButton.addEventListener('click', () => {{
            mobileMenu.classList.toggle('hidden');
            menuIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('hidden');
        }});
    </script>
</body>
</html>'''
    
    return template


def generate_website(json_file='site_content.json', output_dir='website'):
    """Generate complete website from JSON data."""
    print("🎨 Generating IMPROVED Tailwind CSS Website v2.0")
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
    print(f"🎉 IMPROVED Website generated successfully!")
    print(f"📂 Location: {output_dir}/")
    print(f"\n✨ What's New:")
    print(f"   ✓ Fixed navigation order (logical flow)")
    print(f"   ✓ Cleaned markdown from summaries")
    print(f"   ✓ Added contact form")
    print(f"   ✓ Added features section on home")
    print(f"   ✓ Removed duplicate content")
    print(f"   ✓ Fixed broken links")
    print(f"   ✓ Improved typography")
    print(f"   ✓ Better visual hierarchy")
    print(f"   ✓ Complete footer navigation")
    print(f"   ✓ Mobile menu close button")
    print(f"\n💡 To view your website:")
    print(f"   open {output_dir}/index.html")


if __name__ == "__main__":
    generate_website()


