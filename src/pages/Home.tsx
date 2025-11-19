const Home = () => {
  return (
    <div style={{ padding: '20px', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <h1 style={{ color: '#333', fontSize: '32px' }}>Susan Tish - Christian Science Practitioner</h1>
      <p style={{ color: '#666', fontSize: '18px', marginTop: '16px' }}>
        Welcome! The site is loading. If you see this, React is working.
      </p>
      <div style={{ marginTop: '24px' }}>
        <a href="/about" style={{ color: '#0066cc', marginRight: '16px' }}>About</a>
        <a href="/services" style={{ color: '#0066cc', marginRight: '16px' }}>Services</a>
        <a href="/contact" style={{ color: '#0066cc' }}>Contact</a>
      </div>
    </div>
  );
};

export default Home;
