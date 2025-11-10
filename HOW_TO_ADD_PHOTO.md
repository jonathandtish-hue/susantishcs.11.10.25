# How to Add Your Photo - Step by Step

## The Problem
The current file is not a real image - it's just 629 bytes of error text. You need to manually save the photo from the chat.

## Solution - 3 Easy Steps:

### Step 1: Save the Photo from Chat
1. Scroll up to where you attached your hiking photo in this conversation
2. **Right-click** on the image
3. Choose **"Save Image As..."** or **"Download Image"**
4. Save it to your **Desktop** (for now, any name is fine)

### Step 2: Move and Rename
**Option A - Using Finder:**
1. Open **Finder**
2. Find the photo you just saved (probably in Desktop or Downloads)
3. **Drag it** to: `/Users/jonathantish/Downloads/susantishcs-102425/website/`
4. **Rename it** to exactly: `susan-tish.jpg`

**Option B - Using Terminal:**
```bash
# If the photo is on your Desktop (replace "your-photo-name.jpg" with actual name):
cd /Users/jonathantish/Downloads/susantishcs-102425/website
cp ~/Desktop/your-photo-name.jpg susan-tish.jpg

# Or if it's in Downloads:
cp ~/Downloads/your-photo-name.jpg susan-tish.jpg
```

### Step 3: Verify It Works
1. Go to: **http://localhost:8080/**
2. You should see your real photo!
3. Check both:
   - Homepage (right side hero section)
   - About page (left side with your story)

## Troubleshooting

**If the photo still doesn't show:**
```bash
# Check the file size (should be 50KB-500KB, not 629 bytes):
cd /Users/jonathantish/Downloads/susantishcs-102425/website
ls -lh susan-tish.jpg

# Check the file type (should say "JPEG image" or similar):
file susan-tish.jpg
```

**Good output looks like:**
```
-rw-r--r--  1 user  staff   245K Oct 24 17:30 susan-tish.jpg
susan-tish.jpg: JPEG image data...
```

**Bad output (what you have now):**
```
-rw-r--r--  1 user  staff   629B Oct 24 17:04 susan-tish.jpg
susan-tish.jpg: XML 1.0 document text...
```

## Need Help?

Let me know if:
- You can't find where the photo saved
- The file size is still tiny (under 10KB)
- The photo isn't showing after you add it

I'm here to help! 📸


