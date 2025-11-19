import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const About = () => {
  return (
    <div className="bg-page">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 btn-gradient">
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content">
        {/* Hero Section with Photo */}
        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--edge">
            <div className="pattern-shell pattern-shell--split">
              <div className="pattern-shell__media fade-up fade-delay-80">
                <img src="/susan-about.jpg" alt="Susan Tish, Christian Science Practitioner" />
              </div>
              <div className="pattern-shell__content fade-up fade-delay-140">
                <span className="section-eyebrow">Meet Susan</span>
                <h2 className="text-4xl font-bold leading-tight text-primary mb-5">My Journey to Healing</h2>
                <p className="text-xl leading-relaxed text-muted mb-4">
                  Searching for the deeper meaning, the underlying truth of things, has been a lifelong pursuit. 
                  Studying Christian Science as a youth, I found rich answers to deep questions about life.
                </p>
                <p className="text-lg leading-relaxed text-muted">
                  I began to confirm my belief that what we see and hear with our physical senses does not 
                  always lead us to truth, health, or happiness. Prayer revealed a spiritual foundation I could trust.
                </p>
                <div className="pattern-shell__meta">
                  <span className="pattern-shell__chip">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M12 18a6 6 0 110-12 6 6 0 010 12z"></path>
                    </svg>
                    20+ years in practice
                  </span>
                  <span className="pattern-shell__chip">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v7H5a2 2 0 01-2-2v-7zM19 9v11a2 2 0 01-2 2h-2v-7a2 2 0 00-2-2h-3V9a2 2 0 012-2h5.945a2 2 0 012 2z"></path>
                    </svg>
                    Worldwide support
                  </span>
                  <span className="pattern-shell__chip">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                    Writer &amp; speaker
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Key Moment Story */}
        <section className="section-flow section-flow--evening">
          <div className="layout-shell layout-shell--narrow">
            <div className="callout-banner fade-up fade-delay-180">
              <h3 className="callout-banner__title">The Moment That Changed Everything</h3>
              <p className="callout-banner__quote">
                As a young girl I witnessed my grandmother <strong>recover completely and rapidly from a car accident</strong> 
                that doctors warned she would never recover from, through her reliance on God.
              </p>
              <div className="callout-banner__aside">
                I realized that what we often perceive as inevitable limitations or challenges are unknown to God 
                and have no bearing on our true nature or our permanent health as spiritual beings.
              </div>
            </div>
          </div>
        </section>
        
        {/* What I Learned */}
        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--edge">
            <div className="section-intro section-intro--left section-intro--narrow">
              <span className="section-eyebrow">Lessons From Practice</span>
            </div>
            <div className="story-rail">
              <article className="story-rail__event story-rail__event--accent fade-up fade-delay-100">
                <h3 className="story-rail__title">Nothing Is Too Difficult</h3>
                <p className="story-rail__body">
                  There isn't anything too difficult to overcome, no matter what the physical picture presents. 
                  God, this all-loving, all-intelligent presence, undergirds me and everyone.
                </p>
              </article>
              <article className="story-rail__event fade-up fade-delay-160">
                <h3 className="story-rail__title">Permanent Well-Being</h3>
                <p className="story-rail__body">
                  Learning more about God introduced me to an all-loving, ever-present Spirit that leads us to 
                  discover our greatest potential and understand our permanent well-being.
                </p>
              </article>
              <article className="story-rail__event fade-up fade-delay-220">
                <h3 className="story-rail__title">Prayer With Purpose</h3>
                <p className="story-rail__body">
                  Each treatment is a focused spiritual treatment—anchored in scripture, Mary Baker Eddy's writings, 
                  and Christly compassion—that continues beyond our conversation.
                </p>
              </article>
            </div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="callout-banner text-center fade-up">
              <h3 className="callout-banner__title">Ready to Begin Your Journey?</h3>
              <p className="callout-banner__quote">
                Let's explore how prayer-based treatment can support you.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center mt-6">
                <Link to="/booking" className="btn-gradient">Schedule Free Consultation</Link>
                <Link to="/services" className="btn-outline">Learn About Services</Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default About;

