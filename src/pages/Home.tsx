import { Link } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { useEffect, useRef, useState } from "react";

const Home = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(true);

  const toggleVideo = () => {
    if (videoRef.current) {
      if (videoRef.current.paused) {
        videoRef.current.play();
        setIsPlaying(true);
      } else {
        videoRef.current.pause();
        setIsPlaying(false);
      }
    }
  };

  return (
    <div className="bg-page">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 btn-gradient">
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content">
        {/* Hero Section */}
        <section className="relative min-h-[600px] flex items-center justify-center overflow-hidden">
          <video
            ref={videoRef}
            autoPlay
            loop
            muted
            playsInline
            className="absolute inset-0 w-full h-full object-cover"
          >
            <source src="/ocean-waves.mp4" type="video/mp4" />
          </video>
          
          <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/40 to-transparent"></div>
          
          <button
            onClick={toggleVideo}
            aria-label={isPlaying ? "Pause background video" : "Play background video"}
            className="absolute bottom-8 right-8 z-20 bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-3 rounded-full transition-all duration-300"
          >
            {isPlaying ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            )}
          </button>
          
          <div className="relative z-10 layout-shell text-center text-white">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              Prayer Opens the Door<br />to Divine Healing
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto opacity-95">
              Christian Science treatment supports you through life's challenges with compassion, confidentiality, and unwavering spiritual care.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/booking" className="btn-gradient text-lg">Schedule Free Consultation</Link>
              <Link to="/services" className="px-6 py-3 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all duration-300 border-2 border-white/30">Learn About Services</Link>
            </div>
          </div>
        </section>

        {/* Welcome Section */}
        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow text-center">
            <span className="section-eyebrow">Welcome</span>
            <h2 className="text-4xl font-bold leading-tight text-primary mb-6">
              Finding Peace Through Prayer
            </h2>
            <p className="text-lg text-muted leading-relaxed mb-8">
              For over 20 years, I've helped people discover the healing power of God's love. Whether you're facing physical challenges, emotional struggles, or spiritual questions, Christian Science treatment offers a path to lasting peace and well-being.
            </p>
            <Link to="/about" className="btn-gradient">Discover My Journey</Link>
          </div>
        </section>

        {/* Services Overview */}
        <section className="section-flow section-flow--sage">
          <div className="layout-shell">
            <div className="text-center mb-12">
              <span className="section-eyebrow">How I Can Help</span>
              <h2 className="text-4xl font-bold leading-tight text-primary mb-4">
                Compassionate Spiritual Care
              </h2>
              <p className="text-lg text-muted max-w-2xl mx-auto">
                Every situation is unique. I offer personalized prayer-based treatment tailored to your specific needs.
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div className="flow-card fade-up">
                <h3 className="flow-card__title">Physical Healing</h3>
                <p className="flow-card__body">
                  Experience the transformative power of prayer for physical wellness. Many have found relief and healing through spiritual understanding.
                </p>
              </div>
              <div className="flow-card fade-up fade-delay-80">
                <h3 className="flow-card__title">Emotional Support</h3>
                <p className="flow-card__body">
                  Find comfort and strength during difficult times. Prayer brings peace, clarity, and renewed hope for the future.
                </p>
              </div>
              <div className="flow-card fade-up fade-delay-160">
                <h3 className="flow-card__title">Spiritual Growth</h3>
                <p className="flow-card__body">
                  Deepen your understanding of God's love and your spiritual identity. Discover lasting joy and purpose.
                </p>
              </div>
            </div>
            
            <div className="text-center mt-12">
              <Link to="/services" className="btn-gradient">Explore All Services</Link>
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="section-flow section-flow--clear">
          <div className="layout-shell">
            <div className="text-center mb-12">
              <span className="section-eyebrow">Testimonials</span>
              <h2 className="text-4xl font-bold leading-tight text-primary mb-4">
                Stories of Healing
              </h2>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div className="soft-card p-8 shadow-soft fade-up">
                <p className="text-lg italic text-muted mb-4">
                  "Susan's compassionate support helped me through one of the most challenging periods of my life. Her unwavering faith and gentle guidance brought me peace I didn't think possible."
                </p>
                <p className="font-semibold text-primary">— Sarah M.</p>
              </div>
              <div className="soft-card p-8 shadow-soft fade-up fade-delay-120">
                <p className="text-lg italic text-muted mb-4">
                  "The healing I experienced through Christian Science treatment exceeded all expectations. Susan's dedication and spiritual insight made all the difference."
                </p>
                <p className="font-semibold text-primary">— Robert T.</p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--narrow">
            <div className="callout-banner text-center fade-up">
              <h3 className="callout-banner__title">Ready to Begin Your Journey?</h3>
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

export default Home;
