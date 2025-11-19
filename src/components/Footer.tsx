import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="text-white mt-16 border-t footer-gradient">
      <div className="layout-shell layout-shell--wide section-pad--compact">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <h3 className="text-3xl font-bold mb-2">Susan Tish, CS</h3>
            <p className="text-gray-300 mb-4 text-lg">Christian Science Practitioner</p>
            <p className="text-gray-400 mb-6">
              Providing spiritual healing services worldwide for over 20 years. Helping people find lasting health and well-being through prayer-based treatment.
            </p>
            <div className="flex gap-2">
              <span className="badge-solid-sage">20+ Years Experience</span>
              <span className="badge-solid-mint">Worldwide Service</span>
            </div>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-3">
              <li><Link to="/" className="text-gray-300 hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/about" className="text-gray-300 hover:text-white transition-colors">About</Link></li>
              <li><Link to="/services" className="text-gray-300 hover:text-white transition-colors">Services</Link></li>
              <li><Link to="/inspiration" className="text-gray-300 hover:text-white transition-colors">Resources</Link></li>
              <li><Link to="/contact" className="text-gray-300 hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Contact</h3>
            <ul className="space-y-3 text-gray-300">
              <li><a href="mailto:susantishcs@gmail.com" className="hover:text-white transition-colors">susantishcs@gmail.com</a></li>
              <li><a href="tel:734-693-5946" className="hover:text-white transition-colors">734-693-5946</a></li>
              <li>Skype: susantishcs</li>
            </ul>
            <p className="text-gray-400 text-sm mt-4">Response within 24 hours</p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-12 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Susan Tish. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
