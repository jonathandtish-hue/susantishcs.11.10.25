#!/usr/bin/env python3
"""
Generate a beautiful Tailwind CSS website from scraped JSON data.
VERSION 3 - VISUAL DESIGN with cards, sections, and imagery.
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
    summary = re.sub(r'#{1,6}\s*', '', summary)
    summary = re.sub(r'^\.\s*', '', summary)
    summary = re.sub(r'\s+', ' ', summary)
    return summary.strip()


def split_into_paragraphs(content):
    """Split content into manageable paragraphs for visual design."""
    if not content:
        return []
    
    # Split by double newlines or paragraph markers
    paragraphs = re.split(r'\n{2,}', content)
    cleaned = []
    
    for p in paragraphs:
        p = p.strip()
        if len(p) > 20:  # Only include substantial paragraphs
            # Remove markdown artifacts
            p = re.sub(r'#{1,6}\s*', '', p)
            p = re.sub(r'^\.\s*', '', p)
            p = re.sub(r'click here\s*\.?', '', p, flags=re.IGNORECASE)
            p = re.sub(r'\?\s*\.', '?', p)
            p = re.sub(r'!\s*\.', '!', p)
            
            # If paragraph is too long (> 500 chars), try to split it further
            if len(p) > 500:
                # Try to split by sentences
                sentences = re.split(r'(?<=[.!?])\s+', p)
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) < 400:
                        current_chunk += " " + sentence if current_chunk else sentence
                    else:
                        if current_chunk:
                            cleaned.append(current_chunk.strip())
                        current_chunk = sentence
                if current_chunk:
                    cleaned.append(current_chunk.strip())
            else:
                cleaned.append(p)
    
    return cleaned


def create_visual_content_sections(content):
    """Create visually appealing sections from content."""
    paragraphs = split_into_paragraphs(content)
    
    if not paragraphs:
        return ''
    
    sections = []
    card_colors = [
        'from-blue-50 to-cyan-50',
        'from-indigo-50 to-purple-50',
        'from-purple-50 to-pink-50',
        'from-teal-50 to-blue-50'
    ]
    
    for i, para in enumerate(paragraphs):
        # Check if it's a heading (all caps or very short)
        if para.isupper() and len(para) < 50:
            sections.append(f'''
                <div class="flex items-center gap-4 my-10">
                    <div class="flex-shrink-0 w-2 h-12 bg-gradient-to-b from-blue-600 to-indigo-600 rounded-full"></div>
                    <h3 class="text-3xl font-bold text-gray-900">{para}</h3>
                </div>
            ''')
        elif len(para) < 80:
            # Very short - treat as subheading
            sections.append(f'''
                <h4 class="text-xl font-bold text-blue-600 mb-4 mt-8">{para}</h4>
            ''')
        elif i == 0:
            # First paragraph - make it stand out with gradient
            color = card_colors[0]
            sections.append(f'''
                <div class="bg-gradient-to-br {color} rounded-2xl p-8 mb-8 shadow-lg border border-blue-100">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-1 bg-gradient-to-b from-blue-600 to-indigo-600 rounded-full self-stretch"></div>
                        <p class="text-xl text-gray-800 leading-relaxed font-medium">{para}</p>
                    </div>
                </div>
            ''')
        elif len(para) < 150:
            # Short paragraph - highlighted quote style
            sections.append(f'''
                <div class="relative bg-white rounded-xl p-6 my-6 shadow-md hover:shadow-lg transition-all border-l-4 border-blue-500">
                    <svg class="absolute top-4 right-4 w-8 h-8 text-blue-200" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"></path>
                    </svg>
                    <p class="text-gray-700 text-lg leading-relaxed italic relative z-10">{para}</p>
                </div>
            ''')
        else:
            # Regular paragraph - alternating card styles
            color_index = (i // 2) % len(card_colors)
            if i % 2 == 0:
                # White card with colored left border
                border_colors = ['border-blue-500', 'border-indigo-500', 'border-purple-500', 'border-teal-500']
                border = border_colors[color_index]
                sections.append(f'''
                    <div class="bg-white rounded-xl p-8 mb-6 shadow-md hover:shadow-xl transition-all border-l-4 {border}">
                        <p class="text-gray-700 text-lg leading-relaxed">{para}</p>
                    </div>
                ''')
            else:
                # Subtle gradient card
                color = card_colors[color_index]
                sections.append(f'''
                    <div class="bg-gradient-to-br {color} rounded-xl p-8 mb-6 shadow-md hover:shadow-lg transition-all">
                        <p class="text-gray-800 text-lg leading-relaxed">{para}</p>
                    </div>
                ''')
    
    return '\n'.join(sections)


def create_navigation(pages, current_slug):
    """Generate navigation HTML with proper order."""
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('spiritual-healing', 'Spiritual Healing'),
        ('inspiration', 'Inspiration'),
        ('contact', 'Contact')
    ]
    
    nav_items = []
    for slug, label in page_order:
        active_class = 'text-blue-600 border-b-2 border-blue-600' if slug == current_slug else 'text-gray-700 hover:text-blue-600'
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        nav_items.append(f'<a href="{filename}" class="{active_class} px-3 py-2 text-sm font-semibold transition-colors duration-200">{label}</a>')
    
    return ''.join(nav_items)


def create_mobile_navigation(pages, current_slug):
    """Generate mobile navigation HTML."""
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('spiritual-healing', 'Spiritual Healing'),
        ('inspiration', 'Inspiration'),
        ('contact', 'Contact')
    ]
    
    nav_items = []
    for slug, label in page_order:
        active_class = 'bg-blue-50 text-blue-600 font-semibold' if slug == current_slug else 'text-gray-700 hover:bg-gray-50'
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        nav_items.append(f'<a href="{filename}" class="{active_class} block px-4 py-3 text-base rounded-md transition-colors">{label}</a>')
    
    return ''.join(nav_items)


def create_hero_with_image(title, summary, cta1_text="Get in Touch", cta1_link="contact.html", cta2_text="Learn More", cta2_link="services.html"):
    """Create an impressive hero section."""
    return f'''
    <div class="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
        <!-- Decorative background pattern -->
        <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
        </div>
        
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <!-- Text Content -->
                <div class="text-center lg:text-left">
                    <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
                        {title}
                    </h1>
                    <p class="text-xl sm:text-2xl text-blue-50 mb-10 leading-relaxed">
                        {summary}
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                        <a href="{cta1_link}" class="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:bg-blue-50 transition-all shadow-xl transform hover:scale-105 hover:shadow-2xl">
                            {cta1_text}
                        </a>
                        <a href="{cta2_link}" class="inline-block bg-transparent text-white px-8 py-4 rounded-lg font-bold hover:bg-blue-700 transition-all border-2 border-white">
                            {cta2_text}
                        </a>
                    </div>
                </div>
                
                <!-- Image/Illustration Placeholder -->
                <div class="hidden lg:block">
                    <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
                        <div class="aspect-square bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center">
                            <svg class="w-48 h-48 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''


def create_page_template(page, pages, all_pages):
    """Create beautiful HTML page with visual design."""
    slug = get_page_slug(page['url'])
    title = page['title']
    content = page.get('content', '')
    summary = clean_summary(page.get('summary', ''))
    
    is_home = slug == 'home'
    is_contact = slug == 'contact'
    is_about = slug == 'about'
    
    # Clean meta description
    meta_description = clean_summary(summary[:160] if summary else title)
    
    # Hero section
    hero_section = ''
    if is_home:
        hero_section = create_hero_with_image(
            "Welcome to Spiritual Healing",
            summary or "Experience permanent healing through prayer and understanding of divine laws.",
            "Get in Touch", "contact.html",
            "View Services", "services.html"
        )
    elif is_about:
        hero_section = create_hero_with_image(
            "About Susan Tish",
            "Christian Science Practitioner with over 12 years of experience",
            "Contact Me", "contact.html",
            "View Services", "services.html"
        )
    
    # Features section for home
    features_section = ''
    if is_home:
        features_section = '''
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="text-center mb-16">
                <h2 class="text-4xl font-bold text-gray-900 mb-4">How I Can Help You</h2>
                <p class="text-xl text-gray-600 max-w-3xl mx-auto">Discover permanent healing through spiritual understanding</p>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Feature 1 -->
                <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                    <div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Spiritual Healing</h3>
                    <p class="text-gray-600 mb-6 leading-relaxed">Permanent healing through prayer and understanding of divine laws rooted in Christian Science.</p>
                    <a href="spiritual-healing.html" class="text-blue-600 hover:text-blue-700 font-semibold inline-flex items-center group">
                        Learn More 
                        <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                        </svg>
                    </a>
                </div>
                
                <!-- Feature 2 -->
                <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                    <div class="w-20 h-20 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Professional Care</h3>
                    <p class="text-gray-600 mb-6 leading-relaxed">Over 12 years of full-time practice as a dedicated Christian Science Practitioner.</p>
                    <a href="about.html" class="text-blue-600 hover:text-blue-700 font-semibold inline-flex items-center group">
                        About Susan
                        <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                        </svg>
                    </a>
                </div>
                
                <!-- Feature 3 -->
                <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                    <div class="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Remote Sessions</h3>
                    <p class="text-gray-600 mb-6 leading-relaxed">Connect via phone, email, or Skype from anywhere in the world.</p>
                    <a href="contact.html" class="text-blue-600 hover:text-blue-700 font-semibold inline-flex items-center group">
                        Get in Touch
                        <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
        '''
    
    # Contact section
    contact_section = ''
    if is_contact:
        contact_section = '''
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <!-- Contact Info Cards -->
            <div class="space-y-4">
                <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                    <div class="flex items-center">
                        <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                            </svg>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 font-medium">Email</p>
                            <a href="mailto:susantishcs@gmail.com" class="text-blue-600 hover:text-blue-700 font-bold text-lg">susantishcs@gmail.com</a>
                        </div>
                    </div>
                </div>
                
                <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                    <div class="flex items-center">
                        <div class="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                            </svg>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 font-medium">Phone</p>
                            <a href="tel:734-693-5946" class="text-blue-600 hover:text-blue-700 font-bold text-lg">734-693-5946</a>
                        </div>
                    </div>
                </div>
                
                <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                    <div class="flex items-center">
                        <div class="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600 font-medium">Skype</p>
                            <span class="text-gray-900 font-bold text-lg">susantishcs</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Contact Form -->
            <div class="bg-white rounded-xl shadow-lg p-8">
                <h3 class="text-2xl font-bold text-gray-900 mb-6">Send a Message</h3>
                <form class="space-y-5" action="mailto:susantishcs@gmail.com" method="GET" enctype="text/plain">
                    <div>
                        <label for="name" class="block text-sm font-semibold text-gray-700 mb-2">Your Name *</label>
                        <input type="text" id="name" name="name" required 
                               class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">Your Email *</label>
                        <input type="email" id="email" name="email" required 
                               class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                    </div>
                    <div>
                        <label for="message" class="block text-sm font-semibold text-gray-700 mb-2">Your Message *</label>
                        <textarea id="message" name="body" rows="5" required 
                                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"></textarea>
                    </div>
                    <button type="submit" 
                            class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg font-bold hover:from-blue-700 hover:to-indigo-700 focus:ring-4 focus:ring-blue-300 transition-all transform hover:scale-105 shadow-lg">
                        Send Message
                    </button>
                </form>
            </div>
        </div>
        '''
    
    # Main content - visual design
    main_content = ''
    if not is_home and content:
        main_content = f'''
        <div class="max-w-5xl mx-auto">
            {f'<div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 mb-12 shadow-md"><p class="text-2xl text-gray-800 leading-relaxed font-medium text-center">{summary}</p></div>' if summary and not (is_home or is_about) else ''}
            {create_visual_content_sections(content)}
        </div>
        '''
    
    # CTA section
    cta_section = '' if is_contact else '''
    <div class="max-w-4xl mx-auto mt-20">
        <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-3xl p-12 text-center text-white shadow-2xl transform hover:scale-105 transition-transform duration-300">
            <h2 class="text-4xl font-bold mb-4">Ready to Begin Your Healing Journey?</h2>
            <p class="text-xl text-blue-50 mb-8 max-w-2xl mx-auto">Experience permanent health and well-being through spiritual healing</p>
            <a href="contact.html" class="inline-block bg-white text-blue-600 px-12 py-5 rounded-full font-bold hover:bg-blue-50 transition-all shadow-xl transform hover:scale-110 text-lg">
                Get in Touch Today
            </a>
        </div>
    </div>
    '''
    
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-md sticky top-0 z-50 border-b border-gray-100">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex-shrink-0">
                    <a href="index.html" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent hover:from-blue-700 hover:to-indigo-700 transition-all">
                        Susan Tish
                    </a>
                </div>
                <div class="hidden md:flex space-x-1">
                    {create_navigation(pages, slug)}
                </div>
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
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-200">
            <div class="px-4 pt-2 pb-3 space-y-1">
                {create_mobile_navigation(pages, slug)}
            </div>
        </div>
    </header>

    {hero_section}
    {features_section}

    {f'<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">' if not is_home else '<main class="py-16">'}
        {'' if is_home or is_about else f'<h1 class="text-5xl font-bold text-center text-gray-900 mb-12 max-w-4xl mx-auto leading-tight">{title.split("|")[0].strip()}</h1>'}
        {main_content}
        {contact_section}
        {cta_section}
    </main>

    <!-- Footer -->
    <footer class="bg-gradient-to-br from-gray-900 to-gray-800 text-white mt-24">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
                <div>
                    <h3 class="text-2xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">Susan Tish</h3>
                    <p class="text-gray-300 mb-4 text-lg">Christian Science Practitioner</p>
                    <p class="text-gray-400">Providing spiritual healing services with over 12 years of dedicated experience.</p>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-3">
                        <li><a href="index.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg> Home</a></li>
                        <li><a href="about.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path></svg> About</a></li>
                        <li><a href="services.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"></path></svg> Services</a></li>
                        <li><a href="spiritual-healing.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg> Spiritual Healing</a></li>
                        <li><a href="inspiration.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path></svg> Inspiration</a></li>
                        <li><a href="contact.html" class="text-gray-300 hover:text-white transition-colors flex items-center"><svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path></svg> Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Contact</h3>
                    <ul class="space-y-3 text-gray-300">
                        <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path></svg><a href="mailto:susantishcs@gmail.com" class="hover:text-white transition-colors">susantishcs@gmail.com</a></li>
                        <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"></path></svg><a href="tel:734-693-5946" class="hover:text-white transition-colors">734-693-5946</a></li>
                        <li class="flex items-start"><svg class="w-5 h-5 mr-2 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path></svg>Skype: susantishcs</li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-700 mt-12 pt-8 text-center text-gray-400">
                <p>&copy; 2025 Susan Tish. All rights reserved.</p>
            </div>
        </div>
    </footer>

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
    print("🎨 Generating VISUAL DESIGN Website v3.0")
    print("=" * 70)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        pages = json.load(f)
    
    print(f"📄 Loaded {len(pages)} pages from {json_file}")
    
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Created output directory: {output_dir}/")
    
    pages_sorted = sorted(pages, key=lambda p: get_page_slug(p['url']))
    
    for page in pages_sorted:
        slug = get_page_slug(page['url'])
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        filepath = Path(output_dir) / filename
        
        html = create_page_template(page, pages_sorted, pages)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated: {filename}")
    
    print("=" * 70)
    print(f"🎉 VISUAL Website v3.0 generated!")
    print(f"📂 Location: {output_dir}/")
    print(f"\n✨ New in v3.0:")
    print(f"   ✓ Visual hero sections with decorative backgrounds")
    print(f"   ✓ Content in visual cards (not raw paragraphs)")
    print(f"   ✓ Gradient color blocks")
    print(f"   ✓ Icon-based features with hover effects")
    print(f"   ✓ Pull quotes and highlighted sections")
    print(f"   ✓ No long text walls")
    print(f"   ✓ Professional visual hierarchy")
    print(f"   ✓ Animated elements")
    print(f"\n💡 To view:")
    print(f"   open {output_dir}/index.html")


if __name__ == "__main__":
    generate_website()

