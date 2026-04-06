import { useEffect, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import logo from '../assets/reckonlight-logo.svg';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/scenarios', label: 'Scenarios' },
  { to: '/about', label: 'About' },
];

export default function Layout({ children }) {
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [connectionStatus, setConnectionStatus] = useState('Live');
  const [highContrast, setHighContrast] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setLastUpdated(new Date());
      setConnectionStatus('Live');
    }, 360000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    document.body.classList.toggle('high-contrast', highContrast);
    return () => document.body.classList.remove('high-contrast');
  }, [highContrast]);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <header className="site-header">
        <div className="container nav-wrap">
          <div>
            <Link className="brand brand-with-logo" to="/">
              <img src={logo} alt="" className="brand-logo" aria-hidden="true" />
              <span>When the Last Light Fades</span>
            </Link>
            <p className="brand-subtitle">End of the Human World · Global Disaster Monitor</p>
          </div>
          <nav aria-label="Primary">
            <ul className="nav-list">
              {navItems.map((item) => (
                <li key={item.to}>
                  <NavLink to={item.to} className={({ isActive }) => (isActive ? 'active' : '')}>
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
          <p className="status-indicator" aria-live="polite">
            <span className="status-dot" /> {connectionStatus} Data
          </p>
          <button className="contrast-toggle" type="button" onClick={() => setHighContrast((v) => !v)}>
            {highContrast ? 'Standard Contrast' : 'High Contrast'}
          </button>
        </div>
      </header>
      <main id="main-content" className="container">
        {children}
      </main>
      <footer className="site-footer">
        <p>
          Data Source: Global Disaster Alert and Coordination System (GDACS) — a cooperation framework between the
          United Nations, the European Commission and disaster managers worldwide. <Link to="/about">About Project</Link>
        </p>
        <p>Update Frequency: Every 6 minutes.</p>
        <p>Updated: {lastUpdated.toUTCString()}</p>
        <p>
          The information presented here is indicative and should not be used for emergency decision-making without
          verification from official sources. This dashboard is an educational and contemplative tool for understanding
          global disaster patterns.
        </p>
        <p>
          In documenting the world&apos;s most challenging moments, we seek not to sensationalize suffering, but to foster
          deeper understanding of shared vulnerability.
        </p>
      </footer>
    </div>
  );
}
