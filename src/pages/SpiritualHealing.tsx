import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const SpiritualHealing = () => {
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
              <span className="section-eyebrow">How It Works</span>
              <h1 className="text-4xl font-bold leading-tight text-primary">Spiritual Healing | How Christian Science Healing Works</h1>
              <p className="text-lg text-muted max-w-2xl mx-auto">
                Learn how Christian Science spiritual healing works in daily life—rooted in the Bible, practiced through prayer, and available to everyone seeking lasting transformation.
              </p>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--narrow">
            <div className="space-y-8">
              <div className="soft-card p-8 shadow-soft fade-up">
                <h2 className="text-3xl font-bold text-primary mb-4">Understanding Christian Science Treatment</h2>
                <p className="text-lg text-muted leading-relaxed mb-4">
                  Christian Science treatment is prayer-based healing that acknowledges your spiritual identity as God's beloved creation. 
                  It's not about positive thinking or ignoring problems—it's about discovering the permanent, spiritual reality that underlies all existence.
                </p>
                <p className="text-lg text-muted leading-relaxed">
                  Through prayer, we access an understanding of God's all-loving, all-powerful nature and recognize that harmony, health, and wholeness 
                  are our natural state as spiritual beings created in God's image.
                </p>
              </div>

              <div className="soft-card p-8 shadow-soft fade-up fade-delay-120">
                <h2 className="text-3xl font-bold text-primary mb-4">Rooted in Scripture</h2>
                <p className="text-lg text-muted leading-relaxed mb-4">
                  Christian Science healing is based on the Bible's teachings, particularly the words and works of Christ Jesus, 
                  who healed through prayer and demonstrated God's constant love for humanity.
                </p>
                <p className="text-lg text-muted leading-relaxed">
                  Mary Baker Eddy discovered Christian Science through her study of the Bible and wrote "Science and Health with Key to the Scriptures" 
                  to explain the spiritual laws that make healing possible for everyone.
                </p>
              </div>

              <div className="soft-card p-8 shadow-soft fade-up fade-delay-160">
                <h2 className="text-3xl font-bold text-primary mb-4">Available to Everyone</h2>
                <p className="text-lg text-muted leading-relaxed">
                  Christian Science treatment can address any challenge—physical, emotional, financial, or relational. 
                  The healing doesn't depend on your religious background or level of spiritual understanding. 
                  It's available to anyone who is open to discovering their spiritual identity and experiencing God's love.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="callout-banner text-center fade-up">
              <h3 className="callout-banner__title">Ready to Experience Healing?</h3>
              <p className="callout-banner__quote">
                "Divine Love always has met and always will meet every human need."
              </p>
              <p className="callout-banner__aside mb-6">
                — Mary Baker Eddy, Science and Health with Key to the Scriptures
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/booking" className="btn-gradient">Schedule Free Consultation</Link>
                <Link to="/contact" className="btn-outline">Get in Touch</Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default SpiritualHealing;

