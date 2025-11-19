import { Link, useLocation } from "react-router-dom";
import { useState } from "react";

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 border-b site-header">
      <div className="hidden lg:block fixed left-0 top-0 bottom-0 w-1 z-40 site-rail"></div>
      <div className="hidden lg:block fixed right-0 top-0 bottom-0 w-1 z-40 site-rail"></div>
      
      <nav className="max-w-7xl mx-auto px-5 sm:px-8 md:px-10 lg:px-12 xl:px-16">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center hover:opacity-80 transition-opacity">
              <img src="/susantish-logo.png" alt="Susan Tish, CS" className="logo-image" />
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            <Link to="/" className={`nav-link px-3 py-2 text-sm transition-all duration-300 ease-in-out ${isActive('/') ? 'text-[hsl(var(--sage))]' : ''}`}>
              Home
            </Link>
            <Link to="/about" className={`nav-link px-3 py-2 text-sm transition-all duration-300 ease-in-out ${isActive('/about') ? 'text-[hsl(var(--sage))]' : ''}`}>
              About
            </Link>
            <Link to="/services" className={`nav-link px-3 py-2 text-sm transition-all duration-300 ease-in-out ${isActive('/services') ? 'text-[hsl(var(--sage))]' : ''}`}>
              Services
            </Link>
            <Link to="/inspiration" className={`nav-link px-3 py-2 text-sm transition-all duration-300 ease-in-out ${isActive('/inspiration') ? 'text-[hsl(var(--sage))]' : ''}`}>
              Resources
            </Link>
            <Link to="/contact" className={`nav-link px-3 py-2 text-sm transition-all duration-300 ease-in-out ${isActive('/contact') ? 'text-[hsl(var(--sage))]' : ''}`}>
              Contact
            </Link>
            <Link to="/booking" className="ml-4 btn-gradient flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              Book Appointment
            </Link>
          </div>
          
          <div className="md:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? "Close navigation menu" : "Open navigation menu"}
              className="text-muted hover:text-sage focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-sage rounded-xl p-2 transition-all duration-300 ease-in-out"
            >
              {mobileMenuOpen ? (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              ) : (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              )}
            </button>
          </div>
        </div>
      </nav>
      
      {mobileMenuOpen && (
        <div className="md:hidden border-t site-header">
          <div className="px-5 sm:px-6 pt-2 pb-3 space-y-1">
            <Link to="/" className="block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out nav-link" onClick={() => setMobileMenuOpen(false)}>
              Home
            </Link>
            <Link to="/about" className="block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out nav-link" onClick={() => setMobileMenuOpen(false)}>
              About
            </Link>
            <Link to="/services" className="block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out nav-link" onClick={() => setMobileMenuOpen(false)}>
              Services
            </Link>
            <Link to="/inspiration" className="block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out nav-link" onClick={() => setMobileMenuOpen(false)}>
              Resources
            </Link>
            <Link to="/contact" className="block px-4 py-3 text-base rounded-xl transition-all duration-300 ease-in-out nav-link" onClick={() => setMobileMenuOpen(false)}>
              Contact
            </Link>
            <Link to="/booking" className="block btn-gradient text-base font-semibold rounded-xl transition-all duration-300 ease-in-out text-center mt-2" onClick={() => setMobileMenuOpen(false)}>
              <span className="inline-flex items-center justify-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span>Book Appointment</span>
              </span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
