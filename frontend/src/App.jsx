import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Incidents from './pages/Incidents';
import Agent from './pages/Agent';
import Settings from './pages/Settings';
import Login from './pages/Login';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check for existing auth token
        const token = localStorage.getItem('aoia_token');
        const storedUser = localStorage.getItem('aoia_user');

        if (token && storedUser) {
            setIsAuthenticated(true);
            setUser(JSON.parse(storedUser));
        }
        setIsLoading(false);
    }, []);

    const handleLogin = (userData, token) => {
        localStorage.setItem('aoia_token', token);
        localStorage.setItem('aoia_user', JSON.stringify(userData));
        setUser(userData);
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        localStorage.removeItem('aoia_token');
        localStorage.removeItem('aoia_user');
        setUser(null);
        setIsAuthenticated(false);
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-dark-950 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
                    <p className="text-dark-400">Loading AOIA...</p>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Login onLogin={handleLogin} />;
    }

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
