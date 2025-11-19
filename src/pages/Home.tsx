import { Link } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const Home = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main>
        {/* Hero Section */}
        <section className="relative min-h-[500px] flex items-center justify-center bg-gradient-to-br from-blue-50 to-green-50">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Prayer Opens the Door to Divine Healing
            </h1>
            <p className="text-xl text-gray-700 mb-8 max-w-2xl mx-auto">
              Christian Science treatment supports you through life's challenges with compassion and spiritual care.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/booking" 
                className="inline-block bg-green-700 text-white px-8 py-4 rounded-lg font-semibold hover:bg-green-800 transition-colors"
              >
                Schedule Free Consultation
              </Link>
              <Link 
                to="/services" 
                className="inline-block bg-white text-green-700 border-2 border-green-700 px-8 py-4 rounded-lg font-semibold hover:bg-green-50 transition-colors"
              >
                Learn About Services
              </Link>
            </div>
          </div>
        </section>

        {/* Welcome Section */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Finding Peace Through Prayer
            </h2>
            <p className="text-lg text-gray-700 leading-relaxed">
              For over 20 years, I've helped people discover the healing power of God's love. Whether you're facing physical challenges, emotional struggles, or spiritual questions, Christian Science treatment offers a path to lasting peace and well-being.
            </p>
          </div>
        </section>

        {/* Services Overview */}
        <section className="py-16 px-4 bg-gray-50">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">How I Can Help</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white p-8 rounded-lg shadow-sm">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Physical Healing</h3>
                <p className="text-gray-700">
                  Prayer-based treatment for physical conditions, recognizing the spiritual nature of being.
                </p>
              </div>
              <div className="bg-white p-8 rounded-lg shadow-sm">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Mental & Emotional Support</h3>
                <p className="text-gray-700">
                  Support for mental health challenges, anxiety, and emotional difficulties through spiritual understanding.
                </p>
              </div>
              <div className="bg-white p-8 rounded-lg shadow-sm">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Life Guidance</h3>
                <p className="text-gray-700">
                  Help with relationship issues, employment concerns, and other life challenges.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-green-700 text-white">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-6">
              Ready to Begin Your Healing Journey?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Schedule a free consultation to discuss how Christian Science treatment can help you.
            </p>
            <Link 
              to="/booking" 
              className="inline-block bg-white text-green-700 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              Book Your Session
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
