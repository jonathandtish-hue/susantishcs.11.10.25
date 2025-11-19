import { useEffect } from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Booking = () => {
  useEffect(() => {
    // Load Calendly widget script
    const script = document.createElement('script');
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="bg-page">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 btn-gradient">
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content">
        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--edge">
            <div className="pattern-shell pattern-shell--split">
              <div className="pattern-shell__content">
                <span className="section-eyebrow">Complimentary Conversation</span>
                <h1 className="text-4xl font-bold leading-tight text-primary mb-4">Schedule Your Free Consultation</h1>
                <p className="text-muted mb-6">
                  Choose a time that fits your day. We'll explore what's unfolding, answer questions about Christian Science treatment, and outline supportive next steps together.
                </p>
                <div className="pattern-shell__meta flex gap-4">
                  <a href="#booking" className="btn-gradient">Go to booking</a>
                  <Link to="/contact" className="btn-outline">Contact first</Link>
                </div>
              </div>
              <div className="pattern-shell__media">
                <div className="flow-card flow-card--accent">
                  <span className="flow-card__eyebrow">What's Included</span>
                  <h3 className="flow-card__title">15-minute welcome call</h3>
                  <p className="flow-card__body">
                    Available worldwide by phone, email, or video. Flexible daytime and evening availability to meet your schedule.
                  </p>
                  <ul className="flow-card__list">
                    <li><span className="flow-card__bullet">✓</span> Prayer-based support from the very first conversation</li>
                    <li><span className="flow-card__bullet">✓</span> Space to ask questions about treatment and next steps</li>
                    <li><span className="flow-card__bullet">✓</span> Follow-up options tailored to you or a loved one</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--edge">
            <div className="section-intro section-intro--left section-intro--narrow">
              <span className="section-eyebrow">What to Expect</span>
              <h2 className="text-3xl font-bold leading-tight text-primary">Thoughtful, Prayerful Preparation</h2>
              <p>Each introductory call is confidential, gentle, and grounded in prayer so you feel supported from the very first moment.</p>
            </div>
            <div className="flow-grid">
              <div className="flow-card flow-card--soft fade-up fade-delay-80">
                <h3 className="flow-card__title">Warm welcome</h3>
                <p className="flow-card__body">Share what's taking place and feel heard without judgment. We begin with inspiration, not with problems.</p>
              </div>
              <div className="flow-card flow-card--soft fade-up fade-delay-120">
                <h3 className="flow-card__title">Flexible format</h3>
                <p className="flow-card__body">We can meet by phone, email, or Skype and can discuss in-person visits if that's helpful.</p>
              </div>
              <div className="flow-card flow-card--soft fade-up fade-delay-160">
                <h3 className="flow-card__title">Next steps in peace</h3>
                <p className="flow-card__body">We'll outline options, timing, and fees so you can move forward confidently and without pressure.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="booking" className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="soft-card p-8 shadow-soft fade-up">
              <div className="flex items-start gap-4 mb-6">
                <div className="w-12 h-12 rounded-xl bg-gradient-brand flex items-center justify-center text-white">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <h2 className="text-3xl font-bold leading-tight text-primary">Reserve Your Time</h2>
                  <p className="text-muted">Select a slot below and Calendly will confirm your appointment instantly.</p>
                </div>
              </div>
              <div className="calendly-inline-widget" data-url="https://calendly.com/YOUR_CALENDLY_USERNAME?hide_gdpr_banner=1&primary_color=2563eb" style={{ minWidth: '100%', height: '720px' }}></div>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="flow-sidenote fade-up fade-delay-200">
              <div className="flex items-start gap-4">
                <svg className="w-8 h-8 text-sage flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
                </svg>
                <div>
                  <h3 className="text-xl font-bold text-primary mb-2">Calendly setup required</h3>
                  <p className="text-muted mb-2">Once your Calendly account is ready, replace <code className="bg-section-soft px-2 py-1 rounded">YOUR_CALENDLY_USERNAME</code> in the embed URL above.</p>
                  <ol className="list-decimal list-inside text-muted space-y-1">
                    <li>Create or log in at <a href="https://calendly.com" target="_blank" rel="noopener noreferrer" className="underline font-semibold">calendly.com</a></li>
                    <li>Configure your availability and meeting length</li>
                    <li>Update the embed URL and publish your site</li>
                  </ol>
                  <p className="text-sm italic text-muted mt-3">Need more guidance? Review <strong>CALENDLY_SETUP_INSTRUCTIONS.md</strong>.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--narrow">
            <div className="callout-banner fade-up fade-delay-240">
              <h3 className="callout-banner__title">Prefer to reach out directly?</h3>
              <p className="callout-banner__quote">"Love meets every need. If you don't see a time that works, I'll gladly arrange one with you."</p>
              <div className="callout-banner__aside">Email or call and I'll respond within 24 hours to help you find the perfect time.</div>
              <div className="mt-6 flex flex-col sm:flex-row gap-3">
                <a href="mailto:susantishcs@gmail.com" className="btn-gradient">Email Me</a>
                <a href="tel:734-693-5946" className="btn-outline">Call Me</a>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Booking;
