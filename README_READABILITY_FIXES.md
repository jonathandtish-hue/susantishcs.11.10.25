# Home Page Readability Fixes - Quick Reference

## Direct TailwindCSS Changes for `index.html`

### HIGH PRIORITY FIXES

#### 1. Hero H1 - Fix Line Height (Line 228)
```html
<!-- BEFORE -->
<h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-4 leading-tight text-shadow-lg text-white">

<!-- AFTER -->
<h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 sm:mb-8 leading-normal text-shadow-lg text-white">
```

#### 2. Hero Badge - Increase Text Size (Line 226)
```html
<!-- BEFORE -->
<p class="text-white text-sm font-semibold tracking-wide uppercase">Over 20 Years of Experience</p>

<!-- AFTER -->
<p class="text-white text-base font-semibold tracking-wide uppercase">Over 20 Years of Experience</p>
```

#### 3. Hero Subheading - Improve Line Height (Line 231)
```html
<!-- BEFORE -->
<p class="text-xl sm:text-2xl text-white mb-3 leading-relaxed text-shadow-md">

<!-- AFTER -->
<p class="text-xl sm:text-2xl text-white mb-4 sm:mb-5 leading-loose text-shadow-md">
```

#### 4. Hero Secondary Text - Full Opacity (Line 234)
```html
<!-- BEFORE -->
<p class="text-lg text-white/90 mb-6 text-shadow-sm">

<!-- AFTER -->
<p class="text-lg text-white mb-8 sm:mb-10 text-shadow-sm">
```

#### 5. Section H2 - Fix Line Height (Line 284)
```html
<!-- BEFORE -->
<h2 class="text-4xl font-bold leading-tight text-primary">How I Can Help &amp; What Clients Are Experiencing</h2>

<!-- AFTER -->
<h2 class="text-4xl font-bold leading-[1.3] text-primary">How I Can Help &amp; What Clients Are Experiencing</h2>
```

#### 6. Section Intro Paragraph - Add Typography (Line 285)
```html
<!-- BEFORE -->
<p>Christian Science treatment meets you where you are—supporting physical healing, restoring peace of mind, and anchoring families in divine love.</p>

<!-- AFTER -->
<p class="text-lg leading-relaxed text-muted">Christian Science treatment meets you where you are—supporting physical healing, restoring peace of mind, and anchoring families in divine love.</p>
```

#### 7. Card Grid - Increase Gap (Line 288)
```html
<!-- BEFORE -->
<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

<!-- AFTER -->
<div class="grid gap-6 sm:gap-8 sm:grid-cols-2 lg:grid-cols-3">
```

#### 8. Featured Card - Improve Padding (Line 290)
```html
<!-- BEFORE -->
<article class="sm:col-span-2 lg:col-span-2 p-8 rounded-3xl ...">

<!-- AFTER -->
<article class="sm:col-span-2 lg:col-span-2 p-6 sm:p-8 lg:p-10 rounded-3xl ...">
```

#### 9. Featured Card Body Text - Increase Margin (Line 300)
```html
<!-- BEFORE -->
<p class="text-lg text-muted leading-relaxed mb-4">Prayer-based care that addresses pain, anxiety, and the need for calm with compassion and conviction. Through Christian Science treatment, we work together to find lasting solutions that restore your sense of peace and well-being.</p>

<!-- AFTER -->
<p class="text-lg text-muted leading-relaxed mb-6 max-w-prose">Prayer-based care that addresses pain, anxiety, and the need for calm with compassion and conviction. Through Christian Science treatment, we work together to find lasting solutions that restore your sense of peace and well-being.</p>
```

#### 10. Smaller Cards - Add Typography (Line 311)
```html
<!-- BEFORE -->
<article class="p-6 rounded-2xl shadow-sm fade-up fade-delay-120 relative overflow-hidden hover-lift" ...>

<!-- AFTER -->
<article class="p-6 sm:p-7 lg:p-8 rounded-2xl shadow-sm fade-up fade-delay-120 relative overflow-hidden hover-lift" ...>
```

#### 11. Smaller Card Body Text (Line 320)
```html
<!-- BEFORE -->
<p class="text-muted">Support that restores trust, strengthens marriages, and brings stability to the people you love.</p>

<!-- AFTER -->
<p class="text-base text-muted leading-relaxed">Support that restores trust, strengthens marriages, and brings stability to the people you love.</p>
```

#### 12. Smaller Card Body Text (Line 334)
```html
<!-- BEFORE -->
<p class="text-muted">Guidance for pivotal decisions, career shifts, and finding direction rooted in God's constant care.</p>

<!-- AFTER -->
<p class="text-base text-muted leading-relaxed">Guidance for pivotal decisions, career shifts, and finding direction rooted in God's constant care.</p>
```

