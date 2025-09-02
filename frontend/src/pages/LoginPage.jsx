import React from 'react';
import LoginForm from '../components/LoginForm';
// import './LoginPage.css';

const LoginPage = () => {
  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-hero">
          <h1>Welcome Back</h1>
          <p>Sign in to access your AI Receptionist dashboard</p>
        </div>
        <LoginForm />
      </div>
    </div>
  );
};

export default LoginPage;