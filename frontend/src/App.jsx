import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Incidents from './pages/Incidents';
import Agent from './pages/Agent';
import Settings from './pages/Settings';

// Demo user for testing (authentication bypassed)
const demoUser = {
    id: 'demo-user-1',
    email: 'admin@acme.com',
    name: 'Demo Admin',
    role: 'ADMIN',
    organization: {
        id: 'demo-org-1',
        name: 'Acme Manufacturing Co.',
        industry: 'MANUFACTURING',
    },
};

function App() {
    const [user] = useState(demoUser);

    const handleLogout = () => {
        // For demo, just refresh the page
        window.location.reload();
    };

    return (
        <Router>
            <Layout user={user} onLogout={handleLogout}>
                <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/analytics" element={<Analytics />} />
                    <Route path="/incidents" element={<Incidents />} />
                    <Route path="/agent" element={<Agent />} />
                    <Route path="/settings" element={<Settings user={user} />} />
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;

