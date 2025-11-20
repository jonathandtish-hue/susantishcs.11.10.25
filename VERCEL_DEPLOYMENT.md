# Vercel Deployment Guide

## ✅ Project is Ready for Deployment

Your React/Vite application has been configured for Vercel deployment.

## What Was Configured

1. **Updated `package.json`**:
   - Changed `build` script to use `vite build` (required for Vercel)
   - Kept other scripts for local development

2. **Created `vercel.json`**:
   - Configured build command: `npm run build`
   - Set output directory: `dist`
   - Added rewrites for React Router (SPA routing)

3. **Updated `.gitignore`**:
   - Added `node_modules/`, `dist/`, `.vite/`, and `.vercel/`
   - Added environment variable files

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "Add New Project"**
3. **Import your GitHub repository**:
   - Select `susantish-website` repository
   - Vercel will auto-detect the settings from `vercel.json`
4. **Deploy!** - Click "Deploy"

Vercel will automatically:
- Install dependencies (`npm install`)
- Build the project (`npm run build`)
- Deploy to a production URL

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Deploy
vercel

# For production deployment
vercel --prod
```

## Important: Configure Formspree Before Going Live

⚠️ **The contact form needs your Formspree ID before it will work.**

1. **Get your Formspree ID**:
   - Sign up at [formspree.io](https://formspree.io)
   - Create a form and copy your form ID (looks like `xyzabc123`)

2. **Update the Contact form**:
   - Edit `src/pages/Contact.tsx`
   - Replace `YOUR_FORM_ID` on line 14 with your actual Formspree ID:
     ```typescript
     const response = await fetch("https://formspree.io/f/YOUR_ACTUAL_ID", {
     ```
   - Commit and push the change
   - Vercel will automatically redeploy

## Environment Variables (If Needed)

If you need to add environment variables later:

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add any variables your app needs
4. Redeploy

## Build Verification

✅ Build tested successfully:
- Output directory: `dist/`
- All assets included (images, videos, CSS, JS)
- React Router configured for SPA routing

## Post-Deployment Checklist

- [ ] Test all pages load correctly
- [ ] Test navigation between pages
- [ ] Configure Formspree form ID
- [ ] Test contact form submission
- [ ] Verify all images load
- [ ] Test on mobile devices
- [ ] Set up custom domain (optional)

## Troubleshooting

### Build fails on Vercel:
- Check that all dependencies are in `package.json`
- Verify Node.js version (Vercel auto-detects, but you can specify in `package.json`)

### Routes return 404:
- The `vercel.json` rewrites should handle this
- If issues persist, check that `vercel.json` is in the root directory

### Form doesn't work:
- Make sure you've replaced `YOUR_FORM_ID` with your actual Formspree ID
- Check browser console for errors
- Verify Formspree form is active in your dashboard

## Support

For Vercel-specific issues, check:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)

