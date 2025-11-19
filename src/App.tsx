import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Services from "./pages/Services";
import Inspiration from "./pages/Inspiration";
import Contact from "./pages/Contact";
import Booking from "./pages/Booking";
import SpiritualHealing from "./pages/SpiritualHealing";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/services" element={<Services />} />
        <Route path="/inspiration" element={<Inspiration />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="/spiritual-healing" element={<SpiritualHealing />} />
      </Routes>
    </Router>
  );
}

export default App;
