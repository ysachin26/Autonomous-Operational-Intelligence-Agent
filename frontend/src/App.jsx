import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useState } from 'react';
import Layout from './components/Layout';
import { ActionProvider } from './components/ActionProvider';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Incidents from './pages/Incidents';
import Agent from './pages/Agent';
import Settings from './pages/Settings';
import Sales from './pages/Sales';
import LandingPage from './pages/LandingPage';

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

// Wrapper for the main app layout to use Outlet
const AppLayout = ({ user, onLogout }) => {
    return (
        <Layout user={user} onLogout={onLogout}>
            <Outlet />
        </Layout>
    );
};

function App() {
    const [user] = useState(demoUser);

    const handleLogout = () => {
        window.location.reload();
    };

    return (
        <ActionProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<LandingPage />} />

                    {/* Protected/App Routes */}
                    <Route element={<AppLayout user={user} onLogout={handleLogout} />}>
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/sales" element={<Sales />} />
                        <Route path="/analytics" element={<Analytics />} />
                        <Route path="/incidents" element={<Incidents />} />
                        <Route path="/agent" element={<Agent />} />
                        <Route path="/settings" element={<Settings user={user} />} />
                    </Route>

                    {/* Catch all - redirect to landing page */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Router>
        </ActionProvider>
    );
}

export default App;
