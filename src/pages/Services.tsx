import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Services = () => {
  return (
    <div className="bg-page">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 btn-gradient">
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content">
        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--edge">
            <div className="section-intro">
              <span className="section-eyebrow">Prayer Treatment</span>
              <h2 className="text-4xl font-bold leading-tight text-primary">Prayer-Based Healing Treatment</h2>
              <p className="text-lg text-muted max-w-2xl mx-auto">
                Christian Science treatment can be provided to any patient seeking healing from illness, mental health, relationship, or employment concerns. Each treatment is specific, inspired, and rooted in an understanding of God's all-loving, permanent relationship to each of us.
              </p>
            </div>
            <div className="flow-grid mt-12">
              <article className="flow-card flow-card--sunlit flow-grid__wide fade-up fade-delay-80">
                <div className="flow-card__icon bg-gradient-brand text-white">
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                  </svg>
                </div>
                <h3 className="flow-card__title">Healing Treatment</h3>
                <p className="flow-card__body">Specific, prayer-based treatment that begins from your inherent wholeness and continues through to permanent healing.</p>
                <ul className="flow-card__list">
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Phone sessions
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Email support
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Continuous prayer
                  </li>
                </ul>
              </article>

              <article className="flow-card flow-card--soft fade-up fade-delay-120">
                <div className="flow-card__icon bg-gradient-mint text-white">
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                  </svg>
                </div>
                <h3 className="flow-card__title">Consultation &amp; Guidance</h3>
                <p className="flow-card__body">Sometimes it is helpful to talk through questions, explore scripture, or receive guidance as you deepen your spiritual study.</p>
                <ul className="flow-card__list">
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Q&amp;A sessions
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Spiritual guidance
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Study support
                  </li>
                </ul>
              </article>

              <article className="flow-card flow-card--sage flow-grid__tall fade-up fade-delay-160">
                <div className="flow-card__icon bg-gradient-mint-sky text-white">
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                  </svg>
                </div>
                <h3 className="flow-card__title">Office or Home Visits</h3>
                <p className="flow-card__body">While healing doesn't depend on proximity, some prefer time together in person to explore spiritual truths more deeply.</p>
                <ul className="flow-card__list">
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    In-person sessions
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Home visits available
                  </li>
                  <li>
                    <span className="flow-card__bullet">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    Deep spiritual exploration
                  </li>
                </ul>
              </article>
            </div>
            
            <div className="text-center mt-12">
              <Link to="/booking" className="btn-gradient">Schedule Free Consultation</Link>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Services;

