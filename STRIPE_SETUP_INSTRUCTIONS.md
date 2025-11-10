# Stripe Payment Integration Setup Instructions

## Overview
Your website now includes a beautiful "Services & Pricing" page with Stripe payment buttons ready to be connected. Follow these steps to activate the payment functionality.

## Step 1: Create Your Stripe Account

1. **Go to Stripe**: Visit [https://stripe.com](https://stripe.com)
2. **Sign Up**: Click "Start now" and create a free account
3. **Verify Your Email**: Check your inbox for verification email
4. **Complete Business Setup**: 
   - Enter your business information
   - Add your bank account for payouts
   - Verify your identity (required for payouts)

**Note**: Stripe is free to sign up. They only charge 2.9% + $0.30 per transaction when you receive payments.

## Step 2: Create Payment Links

### For Each Service Type:

1. **Go to Products**: In your Stripe dashboard, click "Products" in the left sidebar
2. **Click "Create Product"** or **"Payment Links"** → **"Create Payment Link"**

3. **Set Up Each Service**:

   **A. Initial Treatment Session**
   - Name: "Initial Treatment Session"
   - Price: Enter your price (e.g., $150)
   - Description: "60-90 minute initial treatment session with prayer-based healing"
   - Click "Create payment link"
   - Copy the link (looks like: `https://buy.stripe.com/abc123xyz`)

   **B. Follow-up Session**
   - Name: "Follow-up Session"
   - Price: Enter your price (e.g., $75)
   - Description: "30-45 minute follow-up session"
   - Copy the payment link

   **C. Monthly Support Package** (Subscription)
   - Name: "Monthly Support Package"
   - Price: Enter monthly price (e.g., $200)
   - **Select "Recurring"** → Monthly
   - Description: "Ongoing monthly support with regular check-ins"
   - Copy the subscription link

   **D. Emergency Session**
   - Name: "Emergency Session"
   - Price: Enter your price (e.g., $125)
   - Description: "24/7 emergency prayer treatment"
   - Copy the payment link

## Step 3: Update Your Website Code

### Find the Payment Links Section:

1. **Open**: `generate_website_v5.py` in your code editor
2. **Search for**: `stripePaymentLinks` (around line 1963)
3. **You'll see**:
   ```javascript
   const stripePaymentLinks = {
       initial: 'https://buy.stripe.com/YOUR_INITIAL_SESSION_LINK',
       followup: 'https://buy.stripe.com/YOUR_FOLLOWUP_SESSION_LINK',
       monthly: 'https://buy.stripe.com/YOUR_MONTHLY_SUBSCRIPTION_LINK',
       emergency: 'https://buy.stripe.com/YOUR_EMERGENCY_SESSION_LINK'
   };
   ```

4. **Replace** the placeholder URLs with your actual Stripe payment links:
   ```javascript
   const stripePaymentLinks = {
       initial: 'https://buy.stripe.com/abc123xyz',  // Your Initial Session link
       followup: 'https://buy.stripe.com/def456uvw',  // Your Follow-up link
       monthly: 'https://buy.stripe.com/ghi789rst',  // Your Monthly Subscription link
       emergency: 'https://buy.stripe.com/jkl012mno'  // Your Emergency link
   };
   ```

## Step 4: Update Prices

### Find and Replace Price Placeholders:

1. **Search for**: `$XXX` in the file
2. **Replace** with your actual prices:

   **Initial Session** (around line 1683):
   ```html
   <div class="text-4xl font-bold text-white mb-1">$150</div>
   ```
   And (around line 1714):
   ```html
   <span id="initial-btn-text">Pay $150 - Initial Session</span>
   ```

   **Follow-up Session** (around line 1729):
   ```html
   <div class="text-4xl font-bold text-indigo-600 mb-1">$75</div>
   ```
   And (around line 1760):
   ```html
   <span id="followup-btn-text">Pay $75 - Follow-up</span>
   ```

   **Monthly Package** (around line 1774):
   ```html
   <div class="text-3xl font-bold text-purple-600 mb-1">$200</div>
   ```
   And (around line 1814):
   ```html
   <span id="monthly-btn-text">Subscribe $200/month</span>
   ```

   **Emergency Session** (around line 1825):
   ```html
   <div class="text-3xl font-bold text-red-600 mb-1">$125</div>
   ```
   And (around line 1865):
   ```html
   <span id="emergency-btn-text">Pay $125 - Emergency</span>
   ```

## Step 5: Regenerate Your Website

```bash
cd /Users/jonathantish/Downloads/susantishcs-102425
python3 generate_website_v5.py
```

## Step 6: Test the Payment Buttons

1. **Open**: `website/pricing.html` in your browser
2. **Click** each payment button
3. **Verify**: They redirect to your Stripe checkout page
4. **Test Transaction**: Use Stripe's test mode with test card: `4242 4242 4242 4242`

## Stripe Test Mode vs Live Mode

### Test Mode (Default):
- Use test card numbers (4242 4242 4242 4242)
- No real charges are processed
- Perfect for testing
- Toggle in Stripe Dashboard → Settings → Test/Live mode

### Live Mode:
- Switch when ready to accept real payments
- Real credit cards are charged
- Money goes to your bank account
- Toggle in Stripe Dashboard

## Payment Link Features

### Customize Your Payment Links:
- **Add descriptions**: Explain what's included
- **Set quantity limits**: Max 1 per customer (optional)
- **Add images**: Upload service images
- **Customize thank you page**: Add follow-up message
- **Email receipts**: Automatic (enabled by default)

### Collect Additional Information:
- Add custom fields to payment links:
  - "How did you hear about us?"
  - "Any specific concerns to address?"
  - "Preferred contact method"

## Security & Compliance

✅ **PCI DSS Compliant**: Stripe handles all card data  
✅ **Encrypted**: All transactions are encrypted  
✅ **No card storage**: Your website never sees card numbers  
✅ **Automatic receipts**: Emailed to customers  
✅ **Fraud protection**: Built-in Stripe Radar  

## Payment Processing Timeline

- **Immediate**: Customer sees confirmation
- **1-2 business days**: Money arrives in your bank account
- **Automatic**: No manual processing needed

## Managing Payments

### View Payments:
- Stripe Dashboard → Payments
- See all transactions, refunds, disputes

### Issue Refunds:
- Click on any payment
- Click "Refund"
- Full or partial refunds

### Download Reports:
- Stripe Dashboard → Reports
- Export for taxes/bookkeeping

## Troubleshooting

### Payment Buttons Not Working?
- **Check**: JavaScript in browser console (F12)
- **Verify**: Payment links are correct (no `YOUR_` placeholders)
- **Ensure**: Hard refresh browser (Cmd+Shift+R)

### Payment Links Not Redirecting?
- **Check**: Links start with `https://buy.stripe.com/`
- **Verify**: Links are active in Stripe dashboard
- **Test**: Open link directly in browser

### Prices Not Updating?
- **Check**: You replaced all `$XXX` placeholders
- **Verify**: Regenerated website after changes
- **Hard refresh**: Clear browser cache

## Optional: Customize Payment Experience

### Stripe Payment Links Settings:
- **Branding**: Add your logo
- **Colors**: Match your website theme
- **Thank you message**: Custom post-payment message
- **Email notifications**: Customize receipt emails

### Advanced Features (Optional):
- **Coupon codes**: Create discount codes
- **Payment plans**: Installment options
- **Multiple currencies**: Accept international payments

## Next Steps

1. ✅ Create Stripe account
2. ✅ Create payment links for all services
3. ✅ Update code with your links and prices
4. ✅ Regenerate website
5. ✅ Test payment buttons
6. ✅ Switch to live mode when ready
7. ✅ Share pricing page with clients!

## Support

- **Stripe Help Center**: [https://support.stripe.com](https://support.stripe.com)
- **Stripe Documentation**: [https://stripe.com/docs](https://stripe.com/docs)
- **Payment Links Guide**: [https://stripe.com/docs/payments/payment-links](https://stripe.com/docs/payments/payment-links)

---

**🎉 Once set up, your clients can pay directly from your website!**

**Questions?** The pricing page is at: `website/pricing.html`


