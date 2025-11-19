import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Inspiration = () => {
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
              <span className="section-eyebrow">Resources &amp; Inspiration</span>
              <h1 className="text-4xl font-bold leading-tight text-primary">Inspiration for Spiritual Living and Healing</h1>
              <p className="text-lg text-muted max-w-2xl mx-auto">
                Explore articles, insights, and spiritual resources to support your healing journey.
              </p>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--narrow">
            <div className="text-center p-12 rounded-3xl bg-surface-soft border-2 border-dashed border-sage/20">
              <svg className="w-16 h-16 mx-auto mb-4 text-sage/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
              </svg>
              <p className="text-muted text-lg font-medium">Inspiration content coming soon</p>
              <p className="text-subtle text-sm mt-2">Articles, insights, and spiritual resources will appear here</p>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="text-center">
              <Link to="/services" className="btn-gradient">Explore Services</Link>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Inspiration;

