import Header from "@/components/Header";
import Footer from "@/components/Footer";

const About = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-warm-50 via-white to-warm-100">
      <Header />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <h1 className="font-display text-4xl md:text-5xl font-bold text-warm-800 mb-8 text-center">
              My Search for Answers
            </h1>
          </div>
        </section>

        {/* About Content */}
        <section className="py-16 px-4 bg-white">
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-12 items-center mb-16">
              <div>
                <img 
                  src="/susan-about.jpg" 
                  alt="Susan Tish - Christian Science Practitioner" 
                  className="rounded-lg shadow-xl w-full"
                />
              </div>
              <div className="space-y-6">
                <p className="text-warm-700 leading-relaxed">
                  Searching for the deeper meaning, the underlying truth of things, has been a lifelong pursuit. Studying Christian Science as a youth, I found my questions increasingly answered through this unique theology and practice of spiritual healing.
                </p>
                <p className="text-warm-700 leading-relaxed">
                  The more I learned, the more I experienced healing through prayer, the more I wanted to help others find the same freedom and joy.
                </p>
              </div>
            </div>

            <div className="prose prose-lg max-w-none space-y-6 text-warm-700">
              <h2 className="font-display text-3xl font-bold text-warm-800 mb-6">My Journey</h2>
              
              <p>
                In 2001, I left a successful corporate career to become a full-time Christian Science practitioner. This decision was born from a deep conviction that spiritual healing is not only possible but essential in our modern world.
              </p>

              <p>
                Over the past two decades, I have witnessed countless healings - from physical ailments to mental and emotional challenges. Each healing has deepened my understanding and strengthened my conviction in the power of divine Love.
              </p>

              <h2 className="font-display text-3xl font-bold text-warm-800 mb-6 mt-12">My Practice</h2>
              
              <p>
                My practice is rooted in the teachings of Christian Science, which emphasizes the spiritual nature of reality and the power of divine Truth to heal. Through prayer-based treatment, I help individuals discover their inherent spiritual nature and experience healing.
              </p>

              <p>
                I work with people from all walks of life, addressing a wide range of challenges including physical illness, mental health issues, relationship difficulties, and spiritual questions. Each case is approached with compassion, confidentiality, and a deep trust in divine Love's healing power.
              </p>

              <h2 className="font-display text-3xl font-bold text-warm-800 mb-6 mt-12">Education & Training</h2>
              
              <p>
                I completed Primary class instruction with the Board of Education of The Mother Church, The First Church of Christ, Scientist, in Boston, Massachusetts. I continue my study and practice under the guidance of experienced teachers and through ongoing education in Christian Science.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-warm-600 to-warm-700">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Begin Your Healing Journey?
            </h2>
            <p className="text-warm-100 text-lg mb-8 max-w-2xl mx-auto">
              I'm here to support you through prayer-based Christian Science treatment. Let's connect and explore how spiritual healing can help you.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="/booking" 
                className="inline-block bg-white text-warm-700 px-8 py-4 rounded-lg font-semibold hover:bg-warm-50 transition-colors"
              >
                Schedule a Session
              </a>
              <a 
                href="/contact" 
                className="inline-block bg-warm-800 text-white px-8 py-4 rounded-lg font-semibold hover:bg-warm-900 transition-colors"
              >
                Contact Me
              </a>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default About;
