import Header from "@/components/Header";
import Footer from "@/components/Footer";

const Contact = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-warm-50 via-white to-warm-100">
      <Header />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="font-display text-4xl md:text-5xl font-bold text-warm-800 mb-6">
              Get in Touch
            </h1>
            <p className="text-xl text-warm-600 max-w-2xl mx-auto">
              I'm here to answer your questions and support you on your healing journey
            </p>
          </div>
        </section>

        {/* Contact Content */}
        <section className="py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <div className="grid md:grid-cols-2 gap-12">
              {/* Contact Information */}
              <div className="space-y-8">
                <div>
                  <h2 className="font-display text-2xl font-bold text-warm-800 mb-6">Contact Information</h2>
                  <div className="space-y-4">
                    <div className="flex items-start space-x-4">
                      <div className="w-10 h-10 bg-warm-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-warm-800 mb-1">Email</h3>
                        <a href="mailto:susantishcs@gmail.com" className="text-warm-600 hover:text-warm-700">
                          susantishcs@gmail.com
                        </a>
                      </div>
                    </div>

                    <div className="flex items-start space-x-4">
                      <div className="w-10 h-10 bg-warm-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-warm-800 mb-1">Phone</h3>
                        <a href="tel:+17346935946" className="text-warm-600 hover:text-warm-700">
                          734-693-5946
                        </a>
                      </div>
                    </div>

                    <div className="flex items-start space-x-4">
                      <div className="w-10 h-10 bg-warm-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-warm-800 mb-1">Skype</h3>
                        <span className="text-warm-600">susantishcs</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-warm-50 p-6 rounded-xl">
                  <h3 className="font-display text-xl font-bold text-warm-800 mb-3">Office Hours</h3>
                  <p className="text-warm-700 mb-4">
                    I'm available by appointment. Feel free to reach out anytime, and I'll respond as soon as possible.
                  </p>
                  <p className="text-warm-700">
                    <strong>Appointments available:</strong><br />
                    Monday - Sunday, flexible scheduling
                  </p>
                </div>
              </div>

              {/* Contact Form */}
              <div className="bg-white p-8 rounded-xl shadow-lg">
                <h2 className="font-display text-2xl font-bold text-warm-800 mb-6">Send a Message</h2>
                <form className="space-y-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-semibold text-warm-800 mb-2">
                      Your Name <span className="text-warm-500">*</span>
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      className="w-full px-4 py-3 border border-warm-200 rounded-lg focus:ring-2 focus:ring-warm-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label htmlFor="email" className="block text-sm font-semibold text-warm-800 mb-2">
                      Your Email <span className="text-warm-500">*</span>
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      className="w-full px-4 py-3 border border-warm-200 rounded-lg focus:ring-2 focus:ring-warm-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label htmlFor="subject" className="block text-sm font-semibold text-warm-800 mb-2">
                      Subject
                    </label>
                    <input
                      type="text"
                      id="subject"
                      name="subject"
                      className="w-full px-4 py-3 border border-warm-200 rounded-lg focus:ring-2 focus:ring-warm-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label htmlFor="message" className="block text-sm font-semibold text-warm-800 mb-2">
                      Your Message <span className="text-warm-500">*</span>
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      rows={6}
                      required
                      className="w-full px-4 py-3 border border-warm-200 rounded-lg focus:ring-2 focus:ring-warm-500 focus:border-transparent"
                    ></textarea>
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-warm-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-warm-700 transition-colors"
                  >
                    Send Message
                  </button>

                  <p className="text-sm text-warm-600 text-center">
                    All information shared is completely confidential
                  </p>
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
