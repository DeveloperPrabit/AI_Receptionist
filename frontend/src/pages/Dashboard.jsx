import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Dashboard = () => {
  const { currentUser } = useAuth();
  const [activeTab, setActiveTab] = useState('calls');
  const [callRecords, setCallRecords] = useState([]);
  const [emails, setEmails] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  // Stats state
  const [stats, setStats] = useState({
    totalCalls: 0,
    totalEmails: 0,
    appointmentsToday: 0,
    urgentItems: 0,
  });

  // Fetch stats once on mount
  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const callsResponse = await api.get('/api/calls/');
      const emailsResponse = await api.get('/api/emails/');
      const appointmentsResponse = await api.get('/api/appointments/');

      const today = new Date().toISOString().split('T')[0];

      const appointmentsToday = appointmentsResponse.data.filter(
        apt => apt.start_time.startsWith(today)
      ).length;

      const urgentEmails = emailsResponse.data.filter(
        email => email.category === 'urgent'
      ).length;

      setStats({
        totalCalls: callsResponse.data.length,
        totalEmails: emailsResponse.data.length,
        appointmentsToday,
        urgentItems: urgentEmails,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Fetch tab-specific data
  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    try {
      setLoading(true);
      let response;

      switch (activeTab) {
        case 'calls':
          response = await api.get('/api/calls/');
          setCallRecords(response.data);
          break;
        case 'emails':
          response = await api.get('/api/emails/');
          setEmails(response.data);
          break;
        case 'appointments':
          response = await api.get('/api/appointments/');
          setAppointments(response.data);
          break;
        default:
          break;
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderTabContent = () => {
    if (loading) {
      return <div className="loading">Loading...</div>;
    }

    switch (activeTab) {
      case 'calls':
        return (
          <div className="tab-content">
            <h3>Call History</h3>
            {callRecords.length === 0 ? (
              <p>No call records found.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Caller ID</th>
                    <th>Duration</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {callRecords.map((call) => (
                    <tr key={call.id}>
                      <td>{call.caller_id}</td>
                      <td>{call.duration}</td>
                      <td>{call.status}</td>
                      <td>{new Date(call.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        );
      case 'emails':
        return (
          <div className="tab-content">
            <h3>Email Inbox</h3>
            {emails.length === 0 ? (
              <p>No emails found.</p>
            ) : (
              <div className="email-list">
                {emails.map((email) => (
                  <div key={email.id} className="email-item">
                    <div className="email-header">
                      <span className="email-sender">{email.sender}</span>
                      <span className="email-date">
                        {new Date(email.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="email-subject">{email.subject}</div>
                    <div className="email-preview">{email.body.substring(0, 100)}...</div>
                    <div className="email-category">Category: {email.category}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      case 'appointments':
        return (
          <div className="tab-content">
            <h3>Appointments</h3>
            {appointments.length === 0 ? (
              <p>No appointments found.</p>
            ) : (
              <div className="appointment-list">
                {appointments.map((appointment) => (
                  <div key={appointment.id} className="appointment-item">
                    <div className="appointment-title">{appointment.title}</div>
                    <div className="appointment-time">
                      {new Date(appointment.start_time).toLocaleString()} -{' '}
                      {new Date(appointment.end_time).toLocaleString()}
                    </div>
                    <div className="appointment-status">Status: {appointment.status}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome, {currentUser?.user?.first_name || currentUser?.user?.username}!</h1>
        <p>Manage your AI Receptionist settings and view activity.</p>
      </div>

      {/* Stats Overview */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📞</div>
          <div className="stat-content">
            <h3>{stats.totalCalls}</h3>
            <p>Total Calls</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✉️</div>
          <div className="stat-content">
            <h3>{stats.totalEmails}</h3>
            <p>Emails Processed</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>{stats.appointmentsToday}</h3>
            <p>Today's Appointments</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>{stats.urgentItems}</h3>
            <p>Urgent Items</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="dashboard-tabs">
        <button
          className={activeTab === 'calls' ? 'tab-button active' : 'tab-button'}
          onClick={() => setActiveTab('calls')}
        >
          Calls
        </button>
        <button
          className={activeTab === 'emails' ? 'tab-button active' : 'tab-button'}
          onClick={() => setActiveTab('emails')}
        >
          Emails
        </button>
        <button
          className={activeTab === 'appointments' ? 'tab-button active' : 'tab-button'}
          onClick={() => setActiveTab('appointments')}
        >
          Appointments
        </button>
        <button
          className={activeTab === 'settings' ? 'tab-button active' : 'tab-button'}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </div>

      <div className="dashboard-content">{renderTabContent()}</div>
    </div>
  );
};

export default Dashboard;
