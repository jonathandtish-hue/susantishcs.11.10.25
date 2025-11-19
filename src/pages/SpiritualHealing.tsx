import Header from "@/components/Header";
import Footer from "@/components/Footer";

const SpiritualHealing = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-warm-50 via-white to-warm-100">
      <Header />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="font-display text-4xl md:text-5xl font-bold text-warm-800 mb-6">
              What is Spiritual Healing?
            </h1>
            <p className="text-xl text-warm-600 max-w-3xl mx-auto">
              Understanding the power of prayer-based Christian Science treatment
            </p>
          </div>
        </section>

        {/* Content Section */}
        <section className="py-16 px-4 bg-white">
          <div className="max-w-4xl mx-auto prose prose-lg">
            <div className="space-y-8 text-warm-700">
              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">The Foundation</h2>
                <p className="leading-relaxed">
                  Spiritual healing through Christian Science is based on the understanding that God is infinite divine Love, and that this Love is always present and available to heal. It recognizes that our true nature is spiritual, not material, and that understanding this truth brings healing.
                </p>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">How It Works</h2>
                <p className="leading-relaxed">
                  Christian Science healing is prayer - but not prayer as petition or begging. It's prayer as recognition of spiritual truth. When we understand God's allness and goodness, and our spiritual nature as God's perfect creation, healing naturally occurs.
                </p>
                <p className="leading-relaxed">
                  This isn't positive thinking or mind over matter. It's a systematic, scientific understanding of divine law that has healed countless individuals over more than a century.
                </p>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">What Can Be Healed?</h2>
                <p className="leading-relaxed">
                  Christian Science treatment addresses all types of challenges:
                </p>
                <ul className="space-y-2 ml-6">
                  <li>Physical ailments and diseases</li>
                  <li>Mental and emotional difficulties</li>
                  <li>Relationship problems</li>
                  <li>Financial challenges</li>
                  <li>Life direction and purpose questions</li>
                  <li>Any situation where healing and transformation are needed</li>
                </ul>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">The Science Behind It</h2>
                <p className="leading-relaxed">
                  Christian Science is called a science because it's based on fixed, demonstrable spiritual laws - not on chance, luck, or special favor. Just as mathematical laws are reliable and consistent, spiritual laws operate with the same reliability.
                </p>
                <p className="leading-relaxed">
                  Mary Baker Eddy, who discovered and founded Christian Science in the 19th century, studied the Bible deeply and discovered the spiritual laws that Jesus Christ used in his healing works. These same laws are available and effective today.
                </p>
              </div>

              <div>
                <h2 className="font-display text-3xl font-bold text-warm-800 mb-4">Your Role in Healing</h2>
                <p className="leading-relaxed">
                  While a Christian Science practitioner prays for you and supports your healing, your own understanding and receptivity are important. Healing often involves:
                </p>
                <ul className="space-y-2 ml-6">
                  <li>Willingness to see yourself and your situation from a spiritual perspective</li>
                  <li>Openness to divine Love's healing presence</li>
                  <li>Study of Christian Science to deepen your understanding</li>
                  <li>Patience and persistence as spiritual understanding unfolds</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-warm-600 to-warm-700">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-6">
              Experience Healing Through Prayer
            </h2>
            <p className="text-warm-100 text-lg mb-8 max-w-2xl mx-auto">
              Ready to explore how Christian Science treatment can help you? I'm here to support your healing journey.
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
                Learn More
              </a>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default SpiritualHealing;
