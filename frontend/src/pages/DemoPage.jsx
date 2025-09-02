import React, { useState } from 'react';

const DemoPage = () => {
    const [message, setMessage] = useState('');

    const handleClick = () => {
        setMessage('Welcome to the Demo Page!');
    };

    return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
            <h1>Demo Page</h1>
            <button onClick={handleClick}>Show Message</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default DemoPage;