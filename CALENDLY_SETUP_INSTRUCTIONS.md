# Calendly Integration Setup Instructions

## Overview
Your website now includes a dedicated booking page with Calendly integration, allowing clients to easily schedule appointments with you. Follow these steps to complete the setup.

## Step 1: Create Your Calendly Account

1. **Go to Calendly**: Visit [https://calendly.com](https://calendly.com)
2. **Sign Up**: Create a free account using your email address
3. **Choose Your Plan**: 
   - Free plan works great for basic scheduling
   - Consider paid plans for more features (multiple event types, integrations, etc.)

## Step 2: Set Up Your Availability

1. **Set Your Weekly Hours**: 
   - Go to "Availability" in your Calendly dashboard
   - Set your available days and times
   - Example: Monday-Friday, 9:00 AM - 5:00 PM

2. **Configure Time Zone**: 
   - Make sure your time zone is set correctly
   - Calendly will automatically show times in your clients' time zones

3. **Add Buffer Times** (Optional):
   - Add time before/after appointments if needed
   - Helps prevent back-to-back bookings

## Step 3: Create Your Event Type

1. **Create "Free Consultation" Event**:
   - Event name: "Free 15-Minute Consultation"
   - Duration: 15 minutes
   - Location: Phone call (or Zoom/Skype if you prefer)

2. **Add Event Description**:
   ```
   Schedule a complimentary 15-minute consultation to discuss how Christian Science 
   treatment can help with your specific needs. We'll get to know each other and 
   determine if we're a good fit to work together.
   
   During this call, we'll discuss:
   - Your current situation and needs
   - How Christian Science treatment works
   - Next steps if you'd like to proceed
   ```

3. **Configure Booking Settings**:
   - Minimum scheduling notice: 4 hours (recommended)
   - Date range: 60 days into the future
   - Form fields: Name, Email, Phone (optional), "Tell me about your needs"

## Step 4: Get Your Calendly Link

1. **Find Your Link**: 
   - Go to your event type
   - Click "Copy Link"
   - It will look like: `https://calendly.com/your-username/free-consultation`
   - Or: `https://calendly.com/your-username` (for your main scheduling page)

2. **Note Your Username**: 
   - The part after `/` in your link
   - Example: If your link is `https://calendly.com/susantish`, your username is `susantish`

## Step 5: Update Your Website Code

1. **Open the Generator File**:
   ```bash
   # Navigate to your project folder
   cd /Users/jonathantish/Downloads/susantishcs-102425
   
   # Open generate_website_v5.py in your code editor
   ```

2. **Find the Calendly Embed Code**:
   - Search for: `YOUR_CALENDLY_USERNAME`
   - Located in the `create_booking_page_content()` function
   - Around line 1666

3. **Replace with Your Link**:
   ```html
   <!-- BEFORE -->
   <div class="calendly-inline-widget" 
        data-url="https://calendly.com/YOUR_CALENDLY_USERNAME?hide_gdpr_banner=1&primary_color=2563eb"
   
   <!-- AFTER (example) -->
   <div class="calendly-inline-widget" 
        data-url="https://calendly.com/susantish/free-consultation?hide_gdpr_banner=1&primary_color=2563eb"
   ```

4. **Save the File**

## Step 6: Regenerate Your Website

```bash
cd /Users/jonathantish/Downloads/susantishcs-102425
python3 generate_website_v5.py
```

## Step 7: Test Your Booking Page

1. Open your website: `website/booking.html`
2. Check that the calendar loads properly
3. Try booking a test appointment
4. Verify you receive the confirmation email

## Optional: Remove the Setup Notice

Once Calendly is working properly, you can remove the yellow "Setup Required" notice:

1. In `generate_website_v5.py`, find the section with `<!-- Setup Notice -->`
2. Delete or comment out lines 1672-1695 (the entire yellow notice section)
3. Regenerate the website

## Calendly Best Practices

### Email Notifications
- Set up email reminders for yourself (24 hours before, 1 hour before)
- Enable email confirmations for clients
- Consider SMS reminders for clients (paid feature)

### Calendar Integration
- Connect your Google Calendar, Outlook, or iCloud calendar
- This prevents double-bookings and keeps you organized

### Customize Your Link
- Upgrade to paid plan to use a custom domain
- Example: `https://book.susantish.com` instead of `https://calendly.com/susantish`

### Additional Event Types
You can create multiple appointment types:
- "Free 15-Minute Consultation" (current)
- "Initial Treatment Session" (30-60 minutes)
- "Follow-up Session" (30 minutes)
- "Prayer Support Check-in" (15 minutes)

### Form Questions
Consider adding these questions to your booking form:
- "What brings you here today?"
- "Have you experienced Christian Science treatment before?"
- "How did you hear about me?"
- "Preferred contact method (phone/email/Skype)"

## Troubleshooting

### Calendar Not Showing?
- Check that you replaced `YOUR_CALENDLY_USERNAME` with your actual username
- Make sure your event type is "Active" in Calendly
- Check browser console for JavaScript errors

### Wrong Time Zone?
- Verify your time zone in Calendly settings
- Client will see times in their own time zone automatically

### Bookings Not Appearing?
- Check your Calendly email notifications
- Make sure calendar integration is connected
- Check spam folder

## Support

- **Calendly Help Center**: [https://help.calendly.com](https://help.calendly.com)
- **Video Tutorials**: Search "Calendly tutorial" on YouTube
- **Technical Issues**: Contact Calendly support through their website

## Next Steps

Once your Calendly is set up and working:

1. ✅ Test the booking flow yourself
2. ✅ Share the booking link with friends for feedback  
3. ✅ Update your email signature with the booking link
4. ✅ Consider adding the booking link to your social media profiles
5. ✅ Monitor your bookings and adjust availability as needed

---

**Questions?** The booking page is at: `website/booking.html`


