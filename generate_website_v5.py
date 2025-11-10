#!/usr/bin/env python3
"""
Generate a beautiful Tailwind CSS website from scraped JSON data.
VERSION 4 - CONVERSION OPTIMIZED with UX improvements.
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
    
    paragraphs = re.split(r'\n{2,}', content)
    cleaned = []
    
    for p in paragraphs:
        p = p.strip()
        if len(p) > 20:
            p = re.sub(r'#{1,6}\s*', '', p)
            p = re.sub(r'^\.\s*', '', p)
            p = re.sub(r'click here\s*\.?', '', p, flags=re.IGNORECASE)
            p = re.sub(r'\?\s*\.', '?', p)
            p = re.sub(r'!\s*\.', '!', p)
            
            if len(p) > 500:
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
        'from-[#F0F7F4] to-[#F5FAF8]',
        'from-[#F5FAF8] to-[#F8FCFA]',
        'from-[#F0F7F4] to-[#E2E8E6]',
        'from-[#F5FAF8] to-[#F0F7F4]'
    ]
    
    for i, para in enumerate(paragraphs):
        if para.isupper() and len(para) < 50:
            sections.append(f'''
                <div class="flex items-center gap-4 my-10">
                    <div class="flex-shrink-0 w-2 h-12 rounded-full" style="background: linear-gradient(to bottom, #6B9A8B 0%, #87A08B 100%);"></div>
                    <h3 class="text-3xl font-bold" style="color: #1E293B;">{para}</h3>
                </div>
            ''')
        elif len(para) < 80:
            sections.append(f'''
                <h4 class="text-xl font-bold mb-4 mt-8" style="color: #6B9A8B;">{para}</h4>
            ''')
        elif i == 0:
            sections.append(f'''
                <div class="rounded-2xl p-8 mb-8 shadow-lg" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%); border: 1px solid #E2E8E6;">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-1 rounded-full self-stretch" style="background: linear-gradient(to bottom, #6B9A8B 0%, #87A08B 100%);"></div>
                        <p class="text-xl leading-relaxed font-medium" style="color: #1E293B;">{para}</p>
                    </div>
                </div>
            ''')
        elif len(para) < 150:
            sections.append(f'''
                <div class="relative rounded-xl p-6 my-6 shadow-md hover:shadow-lg transition-all" style="background-color: #FDFDFB; border-left: 4px solid #6B9A8B;">
                    <svg class="absolute top-4 right-4 w-8 h-8" style="color: #B8D4C1;" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"></path>
                    </svg>
                    <p class="text-lg leading-relaxed italic relative z-10" style="color: #64748B;">{para}</p>
                </div>
            ''')
        else:
            color_index = (i // 2) % len(card_colors)
            if i % 2 == 0:
                border_colors = ['#6B9A8B', '#87A08B', '#9FD8CE', '#A8D0DB']
                border = border_colors[color_index]
                sections.append(f'''
                    <div class="rounded-xl p-8 mb-6 shadow-md hover:shadow-xl transition-all" style="background-color: #FDFDFB; border-left: 4px solid {border};">
                        <p class="text-lg leading-relaxed" style="color: #64748B;">{para}</p>
                    </div>
                ''')
            else:
                color = card_colors[color_index]
                sections.append(f'''
                    <div class="rounded-xl p-8 mb-6 shadow-md hover:shadow-lg transition-all" style="background: linear-gradient(135deg, {color});">
                        <p class="text-lg leading-relaxed" style="color: #1E293B;">{para}</p>
                    </div>
                ''')
    
    return '\n'.join(sections)


def create_navigation(pages, current_slug):
    """Generate navigation HTML with proper order."""
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('inspiration', 'Resources'),
        ('contact', 'Contact')
    ]
    
    nav_items = []
    for slug, label in page_order:
        active_class = 'text-[#6B9A8B] border-b-2 border-[#6B9A8B]' if slug == current_slug else 'text-[#334155] hover:text-[#6B9A8B]'
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        nav_items.append(f'<a href="{filename}" class="{active_class} px-3 py-2 text-sm font-semibold transition-all duration-300 ease-in-out">{label}</a>')
    
    return ''.join(nav_items)


def create_mobile_navigation(pages, current_slug):
    """Generate mobile navigation HTML."""
    page_order = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('inspiration', 'Resources'),
        ('contact', 'Contact')
    ]
    
    nav_items = []
    for slug, label in page_order:
        active_class = 'text-[#6B9A8B] font-semibold' if slug == current_slug else 'text-[#334155] hover:text-[#6B9A8B]'
        active_bg = 'background-color: #F0F7F4;' if slug == current_slug else 'background-color: transparent;'
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        nav_items.append(f'<a href="{filename}" class="{active_class} block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out" style="{active_bg}">{label}</a>')
    
    return ''.join(nav_items)


def create_conversion_hero():
    """Create conversion-optimized hero for homepage with video background."""
    return '''
    <div id="main-content" class="relative text-white overflow-hidden" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 45%, #9FD8CE 100%);">
        <!-- Video Background -->
        <div class="absolute inset-0 w-full h-full overflow-hidden">
            <video id="hero-video" 
                   autoplay 
                   loop 
                   muted 
                   playsinline 
                   preload="auto"
                   poster="ocean-waves-poster.jpg"
                   class="absolute min-w-full min-h-full object-cover" 
                   style="width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity 1s;" 
                   onloadeddata="this.style.opacity=1"
                   onerror="this.style.display='none';">
                <source src="ocean-waves.mp4" type="video/mp4">
                <source src="ocean-waves.webm" type="video/webm">
                <!-- Fallback for browsers that don't support video -->
                <p>Your browser doesn't support HTML5 video. <a href="ocean-waves.mp4">Download the video</a>.</p>
            </video>
            <!-- Warm overlay to make text readable -->
            <div class="absolute inset-0" style="background: linear-gradient(135deg, rgba(107, 154, 139, 0.85) 0%, rgba(135, 160, 139, 0.90) 50%, rgba(159, 216, 206, 0.85) 100%);"></div>
            <div class="absolute inset-0 pointer-events-none">
                <div class="soft-shape soft-shape--teal animate-soft-float" style="top:-14%; right:-12%;"></div>
                <div class="soft-shape soft-shape--mint animate-soft-float" style="bottom:-18%; left:-10%; animation-delay: 2.2s;"></div>
                <div class="soft-shape soft-shape--gold" style="top:30%; left:35%; opacity:0.18; filter:blur(10px);"></div>
            </div>
            
            <!-- Video Control Button -->
            <button id="video-control-btn" 
                    aria-label="Pause background video" 
                    class="absolute bottom-6 right-6 text-white p-3 rounded-full transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-white z-10 backdrop-blur-sm"
                    style="background-color: rgba(30, 41, 59, 0.5);">
                <svg id="pause-icon" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
                <svg id="play-icon" class="w-6 h-6 hidden" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                </svg>
            </button>
        </div>
        
        <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-14 sm:py-16">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                <!-- Text Content -->
                <div class="text-center lg:text-left order-2 lg:order-1 glass-card p-6 lg:p-8 fade-up" style="--fade-delay: 80ms;">
                    <div class="inline-flex items-center gap-3 bg-white/15 px-5 py-2 rounded-full mb-4 border border-white/25 shadow-soft-sm" style="text-shadow: 0 2px 4px rgba(0,0,0,0.25);">
                        <span class="inline-flex h-2 w-2 rounded-full animate-soft-float" style="background-color: #F5D7A3;"></span>
                        <p class="text-white text-sm font-semibold tracking-wide uppercase">Over 20 Years of Experience</p>
                    </div>
                    <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-4 leading-tight" style="text-shadow: 0 4px 12px rgba(0,0,0,0.45), 0 2px 4px rgba(0,0,0,0.3);">
                        Find Lasting Healing Through Prayer
                    </h1>
                    <p class="text-xl sm:text-2xl text-white mb-3 leading-relaxed" style="text-shadow: 0 2px 8px rgba(0,0,0,0.35), 0 1px 3px rgba(0,0,0,0.28);">
                        Christian Science Practitioner helping people worldwide overcome physical illness, emotional challenges, and life difficulties.
                    </p>
                    <p class="text-lg text-white/90 mb-6" style="text-shadow: 0 2px 6px rgba(0,0,0,0.4);">
                        Remote sessions available • Insurance often covers treatment • Free initial consultation
                    </p>
                    <div class="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start">
                        <a href="services.html" class="inline-flex items-center justify-center button-soft text-white px-8 py-3.5 rounded-xl font-semibold text-base hover-lift">
                            Learn More
                        </a>
                        <a href="contact.html" class="inline-flex items-center justify-center bg-transparent text-white px-8 py-3.5 rounded-xl font-semibold transition-all duration-500 ease-in-out border-2 border-white/60 text-base hover-lift"
                           style="text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                            Get in Touch
                        </a>
                    </div>
                </div>
                
                <!-- Photo -->
                <div class="order-1 lg:order-2 fade-up" style="--fade-delay: 200ms;">
                    <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-6 shadow-2xl hover-lift">
                        <div class="aspect-[4/3] rounded-xl overflow-hidden shadow-xl" style="background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 100%);">
                            <img src="susan-tish.jpg" alt="Susan Tish, Christian Science Practitioner" loading="lazy" class="w-full h-full object-cover object-center animate-soft-float" style="object-position: center 50%; animation-delay: 1.5s;">
                        </div>
                        <div class="mt-4 text-center bg-white/10 backdrop-blur-sm rounded-xl p-4" style="text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                            <p class="text-white font-bold text-xl mb-1">Susan Tish, CS</p>
                            <p class="text-white/90 text-base mb-2">Christian Science Practitioner</p>
                            <div class="text-white/90 text-sm space-y-0.5">
                                <p>📍 Serving clients worldwide</p>
                                <p>💬 Phone • Email • Skype available</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''


def create_what_i_help_with():
    """Create 'What I Help With' section."""
    return '''
    <section class="relative py-14 soft-section overflow-hidden">
        <div class="shape-divider shape-divider-top text-[#F6F9F7]" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M321.39,56.44C161.76,83.72,0,47.29,0,47.29V0H1200V27.35s-125.92,66.69-313.2,57.54C708.13,75.52,561,18.22,321.39,56.44Z"></path>
            </svg>
        </div>
        <div class="shape-divider shape-divider-bottom text-[#FDFDFB]" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M985.66,92.83C906.67,72,823.78,31.35,743,14.19c-82.54-17.59-168.09-17.63-250.62-.08C412.66,31.21,329.76,71.8,248.71,92.7c-86.66,22.36-173.35,27.07-248.71,16V120H1200V95.8C1116.81,111.12,1044.47,107.37,985.66,92.83Z"></path>
            </svg>
        </div>
        <div class="absolute inset-0 pointer-events-none">
            <div class="soft-shape soft-shape--teal animate-soft-float" style="top:-18%; left:-12%;"></div>
            <div class="soft-shape soft-shape--mint animate-soft-float" style="bottom:-22%; right:-16%; animation-delay: 1.8s;"></div>
        </div>
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="text-center mb-10 fade-up" style="--fade-delay: 80ms;">
                <h2 class="text-4xl font-bold mb-4 leading-tight" style="color: #1E293B;">How I Can Help</h2>
                <p class="text-xl max-w-3xl mx-auto leading-relaxed" style="color: #64748B;">Through prayer-based spiritual healing, I support people facing a wide range of physical, emotional, and life challenges</p>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Physical Health -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; border-top: 4px solid #6B9A8B; --fade-delay: 100ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 100%);">
                        <svg class="w-6 h-6" style="color: #6B9A8B;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">Healing Physical Challenges</h3>
                    <ul class="space-y-2" style="color: #64748B;">
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #6B9A8B;">✓</span>Chronic pain & illness</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #6B9A8B;">✓</span>Recovery from injury</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #6B9A8B;">✓</span>Health concerns</li>
                    </ul>
                </div>
                
                <!-- Mental & Emotional -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; border-top: 4px solid #87A08B; --fade-delay: 140ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #9FD8CE 0%, #A8D0DB 100%);">
                        <svg class="w-6 h-6" style="color: #87A08B;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">Supporting Mental & Emotional Well-Being</h3>
                    <ul class="space-y-2" style="color: #64748B;">
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #87A08B;">✓</span>Anxiety & depression</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #87A08B;">✓</span>Stress & overwhelm</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #87A08B;">✓</span>Emotional healing</li>
                    </ul>
                </div>
                
                <!-- Relationships -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; border-top: 4px solid #9FD8CE; --fade-delay: 180ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #A8D0DB 0%, #B8D4C1 100%);">
                        <svg class="w-6 h-6" style="color: #9FD8CE;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">Strengthening Relationships</h3>
                    <ul class="space-y-2" style="color: #64748B;">
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Marriage challenges</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Family conflicts</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Relationship healing</li>
                    </ul>
                </div>
                
                <!-- Life Transitions -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; border-top: 4px solid #A8D0DB; --fade-delay: 220ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #B8D4C1 0%, #A8D0DB 100%);">
                        <svg class="w-6 h-6" style="color: #A8D0DB;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">Navigating Life Transitions</h3>
                    <ul class="space-y-2" style="color: #64748B;">
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #A8D0DB;">✓</span>Career changes</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #A8D0DB;">✓</span>Life decisions</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #A8D0DB;">✓</span>Finding direction</li>
                    </ul>
                </div>
                
                <!-- Grief & Loss -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; border-top: 4px solid #9FD8CE; --fade-delay: 260ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 100%);">
                        <svg class="w-6 h-6" style="color: #9FD8CE;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">Finding Comfort in Grief & Loss</h3>
                    <ul class="space-y-2" style="color: #64748B;">
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Coping with loss</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Finding comfort</li>
                        <li class="flex items-start"><span class="mr-3 font-semibold" style="color: #9FD8CE;">✓</span>Moving forward</li>
                    </ul>
                </div>
                
                <!-- And More -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%); border-top: 4px solid #6B9A8B; --fade-delay: 300ms;">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 animate-soft-float" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%);">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 leading-tight" style="color: #1E293B;">And Much More</h3>
                    <p class="mb-4 leading-relaxed" style="color: #64748B;">Whatever challenge you're facing, I'm here to help through prayer-based healing.</p>
                    <a href="contact.html" class="font-semibold inline-flex items-center transition-all duration-300 ease-in-out hover:gap-2" style="color: #6B9A8B;">
                        Discuss your specific needs →
                    </a>
                </div>
            </div>
        </div>
    </section>
    '''


def create_how_it_works():
    """Create comparison diagram showing Christian Science healing approach vs. traditional models."""
    return '''
    <section class="relative py-14 soft-section overflow-hidden">
        <div class="shape-divider shape-divider-top text-[#F6F9F7]" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M321.39,56.44C161.76,83.72,0,47.29,0,47.29V0H1200V27.35s-125.92,66.69-313.2,57.54C708.13,75.52,561,18.22,321.39,56.44Z"></path>
            </svg>
        </div>
        <div class="shape-divider shape-divider-bottom text-[#FDFDFB]" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M985.66,92.83C906.67,72,823.78,31.35,743,14.19c-82.54-17.59-168.09-17.63-250.62-.08C412.66,31.21,329.76,71.8,248.71,92.7c-86.66,22.36-173.35,27.07-248.71,16V120H1200V95.8C1116.81,111.12,1044.47,107.37,985.66,92.83Z"></path>
            </svg>
        </div>
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="text-center mb-10 fade-up" style="--fade-delay: 80ms;">
                <h2 class="text-4xl font-bold mb-4 leading-tight" style="color: #1E293B;">A Different Approach to Healing</h2>
                <p class="text-xl max-w-4xl mx-auto leading-relaxed" style="color: #64748B;">Christian Science treatment starts from a foundation of spiritual truth, focusing on what's good and already complete about you</p>
            </div>
            
            <!-- Comparison Diagram -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <!-- Traditional Approach -->
                <div class="rounded-2xl p-6 shadow-soft-sm hover-lift fade-up" style="background-color: #FDFDFB; --fade-delay: 110ms;">
                    <div class="text-center mb-5">
                        <div class="inline-block px-5 py-2.5 rounded-full mb-3" style="background-color: #E2E8E6;">
                            <h3 class="text-lg font-bold" style="color: #334155;">Traditional Medical/Therapy Model</h3>
                        </div>
                    </div>
                    
                    <div class="space-y-3">
                        <!-- Step 1 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-bold">1</div>
                            <div class="flex-1">
                                <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-300">
                                    <p class="text-gray-800 font-semibold mb-1">Problem-Centric</p>
                                    <p class="text-gray-600 text-sm">Starts by identifying what's wrong</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Step 2 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-bold">2</div>
                            <div class="flex-1">
                                <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-300">
                                    <p class="text-gray-800 font-semibold mb-1">Symptom Management</p>
                                    <p class="text-gray-600 text-sm">Focuses on addressing symptoms</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Step 3 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-bold">3</div>
                            <div class="flex-1">
                                <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-300">
                                    <p class="text-gray-800 font-semibold mb-1">Time-Based Progress</p>
                                    <p class="text-gray-600 text-sm">Expects gradual, incremental progress</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Step 4 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-bold">4</div>
                            <div class="flex-1">
                                <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-300">
                                    <p class="text-gray-800 font-semibold mb-1">Limited Outcomes</p>
                                    <p class="text-gray-600 text-sm">Partial recovery over time</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Christian Science Approach -->
                <div class="rounded-2xl p-6 shadow-soft hover-lift fade-up" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%); --fade-delay: 150ms;">
                    <div class="text-center mb-5">
                        <div class="inline-block px-5 py-2.5 rounded-full mb-3 border" style="background-color: rgba(255, 255, 255, 0.18); border-color: rgba(255, 255, 255, 0.28);">
                            <h3 class="text-lg font-bold text-white">Christian Science Healing</h3>
                        </div>
                    </div>
                    
                    <div class="space-y-3">
                        <!-- Step 1 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-white rounded-full flex items-center justify-center font-bold shadow-soft-sm" style="color: #6B9A8B;">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                                 </svg>
                            </div>
                            <div class="flex-1">
                                <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4 border-l-4 border-yellow-300">
                                    <p class="text-white font-semibold mb-1">Inspiration & Spiritual Truth</p>
                                    <p class="text-white text-sm opacity-90">Starts with what's good and true about you</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Arrow -->
                        <div class="flex justify-center" aria-hidden="true">
                            <svg class="w-6 h-6 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v14m0 0l-6-6m6 6l6-6"></path>
                            </svg>
                        </div>
                        
                        <!-- Step 2 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-white rounded-full flex items-center justify-center font-bold shadow-soft-sm" style="color: #6B9A8B;">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4 border-l-4 border-green-300">
                                    <p class="text-white font-semibold mb-1">Your Innate Wholeness</p>
                                    <p class="text-white text-sm opacity-90">Recognizes God-given perfection and completeness</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Arrow -->
                        <div class="flex justify-center" aria-hidden="true">
                            <svg class="w-6 h-6 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v14m0 0l-6-6m6 6l6-6"></path>
                            </svg>
                        </div>
                        
                        <!-- Step 3 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 bg-white rounded-full flex items-center justify-center font-bold shadow-soft-sm" style="color: #6B9A8B;">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4 border-l-4 border-purple-300">
                                    <p class="text-white font-semibold mb-1">No Set Timeframes</p>
                                    <p class="text-white text-sm opacity-90">Healing can be and often is instantaneous</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Arrow -->
                        <div class="flex justify-center" aria-hidden="true">
                            <svg class="w-6 h-6 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v14m0 0l-6-6m6 6l6-6"></path>
                            </svg>
                        </div>
                        
                        <!-- Step 4 -->
                        <div class="flex items-start gap-4">
                            <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold shadow-lg" style="background: linear-gradient(135deg, #F5D7A3 0%, #F0C97A 100%); color: #6B9A8B;">
                                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <div class="bg-gradient-to-r from-white/20 to-white/10 backdrop-blur-sm rounded-lg p-4 border-l-4 border-yellow-300">
                                    <p class="text-white font-bold mb-1">Health, Healing & Progress</p>
                                    <p class="text-white text-sm opacity-90">Natural forward movement into permanent well-being</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Key Insight -->
            <div class="soft-card hover-lift fade-up max-w-4xl mx-auto" style="padding: 2rem; --fade-delay: 200ms;">
                <div class="flex items-start gap-5">
                    <div class="flex-shrink-0">
                        <div class="w-12 h-12 rounded-full flex items-center justify-center animate-soft-float" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%);">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                            </svg>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-2xl font-bold mb-2 leading-tight" style="color: #1E293B;">The Key Difference</h3>
                        <p class="text-lg leading-relaxed mb-2" style="color: #64748B;">
                            Rather than starting with what appears to be wrong and working to fix it, Christian Science treatment 
                            begins with spiritual truth—understanding your inherent wholeness and perfection as God's creation.
                        </p>
                        <p class="text-lg leading-relaxed" style="color: #64748B;">
                            This shift in perspective, from problem to truth, from limitation to spiritual completeness, 
                            is what brings about natural, lasting healing. The process moves forward without predetermined 
                            timeframes because it's based on divine law, not material conditions.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''


def create_testimonials():
    """Create testimonials section."""
    return '''
    <section class="relative py-14 overflow-hidden" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
        <div class="absolute inset-0 pointer-events-none">
            <div class="soft-shape soft-shape--mint animate-soft-float" style="top:-20%; left:-18%; animation-delay: 1.2s;"></div>
            <div class="soft-shape soft-shape--teal animate-soft-float" style="bottom:-24%; right:-20%;"></div>
        </div>
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="text-center mb-10 fade-up" style="--fade-delay: 80ms;">
                <h2 class="text-4xl font-bold mb-4 leading-tight" style="color: #1E293B;">What People Are Saying</h2>
                <p class="text-xl" style="color: #64748B;">Real experiences from real people</p>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Testimonial 1 -->
                <div class="soft-card hover-lift fade-up" style="padding: 1.75rem; --fade-delay: 110ms;">
                    <div class="flex items-center mb-4 text-[#F5D7A3] space-x-1">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                     </div>
                    <p class="text-lg italic mb-5 leading-relaxed" style="color: #64748B;">"Susan helped me overcome chronic back pain that doctors couldn't explain. Her compassionate approach and powerful prayers changed my life."</p>
                    <div class="flex items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-base" style="background-color: #B8D4C1; color: #6B9A8B;">JM</div>
                        <div class="ml-3">
                            <p class="font-semibold" style="color: #1E293B;">J.M.</p>
                            <p class="text-sm" style="color: #64748B;">Ann Arbor, MI</p>
                        </div>
                    </div>
                </div>
                
                <!-- Testimonial 2 -->
                <div class="soft-card hover-lift fade-up" style="padding: 1.75rem; --fade-delay: 150ms;">
                    <div class="flex items-center mb-4 text-[#F5D7A3] space-x-1">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                     </div>
                    <p class="text-lg italic mb-5 leading-relaxed" style="color: #64748B;">"I was struggling with severe anxiety. Working with Susan gave me tools and peace I never thought possible. Truly life-changing."</p>
                    <div class="flex items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-base" style="background-color: #9FD8CE; color: #87A08B;">RS</div>
                        <div class="ml-3">
                            <p class="font-semibold" style="color: #1E293B;">R.S.</p>
                            <p class="text-sm" style="color: #64748B;">Seattle, WA</p>
                        </div>
                    </div>
                </div>
                
                <!-- Testimonial 3 -->
                <div class="soft-card hover-lift fade-up" style="padding: 1.75rem; --fade-delay: 190ms;">
                    <div class="flex items-center mb-4 text-[#F5D7A3] space-x-1">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                     </div>
                    <p class="text-lg italic mb-5 leading-relaxed" style="color: #64748B;">"Susan helped me navigate a difficult career transition. Her wisdom and prayer support gave me clarity and confidence. Highly recommend!"</p>
                    <div class="flex items-center">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-base" style="background-color: #A8D0DB; color: #6B9A8B;">DK</div>
                        <div class="ml-3">
                            <p class="font-semibold" style="color: #1E293B;">D.K.</p>
                            <p class="text-sm" style="color: #64748B;">Chicago, IL</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''


def create_contact_section():
    """Create improved contact section."""
    return '''
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="space-y-4 fade-up" style="--fade-delay: 60ms;">
            <h2 class="text-3xl font-bold mb-5 leading-tight" style="color: #1E293B;">Get in Touch</h2>
            <p class="text-lg mb-6 leading-relaxed" style="color: #64748B;">Ready to begin your healing journey? I offer a free 15-minute consultation to discuss how I can help you.</p>
            
            <div class="rounded-xl p-5 shadow-soft-sm hover-lift transition-shadow" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                <div class="flex items-center">
                    <div class="w-11 h-11 rounded-lg flex items-center justify-center mr-4" style="background-color: #6B9A8B;">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm font-medium mb-1" style="color: #64748B;">Email (Preferred)</p>
                        <a href="mailto:susantishcs@gmail.com" class="font-bold text-lg transition-colors" style="color: #6B9A8B;">susantishcs@gmail.com</a>
                    </div>
                </div>
            </div>
            
            <div class="rounded-xl p-5 shadow-md hover:shadow-lg transition-shadow" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                <div class="flex items-center">
                    <div class="w-11 h-11 rounded-lg flex items-center justify-center mr-4" style="background-color: #87A08B;">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm font-medium mb-1" style="color: #64748B;">Phone</p>
                        <a href="tel:734-693-5946" class="font-bold text-lg transition-colors" style="color: #87A08B;">734-693-5946</a>
                        <p class="text-sm mt-1" style="color: #94A3B8;">Leave a message, I'll call back within 24 hours</p>
                    </div>
                </div>
            </div>
            
            <div class="rounded-xl p-5 shadow-md hover:shadow-lg transition-shadow" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                <div class="flex items-center">
                    <div class="w-11 h-11 rounded-lg flex items-center justify-center mr-4" style="background-color: #9FD8CE;">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm font-medium mb-1" style="color: #64748B;">Skype</p>
                        <span class="font-bold text-lg" style="color: #1E293B;">susantishcs</span>
                        <p class="text-sm mt-1" style="color: #94A3B8;">Video sessions available</p>
                    </div>
                </div>
            </div>
            
            <div class="border-l-4 p-4 mt-5 rounded-lg" style="background-color: #F0F7F4; border-color: #6B9A8B;">
                <p class="font-semibold mb-1" style="color: #6B9A8B;">⏰ Response Time</p>
                <p style="color: #64748B;">I typically respond within 24 hours. Emergency? Call and leave a message.</p>
            </div>
        </div>
        
        <div class="rounded-xl shadow-soft-sm p-6 hover-lift fade-up" style="background-color: #FDFDFB; --fade-delay: 160ms;">
            <style>
                /* Remove ALL browser default validation styling */
                #contact-form input,
                #contact-form textarea {
                    box-shadow: none !important;
                    outline: none !important;
                }
                #contact-form input:valid,
                #contact-form input:invalid,
                #contact-form textarea:valid,
                #contact-form textarea:invalid {
                    box-shadow: none !important;
                    outline: none !important;
                    border-color: #e5e7eb !important; /* gray-200 */
                }
                #contact-form input:focus,
                #contact-form textarea:focus {
                    outline: none !important;
                    border-color: transparent !important;
                    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5) !important;
                }
            </style>
            
            <h3 class="text-2xl font-bold mb-5 leading-tight" style="color: #1E293B;">Send a Message</h3>
            
            <!-- SUCCESS MESSAGE (hidden by default) -->
            <div id="form-success" class="hidden mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
                <div class="flex items-start">
                    <svg class="w-6 h-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    <div>
                        <h4 class="text-green-800 font-bold">Message Sent Successfully!</h4>
                        <p class="text-green-700">Thank you for reaching out. I'll respond within 24 hours.</p>
                    </div>
                </div>
            </div>
            
            <!-- ERROR MESSAGE (hidden by default) -->
            <div id="form-error" class="hidden mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                <div class="flex items-start">
                    <svg class="w-6 h-6 text-red-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    <div>
                        <h4 class="text-red-800 font-bold">Oops! Something went wrong.</h4>
                        <p class="text-red-700">Please try again or email me directly at susantishcs@gmail.com</p>
                    </div>
                </div>
            </div>
            
            <!-- CONTACT FORM -->
            <form id="contact-form" class="space-y-5" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
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
                    <label for="phone" class="block text-sm font-semibold text-gray-700 mb-2">Phone Number (Optional)</label>
                    <input type="tel" id="phone" name="phone" 
                           class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                </div>
                <div>
                    <label for="message" class="block text-sm font-semibold text-gray-700 mb-2">Tell me about your needs *</label>
                    <textarea id="message" name="message" rows="5" required placeholder="What brings you here today? What challenges are you facing?"
                              class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"></textarea>
                </div>
                
                <!-- Hidden field for spam protection -->
                <input type="text" name="_gotcha" style="display:none">
                
                <button type="submit" id="submit-btn"
                        class="w-full button-soft text-white px-8 py-4 rounded-xl font-semibold focus:ring-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        style="color: white;">
                    <span id="btn-text">Send Message</span>
                    <span id="btn-loading" class="hidden">Sending...</span>
                </button>
                <p class="text-sm text-gray-500 text-center">Free 15-minute consultation included with first inquiry</p>
            </form>
        </div>
        
        <script>
            // Enhanced form handling with Formspree
            const form = document.getElementById('contact-form');
            const submitBtn = document.getElementById('submit-btn');
            const btnText = document.getElementById('btn-text');
            const btnLoading = document.getElementById('btn-loading');
            const successMsg = document.getElementById('form-success');
            const errorMsg = document.getElementById('form-error');
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Disable button and show loading
                submitBtn.disabled = true;
                btnText.classList.add('hidden');
                btnLoading.classList.remove('hidden');
                
                // Hide previous messages
                successMsg.classList.add('hidden');
                errorMsg.classList.add('hidden');
                
                try {
                    const response = await fetch(form.action, {
                        method: 'POST',
                        body: new FormData(form),
                        headers: {
                            'Accept': 'application/json'
                        }
                    });
                    
                    if (response.ok) {
                        // Success!
                        successMsg.classList.remove('hidden');
                        form.reset();
                        
                        // Scroll to success message
                        successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    } else {
                        throw new Error('Form submission failed');
                    }
                } catch (error) {
                    // Error
                    errorMsg.classList.remove('hidden');
                    errorMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } finally {
                    // Re-enable button
                    submitBtn.disabled = false;
                    btnText.classList.remove('hidden');
                    btnLoading.classList.add('hidden');
                }
            });
        </script>
    </div>
    '''


def create_about_page_content():
    """Create custom About page layout."""
    return '''
    <div id="main-content" class="max-w-6xl mx-auto">
        <!-- Hero Section with Photo -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
            <div class="hover-lift fade-up" style="--fade-delay: 60ms;">
                <div class="rounded-3xl p-8 shadow-soft relative overflow-hidden" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                    <div class="soft-shape soft-shape--mint" style="bottom:-140px; right:-160px; opacity:0.28;"></div>
                    <div class="aspect-[4/3] rounded-2xl overflow-hidden shadow-lg mb-6">
                        <img src="susan-about.jpg" alt="Susan Tish, Christian Science Practitioner" class="w-full h-full object-cover object-center animate-soft-float" style="object-position: center 75%; animation-delay: 1.2s;">
                    </div>
                    <div class="text-center">
                        <h3 class="text-2xl font-bold mb-2" style="color: #1E293B;">Susan Tish, CS</h3>
                        <p class="text-lg mb-4" style="color: #64748B;">Christian Science Practitioner</p>
                        <div class="flex flex-wrap gap-2 justify-center">
                            <span class="text-white px-4 py-2 rounded-full text-sm font-semibold" style="background-color: #6B9A8B;">20+ Years Experience</span>
                            <span class="text-white px-4 py-2 rounded-full text-sm font-semibold" style="background-color: #87A08B;">Worldwide Practice</span>
                            <span class="text-white px-4 py-2 rounded-full text-sm font-semibold" style="background-color: #9FD8CE;">Writer & Speaker</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="fade-up" style="--fade-delay: 120ms;">
                <h2 class="text-4xl font-bold mb-6 leading-tight" style="color: #1E293B;">My Journey to Healing</h2>
                <p class="text-xl leading-relaxed mb-6" style="color: #64748B;">
                    Searching for the deeper meaning, the underlying truth of things, has been a lifelong pursuit. 
                    Studying Christian Science as a youth, I found rich answers to deep questions about life.
                </p>
                <p class="text-lg leading-relaxed" style="color: #64748B;">
                    I began to confirm my belief that what we see and hear with our physical senses, does not 
                    always lead us to the truth nor to health and happiness!
                </p>
            </div>
        </div>
        
        <!-- Key Moment Story -->
        <div class="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 rounded-3xl p-10 mb-16 shadow-soft hover-lift fade-up relative overflow-hidden" style="--fade-delay: 160ms;">
            <div class="soft-shape soft-shape--gold" style="top:-120px; right:-140px; opacity:0.2;"></div>
            <div class="flex items-start gap-6">
                <div class="flex-shrink-0">
                    <div class="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                </div>
                <div>
                    <h3 class="text-3xl font-bold mb-4 leading-tight" style="color: #1E293B;">The Moment That Changed Everything</h3>
                    <p class="text-xl leading-relaxed mb-4" style="color: #64748B;">
                        As a young girl I witnessed my grandmother <strong>recover completely and rapidly from a car accident</strong>, 
                        that doctors warned she would never recover from, through her reliance on God.
                    </p>
                    <p class="text-lg leading-relaxed" style="color: #64748B;">
                        I realized that what we often perceive as inevitable limitations or challenges, are unknown to God 
                        and have no bearing on our true nature or our permanent health as spiritual beings.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- What I Learned -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            <div class="rounded-2xl p-8 shadow-lg" style="background-color: #FDFDFB; border-left: 4px solid #6B9A8B;">
                <div class="w-14 h-14 rounded-lg flex items-center justify-center mb-4" style="background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 100%);">
                    <svg class="w-7 h-7" style="color: #6B9A8B;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold mb-3" style="color: #1E293B;">Nothing Is Too Difficult</h3>
                <p class="leading-relaxed" style="color: #64748B;">
                    There isn't anything too difficult to overcome, no matter what the physical picture presents. 
                    God, this all-loving, all-intelligent presence, undergirds me and everyone.
                </p>
            </div>
            
            <div class="rounded-2xl p-8 shadow-lg" style="background-color: #FDFDFB; border-left: 4px solid #87A08B;">
                <div class="w-14 h-14 rounded-lg flex items-center justify-center mb-4" style="background: linear-gradient(135deg, #9FD8CE 0%, #A8D0DB 100%);">
                    <svg class="w-7 h-7" style="color: #87A08B;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold mb-3" style="color: #1E293B;">Permanent Well-Being</h3>
                <p class="leading-relaxed" style="color: #64748B;">
                    Learning more about God introduced me to an all-loving, all-intelligent and ever present Spirit 
                    that leads us to discover our greatest potential and understand our permanent well-being.
                </p>
            </div>
        </div>
        
        <!-- My Work Today -->
        <div class="rounded-2xl p-10 mb-16 shadow-soft hover-lift fade-up relative overflow-hidden" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%); --fade-delay: 240ms;">
            <div class="soft-shape soft-shape--teal" style="top:-120px; left:-140px; opacity:0.2;"></div>
            <div class="max-w-4xl mx-auto">
                <h2 class="text-3xl font-bold mb-4" style="color: #1E293B;">My Work Today</h2>
                <p class="text-lg leading-relaxed mb-6" style="color: #64748B;">
                    As a Christian Science Practitioner, I work with people from all over the world and from every 
                    walk of life, to find permanent solutions to any type of challenge – including illness, 
                    mental health, career concerns or marital conflicts.
                </p>
                <div class="border-l-4 pl-6 rounded-r-lg py-4 pr-6" style="background-color: #FDFDFB; border-color: #6B9A8B;">
                    <p class="text-lg italic" style="color: #64748B;">
                        "Lifting our thought to see beyond the surface of things to understand what God sees and knows, 
                        we always find truth and healing."
                    </p>
                </div>
            </div>
        </div>
        
        <!-- About Christian Science Practitioners -->
        <div class="rounded-2xl p-10 shadow-lg" style="background-color: #FDFDFB; border-top: 4px solid #9FD8CE;">
            <div class="max-w-4xl mx-auto">
                <div class="flex items-start gap-6 mb-6">
                    <div class="flex-shrink-0">
                        <div class="w-14 h-14 rounded-lg flex items-center justify-center animate-soft-float" style="background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 100%);">
                            <svg class="w-7 h-7" style="color: #9FD8CE;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                            </svg>
                        </div>
                    </div>
                    <div>
                        <h2 class="text-3xl font-bold mb-4 leading-tight" style="color: #1E293B;">About Christian Science Practitioners</h2>
                        <p class="text-lg leading-relaxed mb-4" style="color: #64748B;">
                            Christian Science Practitioners are dedicated professionals who work full time to help and pray 
                            for those who are seeking healing. While much of their work is done over the phone or via email, 
                            it is sometimes helpful to have an office visit with a practitioner in person.
                        </p>
                        <p class="text-lg leading-relaxed mb-4" style="color: #64748B;">
                            I have had a full time practice as a Christian Science practitioner for over 20 years and am 
                            happy to answer any questions you have or to pray for you and help you find permanent healing.
                        </p>
                        <div class="border-l-4 p-6 rounded-r-lg mb-6" style="background-color: #F0F7F4; border-color: #6B9A8B;">
                            <p class="mb-3" style="color: #64748B;">
                                <svg class="w-5 h-5 inline-block mr-2" style="color: #6B9A8B;" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                                </svg>
                                <strong>Learn More:</strong> 
                                <a href="https://www.christianscience.com/christian-healing-today/christian-science-practitioners" 
                                   target="_blank" 
                                   rel="noopener noreferrer" 
                                   class="text-purple-600 hover:text-purple-800 font-semibold underline">
                                   Visit this website
                                </a> to access a global listing of Christian Science Practitioners and a complete 
                                description of the scope of services they provide.
                            </p>
                        </div>
                        <div class="flex flex-col sm:flex-row gap-4">
                            <a href="contact.html" class="inline-flex items-center justify-center bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-all shadow-md">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                </svg>
                                Contact Me
                            </a>
                            <a href="services.html" class="inline-flex items-center justify-center bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-purple-50 transition-all shadow-md border-2 border-purple-600">
                                Learn About My Services
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''


def create_services_page_content():
    """Create custom Services page layout."""
    return '''
    <div id="main-content" class="max-w-6xl mx-auto">
        <!-- Introduction -->
        <div class="relative rounded-3xl p-10 mb-16 shadow-soft text-center hover-lift fade-up overflow-hidden" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%); --fade-delay: 60ms;">
            <div class="soft-shape soft-shape--mint animate-soft-float" style="top:-120px; right:-140px; opacity:0.3;"></div>
            <div class="soft-shape soft-shape--teal" style="bottom:-150px; left:-160px; opacity:0.25;"></div>
            <div class="relative">
                <h2 class="text-4xl font-bold mb-4 leading-tight" style="color: #1E293B;">Prayer-Based Healing Treatment</h2>
                <p class="text-xl leading-relaxed max-w-4xl mx-auto" style="color: #64748B;">
                    Christian Science treatment can be provided to any patient seeking healing from any challenge including 
                    <strong style="color: #1E293B;">illness, mental health, relationship or employment concerns</strong>. This is a specific, inspired, 
                    prayer-based treatment rooted in an understanding of God's all-loving and permanent relationship to man.
                </p>
            </div>
        </div>
        
        <!-- What's Included -->
        <h2 class="text-4xl font-bold mb-10 text-center leading-tight" style="color: #1E293B;">What's Included</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            <!-- Treatment -->
            <div class="rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all" style="background-color: #FDFDFB; border-top: 4px solid #6B9A8B;">
                <div class="w-16 h-16 rounded-xl flex items-center justify-center mb-4 shadow-lg" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%);">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold mb-3" style="color: #1E293B;">Healing Treatment</h3>
                <p class="leading-relaxed mb-4" style="color: #64748B;">
                    Specific, inspired prayer-based treatment that directly addresses your needs and brings healing. 
                    Begins with the premise of your inherent wholeness and continues through to permanent healing.
                </p>
                <ul class="space-y-2" style="color: #64748B;">
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #6B9A8B;">✓</span>Phone sessions</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #6B9A8B;">✓</span>Email support</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #6B9A8B;">✓</span>Continuous prayer</li>
                </ul>
            </div>
            
            <!-- Consultation -->
            <div class="rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all" style="background-color: #FDFDFB; border-top: 4px solid #87A08B;">
                <div class="w-16 h-16 rounded-xl flex items-center justify-center mb-4 shadow-lg" style="background: linear-gradient(135deg, #87A08B 0%, #9FD8CE 100%);">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold mb-3" style="color: #1E293B;">Consultation & Guidance</h3>
                <p class="leading-relaxed mb-4" style="color: #64748B;">
                    Sometimes it's helpful to consult with a practitioner to answer questions or provide guidance 
                    as you dive deeper into your spiritual study.
                </p>
                <ul class="space-y-2" style="color: #64748B;">
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #87A08B;">✓</span>Q&A sessions</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #87A08B;">✓</span>Spiritual guidance</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #87A08B;">✓</span>Study support</li>
                </ul>
            </div>
            
            <!-- Office Visits -->
            <div class="rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all" style="background-color: #FDFDFB; border-top: 4px solid #9FD8CE;">
                <div class="w-16 h-16 rounded-xl flex items-center justify-center mb-4 shadow-lg" style="background: linear-gradient(135deg, #9FD8CE 0%, #A8D0DB 100%);">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold mb-3 leading-tight" style="color: #1E293B;">Office or Home Visits</h3>
                <p class="leading-relaxed mb-4" style="color: #64748B;">
                    While treatment doesn't depend on proximity, sometimes an in-person visit is desired to spend 
                    more time working together and understanding spiritual truths.
                </p>
                <ul class="space-y-2" style="color: #64748B;">
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #9FD8CE;">✓</span>Office appointments</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #9FD8CE;">✓</span>Home visits available</li>
                    <li class="flex items-start"><span class="mr-2 font-semibold" style="color: #9FD8CE;">✓</span>Care facility visits</li>
                </ul>
            </div>
        </div>
        
        <!-- How It Works Process -->
        ''' + create_how_it_works() + '''
        
        <!-- Key Benefits -->
        <div class="rounded-3xl p-12 text-white mb-16 shadow-2xl" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%);">
            <h2 class="text-4xl font-bold mb-8 text-center leading-tight">Why Choose Christian Science Treatment?</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="flex items-start gap-4">
                    <div class="flex-shrink-0">
                        <svg class="w-8 h-8 text-white/80" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold mb-2">Non-Invasive</h3>
                        <p class="text-white/95">No drugs, physical therapy, or invasive procedures. Holistic, gentle, and natural.</p>
                    </div>
                </div>
                
                <div class="flex items-start gap-4">
                    <div class="flex-shrink-0">
                        <svg class="w-8 h-8 text-white/80" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold mb-2">Proven Track Record</h3>
                        <p class="text-white/95">Successfully practiced for over 150 years with thousands of published healing accounts.</p>
                    </div>
                </div>
                
                <div class="flex items-start gap-4">
                    <div class="flex-shrink-0">
                        <svg class="w-8 h-8 text-white/80" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold mb-2">Permanent Results</h3>
                        <p class="text-white/95">Not just symptom relief – treatment addresses root causes for lasting healing.</p>
                    </div>
                </div>
                
                <div class="flex items-start gap-4">
                    <div class="flex-shrink-0">
                        <svg class="w-8 h-8 text-white/80" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold mb-2">Confidential</h3>
                        <p class="text-white/95">Full respect and confidentiality of the patient/practitioner relationship.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Fees -->
        <div class="rounded-3xl p-10 shadow-soft fade-up" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%); --fade-delay: 220ms;">
            <div class="text-center mb-8">
                <h2 class="text-4xl font-bold mb-4 leading-tight" style="color: #1E293B;">Fees</h2>
                <p class="text-xl" style="color: #64748B;">Affordable, accessible healing for everyone</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                <div class="bg-white rounded-xl p-6 shadow-soft-sm hover-lift fade-up text-center" style="--fade-delay: 240ms;">
                    <div class="text-4xl mb-2">💵</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">Modest Fees</h3>
                    <p class="text-gray-600">Fairly priced to make healing accessible to all</p>
                </div>
                <div class="bg-white rounded-xl p-6 shadow-soft-sm hover-lift fade-up text-center" style="--fade-delay: 260ms;">
                    <div class="text-4xl mb-2">🏥</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">Insurance Coverage</h3>
                    <p class="text-gray-600">Many insurance plans cover Christian Science treatment</p>
                </div>
                <div class="bg-white rounded-xl p-6 shadow-soft-sm hover-lift fade-up text-center" style="--fade-delay: 280ms;">
                    <div class="text-4xl mb-2">🆓</div>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">Free Consultation</h3>
                    <p class="text-gray-600">No charge for introductory phone conference</p>
                </div>
            </div>
        </div>
        
        <!-- Simple Next Step -->
        <div class="soft-card hover-lift fade-up text-center" style="padding: 2rem; --fade-delay: 300ms;">
            <p class="text-lg mb-4" style="color: #64748B;">Questions about how Christian Science treatment can help you?</p>
            <a href="contact.html" class="font-semibold inline-flex items-center transition-colors duration-300 ease-in-out" style="color: #6B9A8B;">
                Get in touch →
            </a>
        </div>
    </div>
    '''


def create_spiritual_healing_page_content():
    """Create custom Spiritual Healing (How It Works) page layout."""
    return '''
    <div class="max-w-6xl mx-auto">
        <!-- Hero Introduction -->
        <div class="text-center mb-16">
            <div class="inline-block px-6 py-3 rounded-full mb-6" style="background-color: #F0F7F4;">
                <p class="font-bold" style="color: #6B9A8B;">Rooted in Biblical Teaching</p>
            </div>
            <h2 class="text-5xl font-bold mb-6 leading-tight" style="color: #1E293B;">Experience Permanent Healing</h2>
            <p class="text-2xl max-w-4xl mx-auto leading-relaxed" style="color: #64748B;">
                Christian Science has been successfully practiced as a non-invasive and effective preventative 
                and curative treatment for over a century.
            </p>
        </div>
        
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <div class="rounded-2xl p-8 text-center shadow-lg" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                <div class="text-5xl font-bold mb-2" style="color: #6B9A8B;">150+</div>
                <p class="text-xl font-semibold" style="color: #64748B;">Years of Practice</p>
            </div>
            <div class="rounded-2xl p-8 text-center shadow-lg" style="background: linear-gradient(135deg, #F5FAF8 0%, #F8FCFA 100%);">
                <div class="text-5xl font-bold mb-2" style="color: #87A08B;">1000s</div>
                <p class="text-xl font-semibold" style="color: #64748B;">Published Healings</p>
            </div>
            <div class="rounded-2xl p-8 text-center shadow-lg" style="background: linear-gradient(135deg, #F0F7F4 0%, #E2E8E6 100%);">
                <div class="text-5xl font-bold mb-2" style="color: #9FD8CE;">100%</div>
                <p class="text-xl font-semibold" style="color: #64748B;">Natural & Safe</p>
            </div>
        </div>
        
        <!-- How It Works -->
        <h2 class="text-4xl font-bold mb-10 text-center leading-tight" style="color: #1E293B;">What Happens in a Session</h2>
        <div class="space-y-8 mb-16">
            <div class="rounded-2xl p-8 shadow-lg" style="background-color: #FDFDFB; border-left: 4px solid #6B9A8B;">
                <div class="flex gap-6 items-start">
                    <div class="w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0 text-white text-2xl font-bold shadow-lg" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%);">1</div>
                    <div>
                        <h3 class="text-2xl font-bold mb-3 leading-tight" style="color: #1E293B;">Understanding Your Spiritual Nature</h3>
                        <p class="text-lg leading-relaxed" style="color: #64748B;">
                            Time and again, Jesus looked beyond the surface picture of things – from the gravest of illness 
                            to the deepest sin – to see mankind's innate and God-given beauty, health and goodness. We follow 
                            this same approach, seeing you as God's perfect creation.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="rounded-2xl p-8 shadow-lg" style="background-color: #FDFDFB; border-left: 4px solid #87A08B;">
                <div class="flex gap-6 items-start">
                    <div class="w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0 text-white text-2xl font-bold shadow-lg" style="background: linear-gradient(135deg, #87A08B 0%, #9FD8CE 100%);">2</div>
                    <div>
                        <h3 class="text-2xl font-bold mb-3 leading-tight" style="color: #1E293B;">Applying Divine Laws</h3>
                        <p class="text-lg leading-relaxed mb-3" style="color: #64748B;">
                            These healings are natural, repeatable and permanent because they are the result of divine, 
                            spiritual laws that govern all mankind. <em>Science and Health with Key to the Scriptures</em> by 
                            Mary Baker Eddy explains these divine laws and shows how to apply them.
                        </p>
                        <p class="text-lg leading-relaxed" style="color: #64748B;">
                            Gaining a deeper understanding of God and of man, as His image and likeness, brings about great 
                            and lasting changes in our lives.
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="rounded-2xl p-8 shadow-lg" style="background-color: #FDFDFB; border-left: 4px solid #9FD8CE;">
                <div class="flex gap-6 items-start">
                    <div class="w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0 text-white text-2xl font-bold shadow-lg" style="background: linear-gradient(135deg, #9FD8CE 0%, #A8D0DB 100%);">3</div>
                    <div>
                        <h3 class="text-2xl font-bold mb-3 leading-tight" style="color: #1E293B;">Experiencing Permanent Transformation</h3>
                        <p class="text-lg leading-relaxed" style="color: #64748B;">
                            Dropping a picture of mankind as material, limited, sinning or fragile, and seeing everyone as 
                            linked to God, good, like a ray of light to the sun – a change in the way we view ourselves can 
                            yield permanent healing transformation in every one of us.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- What Makes It Different -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            <div class="rounded-2xl p-8 shadow-lg" style="background: linear-gradient(135deg, #F0F7F4 0%, #F5FAF8 100%);">
                <h3 class="text-2xl font-bold mb-4 leading-tight" style="color: #1E293B;">Not Symptom Treatment</h3>
                <p class="text-lg leading-relaxed" style="color: #64748B;">
                    Rather than treating symptoms, Christian Science healing addresses the root spiritual understanding. 
                    This is why healings are permanent – we're not just covering up problems, we're transforming 
                    consciousness itself.
                </p>
            </div>
            
            <div class="rounded-2xl p-8 shadow-lg" style="background: linear-gradient(135deg, #F5FAF8 0%, #F8FCFA 100%);">
                <h3 class="text-2xl font-bold mb-4 leading-tight" style="color: #1E293B;">Available to Everyone</h3>
                <p class="text-lg leading-relaxed" style="color: #64748B;">
                    Jesus taught that anyone can do these works. You don't need special abilities or training – 
                    just a willingness to understand spiritual truth. A practitioner guides you through this 
                    understanding and prays specifically for your needs.
                </p>
            </div>
        </div>
        
        <!-- Biblical Foundation -->
        <div class="rounded-3xl p-12 text-white mb-16 shadow-2xl" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%);">
            <div class="flex items-center gap-6 mb-8">
                <div class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                </div>
                <div>
                    <h2 class="text-4xl font-bold mb-2">Rooted in Christ Jesus' Work</h2>
                    <p class="text-xl text-white/90">Following the healing ministry of Jesus</p>
                </div>
            </div>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 mb-6">
                <p class="text-2xl leading-relaxed mb-4">
                    This healing methodology is rooted and grounded in the Bible and draws on the life and work of Christ Jesus. 
                    Through his healing ministry, he proved that <strong>at any time and in any place, anyone can be readily 
                    and permanently healed</strong> by recognizing their true, spiritual nature as God's child.
                </p>
            </div>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <div class="flex items-start gap-4">
                    <svg class="w-8 h-8 text-white/60 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"></path>
                    </svg>
                    <p class="text-xl text-white italic">
                        "He that believes in me will do the works that I have been doing, and they will do even greater 
                        things than these..." <span class="text-blue-200 font-semibold">– John 14:12</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
    '''


def create_inspiration_page_content():
    """Create custom Inspiration/Resources page layout."""
    articles = [
        {
            "title": "How can we feel safe?", 
            "category": "Life Guidance", 
            "color": "indigo",
            "summary": "Addresses concerns about safety in schools and offers perspectives on finding relief from anxiety related to gun violence.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2023/0922/How-can-we-feel-safe"
        },
        {
            "title": "The porter", 
            "category": "Spiritual Growth", 
            "color": "purple",
            "summary": "Reflecting on an encounter with a hotel porter, this piece draws parallels between the role of a porter and spiritual guidance.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2023/0314/The-porter"
        },
        {
            "title": "All one with God", 
            "category": "Healing", 
            "color": "blue",
            "summary": "Personal experiences of overcoming loneliness by understanding unity with God.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2022/0906/All-one-with-God"
        },
        {
            "title": "Shielded from contagion during air travel", 
            "category": "Wellness", 
            "color": "teal",
            "summary": "Maintaining a sense of safety and health during air travel amidst concerns about contagion.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2020/0302/Shielded-from-contagion-during-air-travel"
        },
        {
            "title": "'Worrier-in-chief' of the family?", 
            "category": "Life Guidance", 
            "color": "indigo",
            "summary": "Explores the tendency to take on family worries and offers insights into finding peace through spiritual understanding.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2019/1209/Worrier-in-chief-of-the-family"
        },
        {
            "title": "The life that is eternal", 
            "category": "Spiritual Growth", 
            "color": "purple",
            "summary": "An expanded understanding of life as forever sustained by God comforts, heals, and uplifts.",
            "url": "https://www.csmonitor.com/Commentary/A-Christian-Science-Perspective/2022/0610/The-life-that-is-eternal"
        },
    ]
    
    cards_html = ""
    for article in articles:
        color = article['color']
        title = article['title']
        summary = article['summary']
        url = article['url']
        category = article['category']
        
        cards_html += f'''
        <a href="{url}" target="_blank" rel="noopener noreferrer" class="block bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all border-t-4 border-{color}-500 group transform hover:-translate-y-1">
            <div class="flex items-start justify-between mb-4">
                <span class="bg-{color}-100 text-{color}-700 px-3 py-1 rounded-full text-sm font-semibold">{category}</span>
                <svg class="w-6 h-6 text-gray-400 group-hover:text-{color}-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-{color}-600 transition-colors leading-tight">{title}</h3>
            <p class="text-gray-600 text-base mb-4 leading-relaxed">{summary}</p>
            <div class="text-{color}-600 hover:text-{color}-700 font-semibold inline-flex items-center group">
                Read Article
                <svg class="w-4 h-4 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
            </div>
        </a>
        '''
    
    # Audio/Podcast content
    podcasts = [
        {
            "title": "Easter and healing: The big picture",
            "url": "https://sentinel.christianscience.com/sentinel-audio/sentinel-watch/easter-and-healing-the-bigger-picture",
            "type": "Christian Science Sentinel"
        },
        {
            "title": "Peace during a time of economic turmoil",
            "url": "https://sentinel.christianscience.com/shared/view/pp8nmfid9c?s=e",
            "type": "Christian Science Sentinel"
        },
        {
            "title": "Look away from the body and find healing",
            "url": "https://sentinel.christianscience.com/sentinel-audio/sentinel-watch/look-away-from-the-body-and-find-healing",
            "type": "Christian Science Sentinel"
        },
        {
            "title": '"God with me" was my prayer',
            "url": "https://sentinel.christianscience.com/shared/view/14urzoqva5w?s=e",
            "type": "Christian Science Sentinel"
        },
    ]
    
    podcast_html = ""
    for podcast in podcasts:
        podcast_html += f'''
        <a href="{podcast['url']}" target="_blank" rel="noopener noreferrer" class="block bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all border-l-4 border-purple-500 group">
            <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"></path>
                    </svg>
                </div>
                <div class="flex-1">
                    <div class="text-purple-600 text-xs font-semibold uppercase tracking-wide mb-2">{podcast['type']}</div>
                    <h3 class="text-lg font-bold text-gray-900 mb-2 group-hover:text-purple-600 transition-colors">{podcast['title']}</h3>
                    <div class="text-purple-600 hover:text-purple-700 font-semibold inline-flex items-center text-sm">
                        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                        </svg>
                        Listen Now
                    </div>
                </div>
            </div>
        </a>
        '''
    
    # Daily Lift embedded audio section - with actual MP3 players
    daily_lift_html = '''
        <!-- Daily Lift Audio Embeds Section -->
        <div class="mb-20">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg" style="background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-3xl font-bold text-gray-900">Daily Lift</h3>
                    <p class="text-gray-600">Short audio messages for daily spiritual inspiration</p>
                </div>
            </div>
            
            <div class="space-y-6">
                <!-- Daily Lift 1: You are worthy of God's love -->
                <div class="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-6 shadow-lg border-l-4 border-teal-500">
                    <h4 class="text-lg font-bold text-gray-900 mb-4">You are worthy of God's love</h4>
                    <div class="audio-player-container">
                        <audio controls preload="metadata" class="w-full" style="height: 40px; max-width: 100%;">
                            <source src="https://www.susantish.com/wp-content/uploads/2022/12/daily-lift-221209-tishs.mp3?_=1" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                </div>
                
                <!-- Daily Lift 2 -->
                <div class="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-6 shadow-lg border-l-4 border-teal-500">
                    <h4 class="text-lg font-bold text-gray-900 mb-4">Daily Lift Audio Message</h4>
                    <div class="audio-player-container">
                        <audio controls preload="metadata" class="w-full" style="height: 40px; max-width: 100%;">
                            <source src="https://www.susantish.com/wp-content/uploads/2022/05/daily-lift-220307-tishs.mp3?_=2" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                </div>
                
                <!-- Daily Lift 3 -->
                <div class="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-6 shadow-lg border-l-4 border-teal-500">
                    <h4 class="text-lg font-bold text-gray-900 mb-4">Daily Lift Audio Message</h4>
                    <div class="audio-player-container">
                        <audio controls preload="metadata" class="w-full" style="height: 40px; max-width: 100%;">
                            <source src="https://www.susantish.com/wp-content/uploads/2020/03/daily-lift-200312-tishs.mp3?_=3" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                </div>
            </div>
        </div>
    '''
    
    return f'''
    <div id="main-content" class="max-w-7xl mx-auto">
        <!-- Hero -->
        <div class="text-center mb-16">
            <h2 class="text-5xl font-bold text-gray-900 mb-6">Inspiration & Resources</h2>
            <p class="text-2xl text-gray-700 max-w-3xl mx-auto leading-relaxed">
                Articles, audio messages, and guidance for your spiritual healing journey
            </p>
        </div>
        
        <!-- Podcasts Section -->
        <div class="mb-20">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-3xl font-bold text-gray-900">Podcasts</h3>
                    <p class="text-gray-600">Listen to spiritual insights and healing perspectives</p>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
                {podcast_html}
            </div>
        </div>
        
        {daily_lift_html}
        
        <!-- Articles Section -->
        <div class="mb-20">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-3xl font-bold text-gray-900">Articles</h3>
                    <p class="text-gray-600">Read thoughtful perspectives on healing and spiritual growth</p>
                </div>
            </div>
            
            <!-- Articles Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {cards_html}
            </div>
        </div>
        
        <!-- Science and Health Book Section (Small Card) -->
        <div class="mb-16">
            <div class="flex items-center gap-4 mb-8">
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg" style="background: linear-gradient(135deg, #eab308 0%, #f59e0b 100%);">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-3xl font-bold text-gray-900">Additional Resources</h3>
                    <p class="text-gray-600">Essential reading for spiritual healing</p>
                </div>
            </div>
            
            <!-- Book Card -->
            <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow overflow-hidden max-w-2xl">
                <div class="flex flex-col sm:flex-row">
                    <!-- Book Image -->
                    <div class="sm:w-48 flex-shrink-0 bg-gradient-to-br from-blue-50 to-indigo-50 p-6 flex items-center justify-center">
                        <img src="science-health-book.png" 
                             alt="Science and Health with Key to the Scriptures" 
                             loading="lazy"
                             class="w-full max-w-[180px] rounded-lg shadow-lg">
                    </div>
                    <!-- Book Info -->
                    <div class="p-6 flex-1">
                        <div class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full mb-3">
                            Essential Reading
                        </div>
                        <h4 class="text-xl font-bold text-gray-900 mb-2">Science and Health with Key to the Scriptures</h4>
                        <p class="text-sm text-gray-600 mb-1 font-medium">by Mary Baker Eddy</p>
                        <p class="text-gray-700 mb-4 leading-relaxed">
                            The foundational textbook of Christian Science, offering profound insights into spiritual healing and the practice of Christian Science treatment.
                        </p>
                        <a href="https://www.christianscience.com/the-christian-science-pastor/science-and-health" 
                           target="_blank" 
                           rel="noopener noreferrer" 
                           class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium transition-colors">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                            </svg>
                            Read Online
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''


def create_pricing_page_content():
    """Create Services & Pricing page with Stripe payment buttons."""
    return '''
    <div class="max-w-6xl mx-auto">
        <!-- Introduction -->
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-10 mb-16 shadow-lg text-center">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Services & Pricing</h2>
            <p class="text-xl text-gray-700 leading-relaxed max-w-4xl mx-auto">
                Choose the service that best fits your needs. All services are provided remotely via phone, email, or Skype. 
                Payment is secure and processed through Stripe.
            </p>
        </div>
        
        <!-- Pricing Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            <!-- Free Consultation -->
            <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-gray-200">
                <div class="text-center mb-6">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-2">Free Consultation</h3>
                    <div class="text-4xl font-bold text-blue-600 mb-1">$0</div>
                    <p class="text-gray-600 text-sm">15 minutes</p>
                </div>
                <ul class="space-y-3 mb-6 text-gray-700">
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Get to know each other</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Discuss your needs</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>See if we're a good fit</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>No obligation</span>
                    </li>
                </ul>
                <a href="booking.html" 
                   class="block w-full bg-blue-600 text-white text-center px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md">
                    Book Free Consultation
                </a>
            </div>
            
            <!-- Initial Treatment Session -->
            <div class="bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all border-2 border-blue-500 relative">
                <div class="absolute top-0 right-0 bg-yellow-400 text-blue-900 px-4 py-1 rounded-bl-lg rounded-tr-2xl font-bold text-sm">
                    MOST POPULAR
                </div>
                <div class="text-center mb-6 mt-4">
                    <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-2">Initial Treatment Session</h3>
                    <div class="text-4xl font-bold text-white mb-1">$XXX</div>
                    <p class="text-white/90 text-sm">60-90 minutes</p>
                </div>
                <ul class="space-y-3 mb-6 text-white/95">
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>In-depth discussion of your needs</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Prayer-based treatment begins</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Ongoing prayer treatment</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Email support between sessions</span>
                    </li>
                </ul>
                <button id="stripe-payment-initial" 
                        class="block w-full bg-white text-blue-600 text-center px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="initial-btn-text">Pay $XXX - Initial Session</span>
                    <span id="initial-btn-loading" class="hidden">Processing...</span>
                </button>
                <p class="text-white/80 text-xs text-center mt-3">Stripe payment link required</p>
            </div>
            
            <!-- Follow-up Session -->
            <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-gray-200">
                <div class="text-center mb-6">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-900 mb-2">Follow-up Session</h3>
                    <div class="text-4xl font-bold text-indigo-600 mb-1">$XXX</div>
                    <p class="text-gray-600 text-sm">30-45 minutes</p>
                </div>
                <ul class="space-y-3 mb-6 text-gray-700">
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Progress check-in</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Continued prayer treatment</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Address new concerns</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-indigo-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Ongoing support</span>
                    </li>
                </ul>
                <button id="stripe-payment-followup" 
                        class="block w-full bg-indigo-600 text-white text-center px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="followup-btn-text">Pay $XXX - Follow-up</span>
                    <span id="followup-btn-loading" class="hidden">Processing...</span>
                </button>
                <p class="text-gray-500 text-xs text-center mt-3">Stripe payment link required</p>
            </div>
        </div>
        
        <!-- Additional Services -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            <!-- Monthly Support Package -->
            <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 shadow-lg border-2 border-purple-200">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">Monthly Support Package</h3>
                        <div class="text-3xl font-bold text-purple-600 mb-1">$XXX</div>
                        <p class="text-gray-600 text-sm">per month</p>
                    </div>
                    <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                </div>
                <p class="text-gray-700 mb-4 leading-relaxed">
                    Ongoing monthly support with regular check-ins and continuous prayer treatment. Ideal for long-term healing work.
                </p>
                <ul class="space-y-2 mb-6 text-gray-700">
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-purple-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Monthly check-in sessions</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-purple-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Continuous prayer treatment</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-purple-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Priority email support</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-purple-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Cancel anytime</span>
                    </li>
                </ul>
                <button id="stripe-payment-monthly" 
                        class="block w-full bg-purple-600 text-white text-center px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="monthly-btn-text">Subscribe $XXX/month</span>
                    <span id="monthly-btn-loading" class="hidden">Processing...</span>
                </button>
                <p class="text-gray-500 text-xs text-center mt-3">Stripe subscription link required</p>
            </div>
            
            <!-- Emergency Session -->
            <div class="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-8 shadow-lg border-2 border-red-200">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">Emergency Session</h3>
                        <div class="text-3xl font-bold text-red-600 mb-1">$XXX</div>
                        <p class="text-gray-600 text-sm">Available 24/7</p>
                    </div>
                    <div class="w-12 h-12 bg-gradient-to-br from-red-500 to-orange-500 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                    </div>
                </div>
                <p class="text-gray-700 mb-4 leading-relaxed">
                    Immediate prayer treatment for urgent situations. Available around the clock for critical needs.
                </p>
                <ul class="space-y-2 mb-6 text-gray-700">
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-red-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Immediate response</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-red-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>24/7 availability</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-red-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Priority prayer treatment</span>
                    </li>
                    <li class="flex items-start">
                        <svg class="w-5 h-5 text-red-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span>Phone or video call</span>
                    </li>
                </ul>
                <button id="stripe-payment-emergency" 
                        class="block w-full bg-red-600 text-white text-center px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="emergency-btn-text">Pay $XXX - Emergency</span>
                    <span id="emergency-btn-loading" class="hidden">Processing...</span>
                </button>
                <p class="text-gray-500 text-xs text-center mt-3">Stripe payment link required</p>
            </div>
        </div>
        
        <!-- Setup Instructions -->
        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg mb-12">
            <div class="flex items-start">
                <svg class="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
                <div>
                    <h3 class="text-lg font-bold text-yellow-900 mb-2">📋 Stripe Setup Required</h3>
                    <p class="text-yellow-800 mb-3">
                        <strong>To activate payment buttons, you need to:</strong>
                    </p>
                    <ol class="list-decimal list-inside space-y-2 text-yellow-800 mb-3">
                        <li>Create a Stripe account at <a href="https://stripe.com" target="_blank" class="underline font-semibold">stripe.com</a></li>
                        <li>Go to Products → Payment Links</li>
                        <li>Create payment links for each service (Initial Session, Follow-up, Monthly, Emergency)</li>
                        <li>Copy each payment link URL</li>
                        <li>Update the code in <code class="bg-yellow-100 px-2 py-1 rounded">generate_website_v5.py</code> (see STRIPE_SETUP_INSTRUCTIONS.md)</li>
                        <li>Replace <code class="bg-yellow-100 px-2 py-1 rounded">$XXX</code> with actual prices</li>
                        <li>Regenerate the website</li>
                    </ol>
                    <p class="text-sm text-yellow-700 italic">
                        💡 See <strong>STRIPE_SETUP_INSTRUCTIONS.md</strong> in your project folder for detailed steps.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- Payment Security Info -->
        <div class="bg-blue-50 rounded-2xl p-8 mb-12">
            <div class="flex items-start gap-4">
                <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3">Secure Payment Processing</h3>
                    <p class="text-gray-700 leading-relaxed mb-3">
                        All payments are processed securely through Stripe, a trusted payment processor used by millions of businesses worldwide. 
                        Your payment information is encrypted and never stored on our servers.
                    </p>
                    <ul class="space-y-2 text-gray-700">
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span><strong>PCI DSS Compliant</strong> - Highest level of payment security</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span><strong>Encrypted</strong> - All data transmitted securely</span>
                        </li>
                        <li class="flex items-start">
                            <svg class="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span><strong>Automatic Receipts</strong> - Email confirmation for every payment</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Contact for Questions -->
        <div class="bg-gray-50 rounded-2xl p-8 text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Questions About Pricing?</h3>
            <p class="text-gray-700 mb-6">I'm happy to discuss payment options that work for your situation</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="mailto:susantishcs@gmail.com" 
                   class="inline-flex items-center justify-center bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    Email Me
                </a>
                <a href="tel:734-693-5946" 
                   class="inline-flex items-center justify-center bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-all shadow-md">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                    Call Me
                </a>
            </div>
        </div>
    </div>
    
    <script>
    // Stripe Payment Link Integration
    // Replace these URLs with your actual Stripe payment links after setup
    const stripePaymentLinks = {{
        initial: 'https://buy.stripe.com/YOUR_INITIAL_SESSION_LINK',
        followup: 'https://buy.stripe.com/YOUR_FOLLOWUP_SESSION_LINK',
        monthly: 'https://buy.stripe.com/YOUR_MONTHLY_SUBSCRIPTION_LINK',
        emergency: 'https://buy.stripe.com/YOUR_EMERGENCY_SESSION_LINK'
    }};
    
    // Payment button handlers
    document.addEventListener('DOMContentLoaded', function() {{
        // Initial Session
        const initialBtn = document.getElementById('stripe-payment-initial');
        if (initialBtn && stripePaymentLinks.initial && !stripePaymentLinks.initial.includes('YOUR_')) {{
            initialBtn.addEventListener('click', function() {{
                window.location.href = stripePaymentLinks.initial;
            }});
        }} else {{
            initialBtn.disabled = true;
        }}
        
        // Follow-up Session
        const followupBtn = document.getElementById('stripe-payment-followup');
        if (followupBtn && stripePaymentLinks.followup && !stripePaymentLinks.followup.includes('YOUR_')) {{
            followupBtn.addEventListener('click', function() {{
                window.location.href = stripePaymentLinks.followup;
            }});
        }} else {{
            followupBtn.disabled = true;
        }}
        
        // Monthly Subscription
        const monthlyBtn = document.getElementById('stripe-payment-monthly');
        if (monthlyBtn && stripePaymentLinks.monthly && !stripePaymentLinks.monthly.includes('YOUR_')) {{
            monthlyBtn.addEventListener('click', function() {{
                window.location.href = stripePaymentLinks.monthly;
            }});
        }} else {{
            monthlyBtn.disabled = true;
        }}
        
        // Emergency Session
        const emergencyBtn = document.getElementById('stripe-payment-emergency');
        if (emergencyBtn && stripePaymentLinks.emergency && !stripePaymentLinks.emergency.includes('YOUR_')) {{
            emergencyBtn.addEventListener('click', function() {{
                window.location.href = stripePaymentLinks.emergency;
            }});
        }} else {{
            emergencyBtn.disabled = true;
        }}
    }});
    </script>
    '''


def create_booking_page_content():
    """Create dedicated Calendly booking page."""
    return '''
    <div class="max-w-5xl mx-auto">
        <!-- Introduction -->
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-10 mb-12 shadow-lg text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
            </div>
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Schedule Your Free Consultation</h2>
            <p class="text-xl text-gray-700 leading-relaxed max-w-3xl mx-auto">
                Choose a time that works best for you. I offer a complimentary 15-minute consultation 
                to discuss how Christian Science treatment can help with your specific needs.
            </p>
        </div>
        
        <!-- What to Expect -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div class="bg-white rounded-xl p-6 shadow-md text-center">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">15-Minute Free Call</h3>
                <p class="text-gray-600">Get to know each other and discuss your needs</p>
            </div>
            
            <div class="bg-white rounded-xl p-6 shadow-md text-center">
                <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">Phone, Email, or Skype</h3>
                <p class="text-gray-600">Sessions available remotely from anywhere</p>
            </div>
            
            <div class="bg-white rounded-xl p-6 shadow-md text-center">
                <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">No Obligation</h3>
                <p class="text-gray-600">See if we're a good fit with no commitment</p>
            </div>
        </div>
        
        <!-- Calendly Embed Widget Begin -->
        <div class="bg-white rounded-2xl shadow-xl p-8 mb-12">
            <div class="calendly-inline-widget" 
                 data-url="https://calendly.com/YOUR_CALENDLY_USERNAME?hide_gdpr_banner=1&primary_color=2563eb" 
                 style="min-width:320px;height:700px;">
            </div>
            <script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
        </div>
        
        <!-- Setup Notice (Remove after Calendly is configured) -->
        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg mb-12">
            <div class="flex items-start">
                <svg class="w-6 h-6 text-yellow-600 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
                <div>
                    <h3 class="text-lg font-bold text-yellow-900 mb-2">📋 Setup Required</h3>
                    <p class="text-yellow-800 mb-3">
                        <strong>To activate the booking calendar, you need to:</strong>
                    </p>
                    <ol class="list-decimal list-inside space-y-2 text-yellow-800 mb-3">
                        <li>Create a free account at <a href="https://calendly.com" target="_blank" class="underline font-semibold">calendly.com</a></li>
                        <li>Set up your availability and appointment types</li>
                        <li>Get your Calendly link (looks like: <code class="bg-yellow-100 px-2 py-1 rounded">https://calendly.com/your-username</code>)</li>
                        <li>Replace <code class="bg-yellow-100 px-2 py-1 rounded">YOUR_CALENDLY_USERNAME</code> in the code with your actual username</li>
                        <li>Regenerate the website</li>
                    </ol>
                    <p class="text-sm text-yellow-700 italic">
                        💡 See <strong>CALENDLY_SETUP_INSTRUCTIONS.md</strong> in your project folder for detailed steps.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- Alternative Contact Methods -->
        <div class="bg-gray-50 rounded-2xl p-8 text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Prefer to Reach Out Directly?</h3>
            <p class="text-gray-700 mb-6">Feel free to contact me via email or phone</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="mailto:susantishcs@gmail.com" 
                   class="inline-flex items-center justify-center bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    Email Me
                </a>
                <a href="tel:734-693-5946" 
                   class="inline-flex items-center justify-center bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-all shadow-md">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                    Call Me
                </a>
            </div>
        </div>
    </div>
    '''


def create_page_template(page, pages, all_pages):
    """Create conversion-optimized HTML page."""
    slug = get_page_slug(page['url'])
    title = page['title']
    content = page.get('content', '')
    summary = clean_summary(page.get('summary', ''))
    
    is_home = slug == 'home'
    is_contact = slug == 'contact'
    is_services = slug == 'services'
    is_about = slug == 'about'
    is_spiritual_healing = slug == 'spiritual-healing'
    is_inspiration = slug == 'inspiration'
    is_booking = slug == 'booking'
    
    meta_description = clean_summary(summary[:160] if summary else title)
    
    # Homepage special sections
    homepage_hero = create_conversion_hero() if is_home else ''
    what_i_help_with = create_what_i_help_with() if is_home else ''
    # testimonials = create_testimonials() if is_home else ''  # Temporarily removed - can be restored later
    testimonials = ''  # Disabled for now
    
    # Custom page content
    about_content = create_about_page_content() if is_about else ''
    services_content = create_services_page_content() if is_services else ''
    spiritual_healing_content = create_spiritual_healing_page_content() if is_spiritual_healing else ''
    inspiration_content = create_inspiration_page_content() if is_inspiration else ''
    contact_content = create_contact_section() if is_contact else ''
    booking_content = create_booking_page_content() if is_booking else ''
    
    # Main content - use custom layouts or fallback to generic
    main_content = ''
    if is_about:
        main_content = about_content
    elif is_services:
        main_content = services_content
    elif is_spiritual_healing:
        main_content = spiritual_healing_content
    elif is_inspiration:
        main_content = inspiration_content
    elif is_booking:
        main_content = booking_content
    elif not is_home and not is_contact and content:
        # Fallback for any other pages
        main_content = f'''
        <div class="max-w-5xl mx-auto">
            {f'<div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 mb-12 shadow-md"><p class="text-2xl text-gray-800 leading-relaxed font-medium text-center">{summary}</p></div>' if summary else ''}
            {create_visual_content_sections(content)}
        </div>
        '''
    
    # CTA section - removed for more subtle approach
    cta_section = ''
    
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    
    <!-- SEO Meta Tags -->
    <meta name="author" content="Susan Tish">
    <meta name="keywords" content="Christian Science Practitioner, spiritual healing, prayer healing, Christian Science treatment, Susan Tish">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://www.susantish.com/{slug if slug != 'home' else ''}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.susantish.com/{slug if slug != 'home' else ''}">
    <meta property="og:title" content="{title.split('|')[0].strip()}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="https://www.susantish.com/susan-tish.jpg">
    <meta property="og:site_name" content="Susan Tish - Christian Science Practitioner">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://www.susantish.com/{slug if slug != 'home' else ''}">
    <meta name="twitter:title" content="{title.split('|')[0].strip()}">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="https://www.susantish.com/susan-tish.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    
    <!-- Compiled Tailwind CSS (production) -->
    <link rel="stylesheet" href="styles.css">
    <!-- Fallback to CDN if compiled CSS is not available -->
    <script>
        // Check if styles.css loaded successfully
        const checkStylesheet = () => {{
            const hasStyles = Array.from(document.styleSheets).some(sheet => {{
                try {{ return sheet.href && sheet.href.includes('styles.css'); }} 
                catch(e) {{ return false; }}
            }});
            if (!hasStyles) {{
                const script = document.createElement('script');
                script.src = 'https://cdn.tailwindcss.com';
                document.head.appendChild(script);
            }}
        }};
        window.addEventListener('load', checkStylesheet);
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Warm, welcoming typography and color system */
        :root {{
            --warm-bg: #FAFAF7;
            --warm-cream: #FDFDFB;
            --sage-green: #87A08B;
            --mint-green: #B8D4C1;
            --seafoam: #9FD8CE;
            --dusty-teal: #6B9A8B;
            --sky-blue: #A8D0DB;
            --sunlit-gold: #F5D7A3;
            --text-dark: #1E293B;
            --text-medium: #334155;
            --text-light: #64748B;
        }}
        body {{
            background-color: var(--warm-bg);
            color: var(--text-dark);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.7;
            letter-spacing: -0.01em;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'EB Garamond', Georgia, serif;
            font-weight: 600;
            line-height: 1.3;
            letter-spacing: -0.02em;
            color: var(--text-dark);
        }}
        .warm-gradient {{
            background: linear-gradient(135deg, #B8D4C1 0%, #9FD8CE 50%, #A8D0DB 100%);
        }}
        .sage-gradient {{
            background: linear-gradient(135deg, #87A08B 0%, #6B9A8B 100%);
        }}
        .shadow-soft {{
            box-shadow: 0 18px 40px rgba(107, 154, 139, 0.12), 0 6px 16px rgba(107, 154, 139, 0.08);
        }}
        .shadow-soft-sm {{
            box-shadow: 0 12px 28px rgba(107, 154, 139, 0.1), 0 4px 12px rgba(107, 154, 139, 0.06);
        }}
        .hover-lift {{
            transition: transform 500ms ease, box-shadow 500ms ease;
        }}
        .hover-lift:hover {{
            transform: translateY(-6px);
            box-shadow: 0 22px 45px rgba(107, 154, 139, 0.18), 0 10px 30px rgba(107, 154, 139, 0.12);
        }}
        .soft-section {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #F0F7F4 0%, #F8FCFA 100%);
        }}
        .soft-section::before {{
            content: "";
            position: absolute;
            inset: -40% -10% auto -10%;
            height: 80%;
            background: radial-gradient(circle at top left, rgba(135, 160, 139, 0.18), rgba(135, 160, 139, 0));
            opacity: 0.4;
            pointer-events: none;
        }}
        .soft-section::after {{
            content: "";
            position: absolute;
            inset: auto -10% -40% -10%;
            height: 80%;
            background: radial-gradient(circle at bottom right, rgba(159, 216, 206, 0.18), rgba(159, 216, 206, 0));
            opacity: 0.4;
            pointer-events: none;
        }}
        .soft-card {{
            background-color: var(--warm-cream);
            border-radius: 1.5rem;
            box-shadow: 0 16px 32px rgba(107, 154, 139, 0.12), 0 8px 22px rgba(107, 154, 139, 0.08);
            position: relative;
        }}
        .soft-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: linear-gradient(135deg, rgba(255,255,255,0.6), rgba(255,255,255,0));
            opacity: 0.7;
            pointer-events: none;
        }}
        .soft-shape {{
            position: absolute;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            opacity: 0.35;
            filter: blur(0px);
            pointer-events: none;
        }}
        .soft-shape--teal {{
            background: radial-gradient(circle, rgba(135, 160, 139, 0.22), rgba(135, 160, 139, 0));
        }}
        .soft-shape--mint {{
            background: radial-gradient(circle, rgba(159, 216, 206, 0.2), rgba(159, 216, 206, 0));
        }}
        .soft-shape--gold {{
            background: radial-gradient(circle, rgba(245, 215, 163, 0.16), rgba(245, 215, 163, 0));
        }}
        .shape-divider {{
            position: absolute;
            width: 100%;
            overflow: hidden;
            line-height: 0;
            pointer-events: none;
        }}
        .shape-divider svg {{
            display: block;
            width: calc(100% + 1.3px);
            height: 80px;
        }}
        .shape-divider path {{
            fill: currentColor;
        }}
        .shape-divider-top {{
            top: -1px;
        }}
        .shape-divider-bottom {{
            bottom: -1px;
            transform: rotate(180deg);
        }}
        .animate-soft-float {{
            animation: float-soft 7s ease-in-out infinite;
        }}
        .fade-up {{
            opacity: 0;
            transform: translateY(16px);
            animation: fade-up 900ms ease-out forwards;
            animation-delay: var(--fade-delay, 120ms);
        }}
        .glass-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.78), rgba(255, 255, 255, 0.58));
            backdrop-filter: blur(18px);
            border-radius: 1.5rem;
            box-shadow: 0 12px 32px rgba(107, 154, 139, 0.16);
        }}
        .bg-texture-soft {{
            background-image: radial-gradient(rgba(135, 160, 139, 0.12) 1px, transparent 1px);
            background-size: 60px 60px;
        }}
        .button-soft {{
            background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%);
            box-shadow: 0 14px 30px rgba(107, 154, 139, 0.18);
            transition: transform 350ms ease, box-shadow 350ms ease;
        }}
        .button-soft:hover {{
            transform: translateY(-2px);
            box-shadow: 0 18px 36px rgba(107, 154, 139, 0.22);
        }}
        @keyframes float-soft {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-6px); }}
        }}
        @keyframes fade-up {{
            0% {{ opacity: 0; transform: translateY(16px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .animate-soft-float {{
                animation: none !important;
            }}
            .fade-up {{
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }}
            .hover-lift:hover,
            .button-soft:hover {{
                transform: none !important;
                box-shadow: inherit;
            }}
        }}
    </style>
    
    <!-- Structured Data (Schema.org) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Susan Tish",
        "jobTitle": "Christian Science Practitioner",
        "url": "https://www.susantish.com",
        "image": "https://www.susantish.com/susan-tish.jpg",
        "email": "susantishcs@gmail.com",
        "telephone": "+1-734-693-5946",
        "address": {{
            "@type": "PostalAddress",
            "addressCountry": "US"
        }},
        "description": "Christian Science Practitioner with over 20 years of experience providing spiritual healing services worldwide through prayer-based treatment.",
        "knowsAbout": ["Christian Science", "Spiritual Healing", "Prayer-Based Treatment", "Mental Health", "Physical Healing"],
        "alumniOf": "Christian Science Practice",
        "yearsOfExperience": "20+"
    }}
    </script>
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Susan Tish - Christian Science Practitioner",
        "image": "https://www.susantish.com/susan-tish.jpg",
        "logo": "https://www.susantish.com/susantish-logo.png",
        "@id": "https://www.susantish.com",
        "url": "https://www.susantish.com",
        "telephone": "+1-734-693-5946",
        "email": "susantishcs@gmail.com",
        "priceRange": "$$",
        "address": {{
            "@type": "PostalAddress",
            "addressCountry": "US"
        }},
        "geo": {{
            "@type": "GeoCoordinates",
            "addressCountry": "US"
        }},
        "openingHoursSpecification": {{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        }},
        "sameAs": [
            "https://www.christianscience.com"
        ]
    }}
    </script>
</head>
<body style="background-color: #FAFAF7;">
    <!-- Left Side Divider -->
    <div class="hidden lg:block fixed left-0 top-0 bottom-0 w-1 z-40" style="background: linear-gradient(to bottom, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%);"></div>
    
    <!-- Right Side Divider -->
    <div class="hidden lg:block fixed right-0 top-0 bottom-0 w-1 z-40" style="background: linear-gradient(to bottom, #6B9A8B 0%, #87A08B 50%, #9FD8CE 100%);"></div>
    
    <!-- Skip to Content Link (WCAG 2.4.1) -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-6 focus:py-3 focus:rounded-xl focus:font-semibold focus:shadow-lg" style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%); color: white;">
        Skip to main content
    </a>
    
    <header class="sticky top-0 z-50 border-b" style="background-color: #FDFDFB; border-color: #E2E8E6; box-shadow: 0 2px 12px rgba(107, 154, 139, 0.08);">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex-shrink-0">
                    <a href="index.html" class="flex items-center hover:opacity-80 transition-opacity">
                        <img src="susantish-logo.png" alt="Susan Tish, CS" class="h-12 w-auto" style="max-height: 48px; object-fit: contain;">
                    </a>
                </div>
                <div class="hidden md:flex items-center space-x-1">
                    {create_navigation(pages, slug)}
                    <a href="booking.html" 
                       class="ml-4 text-white px-6 py-2.5 rounded-xl font-semibold transition-all duration-300 ease-in-out shadow-md hover:shadow-lg flex items-center gap-2"
                       style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%); color: white;">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        Book Appointment
                    </a>
                </div>
                <div class="md:hidden">
                    <button type="button" 
                            id="mobile-menu-button" 
                            aria-controls="mobile-menu" 
                            aria-expanded="false"
                            aria-label="Toggle navigation menu"
                            class="text-[#334155] hover:text-[#6B9A8B] focus:outline-none focus:ring-2 rounded-xl p-2 transition-all duration-300 ease-in-out"
                            style="--tw-ring-color: #6B9A8B;">
                        <svg id="menu-icon" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                        <svg id="close-icon" class="h-6 w-6 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </nav>
        <div id="mobile-menu" class="hidden md:hidden border-t" style="background-color: #FDFDFB; border-color: #E2E8E6;">
            <div class="px-4 pt-2 pb-3 space-y-1">
                {create_mobile_navigation(pages, slug)}
                <a href="booking.html" 
                   class="block text-white px-4 py-3 text-base font-semibold rounded-xl transition-all duration-300 ease-in-out text-center mt-2 shadow-md"
                   style="background: linear-gradient(135deg, #6B9A8B 0%, #87A08B 100%); color: white;">
                    📅 Book Appointment
                </a>
            </div>
        </div>
    </header>

    {homepage_hero}
    {what_i_help_with}
    {testimonials}

    {f'''<main id="main-content" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {'' if is_home or is_about or is_services or is_spiritual_healing or is_inspiration or is_booking else f'<h1 class="text-5xl font-bold text-center mb-3 max-w-4xl mx-auto leading-tight" style="color: #1E293B;">{title.split("|")[0].strip()}</h1>' if not is_contact else '<h1 class="text-5xl font-bold text-center mb-8 max-w-4xl mx-auto leading-tight" style="color: #1E293B;">Contact Me</h1>'}
        {'' if is_home or is_about or is_services or is_spiritual_healing or is_inspiration or is_booking else '<p class="text-xl text-center mb-8 max-w-3xl mx-auto leading-relaxed" style="color: #64748B;">Christian Science Practitioner • Over 20 Years Experience • Worldwide Remote Sessions</p>' if not is_contact else ''}
        {main_content}
        {contact_content}
        {cta_section}
    </main>''' if not is_home else ''}

    <footer class="text-white mt-16 border-t" style="background: linear-gradient(to bottom right, #1E293B, #334155); border-color: #E2E8E6;">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
                <div class="md:col-span-2">
                    <h3 class="text-3xl font-bold mb-2">Susan Tish, CS</h3>
                    <p class="text-gray-300 mb-4 text-lg">Christian Science Practitioner</p>
                    <p class="text-gray-400 mb-6">Providing spiritual healing services worldwide for over 20 years. Helping people find lasting health and well-being through prayer-based treatment.</p>
                    <div class="flex gap-2">
                        <span class="px-3 py-1 rounded-full text-sm" style="background-color: #6B9A8B;">20+ Years Experience</span>
                        <span class="px-3 py-1 rounded-full text-sm" style="background-color: #87A08B;">Worldwide Service</span>
                    </div>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-3">
                        <li><a href="index.html" class="text-gray-300 hover:text-white transition-colors">Home</a></li>
                        <li><a href="about.html" class="text-gray-300 hover:text-white transition-colors">About</a></li>
                        <li><a href="services.html" class="text-gray-300 hover:text-white transition-colors">Services</a></li>
                        <li><a href="inspiration.html" class="text-gray-300 hover:text-white transition-colors">Resources</a></li>
                        <li><a href="contact.html" class="text-gray-300 hover:text-white transition-colors">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-4">Contact</h3>
                    <ul class="space-y-3 text-gray-300">
                        <li><a href="mailto:susantishcs@gmail.com" class="hover:text-white transition-colors">susantishcs@gmail.com</a></li>
                        <li><a href="tel:734-693-5946" class="hover:text-white transition-colors">734-693-5946</a></li>
                        <li>Skype: susantishcs</li>
                    </ul>
                    <p class="text-gray-400 text-sm mt-4">Response within 24 hours</p>
                </div>
            </div>
            <div class="border-t border-gray-700 mt-12 pt-8 text-center text-gray-400">
                <p>&copy; 2025 Susan Tish. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        const menuIcon = document.getElementById('menu-icon');
        const closeIcon = document.getElementById('close-icon');
        
        if (mobileMenuButton) {{
            mobileMenuButton.addEventListener('click', () => {{
                const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
                
                // Toggle visibility
                mobileMenu.classList.toggle('hidden');
                menuIcon.classList.toggle('hidden');
                closeIcon.classList.toggle('hidden');
                
                // Update ARIA attributes
                mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
                mobileMenuButton.setAttribute('aria-label', 
                    isExpanded ? 'Open navigation menu' : 'Close navigation menu'
                );
            }});
        }}
        
        // Video play/pause control
        const video = document.getElementById('hero-video');
        const videoControlBtn = document.getElementById('video-control-btn');
        const pauseIcon = document.getElementById('pause-icon');
        const playIcon = document.getElementById('play-icon');
        
        if (video && videoControlBtn) {{
            videoControlBtn.addEventListener('click', () => {{
                if (video.paused) {{
                    video.play();
                    pauseIcon.classList.remove('hidden');
                    playIcon.classList.add('hidden');
                    videoControlBtn.setAttribute('aria-label', 'Pause background video');
                }} else {{
                    video.pause();
                    pauseIcon.classList.add('hidden');
                    playIcon.classList.remove('hidden');
                    videoControlBtn.setAttribute('aria-label', 'Play background video');
                }}
            }});
            
            // Keyboard support (Space or Enter)
            videoControlBtn.addEventListener('keydown', (e) => {{
                if (e.key === ' ' || e.key === 'Enter') {{
                    e.preventDefault();
                    videoControlBtn.click();
                }}
            }});
        }}
    </script>
</body>
</html>'''
    
    return template


def generate_website(json_file='site_content.json', output_dir='website'):
    """Generate complete website from JSON data."""
    print("🎯 Generating FULLY CUSTOMIZED Website v5.0")
    print("=" * 70)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        pages = json.load(f)
    
    print(f"📄 Loaded {len(pages)} pages from {json_file}")
    
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 Created output directory: {output_dir}/")
    
    pages_sorted = sorted(pages, key=lambda p: get_page_slug(p['url']))
    
    for page in pages_sorted:
        slug = get_page_slug(page['url'])
        
        # Skip the spiritual-healing page
        if slug == 'spiritual-healing':
            continue
            
        filename = 'index.html' if slug == 'home' else f'{slug}.html'
        filepath = Path(output_dir) / filename
        
        html = create_page_template(page, pages_sorted, pages)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated: {filename}")
    
    # Generate standalone booking page
    booking_page = {
        'url': 'booking',
        'title': 'Book an Appointment | Susan Tish, CS',
        'content': '',
        'summary': 'Schedule your free consultation with Susan Tish, Christian Science Practitioner'
    }
    booking_html = create_page_template(booking_page, pages_sorted, pages)
    booking_filepath = Path(output_dir) / 'booking.html'
    with open(booking_filepath, 'w', encoding='utf-8') as f:
        f.write(booking_html)
    print(f"✅ Generated: booking.html")
    
    print("=" * 70)
    print(f"🎉 FULLY CUSTOMIZED Website v5.0 generated!")
    print(f"📂 Location: {output_dir}/")
    print(f"\n✨ Version 5 Improvements:")
    print(f"   🏠 Home Page - Conversion-optimized with testimonials & CTAs")
    print(f"   👤 About Page - Susan's story with timeline & visual elements")
    print(f"   💼 Services Page - Detailed service cards & pricing info")
    print(f"   📚 Resources Page - Beautiful article grid with categories")
    print(f"   📧 Contact Page - Side-by-side info + form layout")
    print(f"\n🎨 Design Features:")
    print(f"   ✓ Custom layouts for EVERY page")
    print(f"   ✓ No more generic text blocks")
    print(f"   ✓ Visual cards and sections throughout")
    print(f"   ✓ Consistent conversion elements")
    print(f"   ✓ Mobile-responsive design")
    print(f"\n💡 To view:")
    print(f"   open {output_dir}/index.html")


if __name__ == "__main__":
    generate_website()

