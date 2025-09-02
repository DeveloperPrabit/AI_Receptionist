import React from 'react';
import RegisterForm from '../components/RegisterForm';
// import './RegisterPage.css';

const RegisterPage = () => {
  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-hero">
          <h1>Join Us Today</h1>
          <p>Create an account to start using our AI Receptionist</p>
        </div>
        <RegisterForm />
      </div>
    </div>
  );
};

export default RegisterPage;