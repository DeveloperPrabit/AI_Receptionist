import React from 'react';

const plans = [
    {
        name: 'Basic',
        price: '$19/mo',
        features: [
            '1 user',
            'Basic support',
            'Access to core features',
        ],
    },
    {
        name: 'Pro',
        price: '$49/mo',
        features: [
            '5 users',
            'Priority support',
            'Advanced analytics',
            'Custom integrations',
        ],
    },
    {
        name: 'Enterprise',
        price: 'Contact us',
        features: [
            'Unlimited users',
            'Dedicated support',
            'Custom solutions',
            'Onboarding assistance',
        ],
    },
];

const PlansPage = () => (
    <div style={{ padding: '2rem', maxWidth: 900, margin: '0 auto' }}>
        <h1>Choose Your Plan</h1>
        <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
            {plans.map((plan) => (
                <div
                    key={plan.name}
                    style={{
                        border: '1px solid #ddd',
                        borderRadius: 8,
                        padding: '1.5rem',
                        flex: '1 1 250px',
                        minWidth: 250,
                        background: '#fafafa',
                    }}
                >
                    <h2>{plan.name}</h2>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{plan.price}</p>
                    <ul>
                        {plan.features.map((feature) => (
                            <li key={feature}>{feature}</li>
                        ))}
                    </ul>
                    <button
                        style={{
                            marginTop: '1rem',
                            padding: '0.5rem 1.5rem',
                            borderRadius: 4,
                            border: 'none',
                            background: '#0078d4',
                            color: '#fff',
                            cursor: 'pointer',
                        }}
                    >
                        Select
                    </button>
                </div>
            ))}
        </div>
    </div>
);

export default PlansPage;