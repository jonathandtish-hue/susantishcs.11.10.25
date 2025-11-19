import { useState, FormEvent } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Contact = () => {
  const [formStatus, setFormStatus] = useState<"idle" | "success" | "error">("idle");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    
    try {
      const response = await fetch("https://formspree.io/f/YOUR_FORM_ID", {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });
      
      if (response.ok) {
        setFormStatus("success");
        form.reset();
      } else {
        setFormStatus("error");
      }
    } catch (error) {
      setFormStatus("error");
    }
  };

  return (
    <div className="bg-page">
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 btn-gradient">
        Skip to main content
      </a>
      
      <Header />
      
      <main id="main-content">
        <section className="section-flow section-flow--clear">
          <div className="layout-shell layout-shell--narrow">
            <div className="section-intro">
              <span className="section-eyebrow">Reach Out</span>
              <h1 className="text-4xl font-bold leading-tight text-primary">Contact Me</h1>
              <p className="text-lg text-muted max-w-2xl mx-auto">
                Ready to begin your healing journey? I warmly offer a complimentary 15-minute conversation to answer questions and listen to your needs.
              </p>
            </div>
          </div>
        </section>

        <section className="section-flow section-flow--sage">
          <div className="layout-shell layout-shell--edge">
            <div className="contact-panels">
              <div className="contact-panel contact-panel--accent fade-up fade-delay-60">
                <h2 className="text-3xl font-bold leading-tight mb-4">Get in Touch</h2>
                <p className="contact-panel__meta">I typically respond within 24 hours. For urgent support, call and leave a message—I'll reach you as quickly as possible.</p>
                <div className="contact-panel__list mt-6">
                  <div className="contact-panel__item">
                    <span className="contact-panel__avatar">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                      </svg>
                    </span>
                    <div>
                      <span className="contact-panel__label">Email (Preferred)</span>
                      <a href="mailto:susantishcs@gmail.com" className="flow-card__link">susantishcs@gmail.com</a>
                    </div>
                  </div>
                  <div className="contact-panel__item">
                    <span className="contact-panel__avatar">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                      </svg>
                    </span>
                    <div>
                      <span className="contact-panel__label">Phone</span>
                      <a href="tel:734-693-5946" className="flow-card__link">734-693-5946</a>
                      <p className="contact-panel__meta">Leave a message and I'll return your call promptly.</p>
                    </div>
                  </div>
                  <div className="contact-panel__item">
                    <span className="contact-panel__avatar">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                      </svg>
                    </span>
                    <div>
                      <span className="contact-panel__label">Skype</span>
                      <span className="contact-panel__meta">susantishcs &mdash; video sessions available</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="contact-panel fade-up fade-delay-120">
                <h3 className="text-2xl font-bold mb-5 leading-tight text-primary">Send a Message</h3>
                
                {formStatus === "success" && (
                  <div className="mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-lg" role="status" aria-live="polite">
                    <div className="flex items-start">
                      <svg className="w-6 h-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                      </svg>
                      <div>
                        <h4 className="text-green-800 font-bold">Message sent successfully!</h4>
                        <p className="text-green-700">Thank you for reaching out. I'll respond within 24 hours.</p>
                      </div>
                    </div>
                  </div>
                )}

                {formStatus === "error" && (
                  <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg" role="alert" aria-live="assertive">
                    <div className="flex items-start">
                      <svg className="w-6 h-6 text-red-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                      </svg>
                      <div>
                        <h4 className="text-red-800 font-bold">Something went wrong.</h4>
                        <p className="text-red-700">Please try again or email me directly at susantishcs@gmail.com.</p>
                      </div>
                    </div>
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                  <div>
                    <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">Your Name *</label>
                    <input type="text" id="name" name="name" required className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">Your Email *</label>
                    <input type="email" id="email" name="email" required className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  </div>
                  <div>
                    <label htmlFor="phone" className="block text-sm font-semibold text-gray-700 mb-2">Phone Number (Optional)</label>
                    <input type="tel" id="phone" name="phone" className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                  </div>
                  <div>
                    <label htmlFor="message" className="block text-sm font-semibold text-gray-700 mb-2">Tell me about your needs *</label>
                    <textarea id="message" name="message" rows={5} required placeholder="What brings you here today? What challenges are you facing?" className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"></textarea>
                  </div>
                  <input type="text" name="_gotcha" className="hidden" />
                  <button type="submit" className="btn-gradient w-full">Send Message</button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Contact;

