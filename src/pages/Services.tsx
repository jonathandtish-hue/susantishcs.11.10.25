import Header from "@/components/Header";
import Footer from "@/components/Footer";

const Services = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-warm-50 via-white to-warm-100">
      <Header />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="font-display text-4xl md:text-5xl font-bold text-warm-800 mb-6">
              Christian Science Healing & Treatment
            </h1>
            <p className="text-xl text-warm-600 max-w-3xl mx-auto">
              Prayer-based spiritual healing for any challenge including illness, mental health, and relationship or employment concerns
            </p>
          </div>
        </section>

        {/* Services Overview */}
        <section className="py-16 px-4 bg-white">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8 mb-16">
              <div className="p-8 bg-warm-50 rounded-xl">
                <div className="w-12 h-12 bg-warm-600 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h3 className="font-display text-2xl font-bold text-warm-800 mb-3">Physical Healing</h3>
                <p className="text-warm-700">
                  Treatment for physical conditions through prayer, recognizing the spiritual nature of being and the power of divine Love to heal.
                </p>
              </div>

              <div className="p-8 bg-warm-50 rounded-xl">
                <div className="w-12 h-12 bg-warm-600 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="font-display text-2xl font-bold text-warm-800 mb-3">Mental & Emotional</h3>
                <p className="text-warm-700">
                  Support for mental health challenges, anxiety, depression, and emotional difficulties through spiritual understanding.
                </p>
              </div>

              <div className="p-8 bg-warm-50 rounded-xl">
                <div className="w-12 h-12 bg-warm-600 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="font-display text-2xl font-bold text-warm-800 mb-3">Life Challenges</h3>
                <p className="text-warm-700">
                  Guidance for relationship issues, employment concerns, and other life challenges through prayer and spiritual insight.
                </p>
              </div>
            </div>

            {/* Detailed Information */}
            <div className="prose prose-lg max-w-none space-y-8">
              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">What is Christian Science Treatment?</h2>
                <p className="text-warm-700 leading-relaxed">
                  Christian Science treatment is prayer-based spiritual healing. It involves recognizing the spiritual truth about God and His creation, which includes you. This recognition of spiritual reality brings healing to physical, mental, and emotional challenges.
                </p>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">How Does It Work?</h2>
                <p className="text-warm-700 leading-relaxed">
                  When you request treatment, I pray specifically for you, recognizing your spiritual nature as God's perfect creation. This prayer is not petition or willpower, but rather a scientific understanding of spiritual law and divine Love's ever-presence. Healing occurs as this truth becomes clear in consciousness.
                </p>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">What to Expect</h2>
                <ul className="text-warm-700 space-y-3">
                  <li><strong>Confidential:</strong> All communications and treatment are completely confidential.</li>
                  <li><strong>Remote or In-Person:</strong> Treatment is effective whether we meet in person, by phone, or remotely.</li>
                  <li><strong>Ongoing Support:</strong> I provide continuous prayer support and am available to discuss your progress.</li>
                  <li><strong>No Diagnosis:</strong> Christian Science practice doesn't involve medical diagnosis or treatment - it's purely spiritual.</li>
                  <li><strong>Complementary:</strong> While some choose Christian Science treatment exclusively, others use it alongside conventional medical care.</li>
                </ul>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">Fees & Insurance</h2>
                <p className="text-warm-700 leading-relaxed">
                  Christian Science treatment is available to everyone regardless of financial situation. While there is a fee for services, it is flexible and based on your ability to pay. Some insurance plans cover Christian Science treatment - I can provide documentation for insurance claims.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-warm-600 to-warm-700">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-6">
              Begin Your Healing Today
            </h2>
            <p className="text-warm-100 text-lg mb-8 max-w-2xl mx-auto">
              Whether you're facing a health challenge, seeking spiritual growth, or need support with life's difficulties, I'm here to help through prayer-based treatment.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="/booking" 
                className="inline-block bg-white text-warm-700 px-8 py-4 rounded-lg font-semibold hover:bg-warm-50 transition-colors"
              >
                Schedule a Consultation
              </a>
              <a 
                href="/contact" 
                className="inline-block bg-warm-800 text-white px-8 py-4 rounded-lg font-semibold hover:bg-warm-900 transition-colors"
              >
                Ask a Question
              </a>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Services;
