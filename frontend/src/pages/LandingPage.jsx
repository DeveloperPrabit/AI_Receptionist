import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
// import './LandingPage.css';

const LandingPage = () => {
  const { currentUser } = useAuth();

  return (
    <div className="landing-page">
      <section className="hero">
        <div className="hero-content">
          <h1>AI Receptionist</h1>
          <p>Transform your customer interactions with our intelligent virtual receptionist</p>
          <div className="hero-buttons">
            {currentUser ? (
              <Link to="/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary">
                  Get Started
                </Link>
                <Link to="/demo" className="btn btn-secondary">
                  Watch Demo
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2>Key Features</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📞</div>
              <h3>AI-Powered Calls</h3>
              <p>Answer calls with natural voice, understand caller intent, and transfer to human agents when needed.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">✉️</div>
              <h3>Smart Email Handling</h3>
              <p>Read, analyze, and respond to emails automatically with context-aware replies.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📅</div>
              <h3>Appointment Management</h3>
              <p>Schedule, reschedule, and manage appointments with calendar integration.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💳</div>
              <h3>Payment Processing</h3>
              <p>Handle payments and subscriptions with Stripe and PayPal integration.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta">
        <div className="container">
          <h2>Ready to Get Started?</h2>
          <p>Join thousands of businesses using our AI Receptionist</p>
          <Link to="/plans" className="btn btn-primary">
            View Plans
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;