#### 13. Hero Button Group - Increase Gap (Line 237)
```html
<!-- BEFORE -->
<div class="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start">

<!-- AFTER -->
<div class="flex flex-col sm:flex-row gap-4 sm:gap-4 justify-center lg:justify-start">
```

#### 14. Action Button Group - Improve Spacing (Line 338)
```html
<!-- BEFORE -->
<div class="flex flex-wrap items-center gap-4">

<!-- AFTER -->
<div class="flex flex-wrap items-center gap-5">
```

#### 15. Hero Container - Add Max Width (Line 223)
```html
<!-- BEFORE -->
<div class="text-center lg:text-left order-2 lg:order-1 glass-card p-6 lg:p-8 fade-up fade-delay-80">

<!-- AFTER -->
<div class="text-center lg:text-left order-2 lg:order-1 glass-card p-6 lg:p-8 lg:max-w-2xl fade-up fade-delay-80">
```

#### 16. Remove Conflicting Spacing (Line 351)
```html
<!-- BEFORE -->
<div class="quote-stack space-y-4">

<!-- AFTER -->
<div class="quote-stack">
```
*(Note: `quote-stack` CSS class already handles spacing)*

---

### CSS UPDATES NEEDED (in `tokens.css`)

#### Update Quote Stack Line Height (Line 1264-1270)
```css
/* BEFORE */
.quote-stack__quote {
  font-family: var(--font-display);
  font-size: clamp(1.25rem, 2.5vw, 1.65rem);
  line-height: 1.5;  /* Too tight */
  margin: clamp(0.9rem, 2vw, 1.4rem) 0;
  color: var(--color-text-primary);
}

/* AFTER */
.quote-stack__quote {
  font-family: var(--font-display);
  font-size: clamp(1.25rem, 2.5vw, 1.65rem);
  line-height: 1.65;  /* Improved for readability */
  margin: clamp(0.9rem, 2vw, 1.4rem) 0;
  color: var(--color-text-primary);
}
```

#### Optional: Improve Body Text Letter Spacing (Line 66-73)
```css
/* BEFORE */
body {
  font-family: var(--font-sans);
  font-size: var(--type-body);
  line-height: 1.75;
  color: var(--color-text-primary);
  background-color: var(--color-bg-base);
  letter-spacing: -0.01em;  /* Negative tracking */
}

/* AFTER */
body {
  font-family: var(--font-sans);
  font-size: var(--type-body);
  line-height: 1.75;
  color: var(--color-text-primary);
  background-color: var(--color-bg-base);
  letter-spacing: 0;  /* Neutral for better readability */
}
```

---

## Summary of Changes

### Typography Improvements
- ✅ Hero H1: `leading-tight` → `leading-normal`
- ✅ Hero badge: `text-sm` → `text-base`
- ✅ Hero subheading: `leading-relaxed` → `leading-loose`
- ✅ Hero secondary: `text-white/90` → `text-white`
- ✅ Section H2: `leading-tight` → `leading-[1.3]`
- ✅ Intro paragraph: Add `text-lg leading-relaxed`
- ✅ Card body: Add `text-base leading-relaxed`
- ✅ Quote text: Increase line-height to 1.65 (CSS)

### Spacing Improvements
- ✅ Hero H1 margin: `mb-4` → `mb-6 sm:mb-8`
- ✅ Hero subheading margin: `mb-3` → `mb-4 sm:mb-5`
- ✅ Hero secondary margin: `mb-6` → `mb-8 sm:mb-10`
- ✅ Card grid gap: `gap-4` → `gap-6 sm:gap-8`
- ✅ Featured card padding: `p-8` → `p-6 sm:p-8 lg:p-10`
- ✅ Smaller card padding: `p-6` → `p-6 sm:p-7 lg:p-8`
- ✅ Card body margin: `mb-4` → `mb-6`
- ✅ Button group gap: `gap-3` → `gap-4`
- ✅ Action button gap: `gap-4` → `gap-5`

### Layout Improvements
- ✅ Hero container: Add `lg:max-w-2xl`
- ✅ Card body: Add `max-w-prose`
- ✅ Remove conflicting `space-y-4` from quote-stack

### Accessibility Improvements
- ✅ Improve text sizes for better readability
- ✅ Increase line heights for comfort
- ✅ Full opacity text for better contrast
- ✅ Better spacing for touch targets

---

## Testing Checklist

After implementing changes:
- [ ] Verify hero section readability on mobile and desktop
- [ ] Check card spacing at various screen sizes
- [ ] Test text contrast with browser dev tools
- [ ] Verify line lengths are optimal (50-75 characters)
- [ ] Test with browser zoom at 200%
- [ ] Check focus indicators are visible
- [ ] Validate with screen reader if possible

---

**Next Steps:** Implement high-priority fixes first, then test and iterate on medium-priority improvements.

