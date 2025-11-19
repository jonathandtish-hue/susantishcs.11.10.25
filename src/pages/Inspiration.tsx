import Header from "@/components/Header";
import Footer from "@/components/Footer";

const Inspiration = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-warm-50 via-white to-warm-100">
      <Header />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="font-display text-4xl md:text-5xl font-bold text-warm-800 mb-6">
              Inspiration & Insights
            </h1>
            <p className="text-xl text-warm-600 max-w-2xl mx-auto">
              Thoughts on healing, spirituality, and Christian Science practice
            </p>
          </div>
        </section>

        {/* Content Section */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center py-20">
              <p className="text-warm-600 text-lg">
                Inspirational content coming soon. Check back for articles, insights, and thoughts on spiritual healing.
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Inspiration;
