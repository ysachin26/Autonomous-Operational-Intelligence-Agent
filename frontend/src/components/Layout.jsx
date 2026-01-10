import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    LayoutDashboard,
    BarChart3,
    AlertTriangle,
    MessageSquare,
    Settings,
    LogOut,
    Brain,
    Bell,
    Search,
    Menu,
    X,
} from 'lucide-react';
import { useState } from 'react';

const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Incidents', href: '/incidents', icon: AlertTriangle },
    { name: 'AI Agent', href: '/agent', icon: MessageSquare },
    { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Layout({ children, user, onLogout }) {
    const location = useLocation();
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [notifications] = useState([
        { id: 1, message: 'New anomaly detected on Machine 2', time: '2 min ago', type: 'warning' },
        { id: 2, message: 'Recommendation executed successfully', time: '15 min ago', type: 'success' },
    ]);
    const [showNotifications, setShowNotifications] = useState(false);

    return (
        <div className="min-h-screen bg-dark-950 flex">
            {/* Mobile sidebar overlay */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`fixed lg:static inset-y-0 left-0 z-50 w-72 bg-dark-900/80 backdrop-blur-xl border-r border-dark-700/50 transform transition-transform duration-300 lg:transform-none ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
                    }`}
            >
                <div className="flex flex-col h-full">
                    {/* Logo */}
                    <div className="p-6 border-b border-dark-700/50">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center glow-primary">
                                <Brain className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-xl font-display font-bold gradient-text">AOIA</h1>
                                <p className="text-xs text-dark-400">Operational Intelligence</p>
                            </div>
                        </div>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 p-4 space-y-1">
                        {navigation.map((item) => {
                            const isActive = location.pathname === item.href;
                            return (
                                <NavLink
                                    key={item.name}
                                    to={item.href}
                                    className={`sidebar-item ${isActive ? 'active' : ''}`}
                                    onClick={() => setSidebarOpen(false)}
                                >
                                    <item.icon className={`w-5 h-5 ${isActive ? 'text-primary-400' : ''}`} />
                                    <span>{item.name}</span>
                                    {isActive && (
                                        <motion.div
                                            layoutId="activeIndicator"
                                            className="absolute right-4 w-1.5 h-1.5 bg-primary-500 rounded-full"
                                        />
                                    )}
                                </NavLink>
                            );
                        })}
                    </nav>

                    {/* User section */}
                    <div className="p-4 border-t border-dark-700/50">
                        <div className="flex items-center gap-3 p-3 rounded-xl bg-dark-800/50">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-600 to-accent-600 flex items-center justify-center text-white font-semibold">
                                {user?.name?.charAt(0) || 'U'}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-white truncate">{user?.name || 'User'}</p>
                                <p className="text-xs text-dark-400 truncate">{user?.organization?.name || 'Organization'}</p>
                            </div>
                            <button
                                onClick={onLogout}
                                className="p-2 rounded-lg hover:bg-dark-700 text-dark-400 hover:text-white transition-colors"
                                title="Logout"
                            >
                                <LogOut className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main content */}
            <div className="flex-1 flex flex-col min-h-screen">
                {/* Top bar */}
                <header className="sticky top-0 z-30 bg-dark-950/80 backdrop-blur-xl border-b border-dark-700/50">
                    <div className="flex items-center justify-between px-4 lg:px-8 h-16">
                        {/* Mobile menu button */}
                        <button
                            className="lg:hidden p-2 rounded-lg hover:bg-dark-800 text-dark-400"
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                        >
                            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                        </button>

                        {/* Search */}
                        <div className="hidden md:flex items-center flex-1 max-w-md">
                            <div className="relative w-full">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-400" />
                                <input
                                    type="text"
                                    placeholder="Search operations, incidents..."
                                    className="w-full pl-10 pr-4 py-2 rounded-xl bg-dark-800/50 border border-dark-700 focus:border-primary-500 focus:ring-1 focus:ring-primary-500/20 outline-none text-sm text-white placeholder-dark-400 transition-all"
                                />
                            </div>
                        </div>

                        {/* Right side */}
                        <div className="flex items-center gap-4">
                            {/* Live indicator */}
                            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/30">
                                <span className="status-dot active" />
                                <span className="text-xs text-green-400 font-medium">Live</span>
                            </div>

                            {/* Notifications */}
                            <div className="relative">
                                <button
                                    onClick={() => setShowNotifications(!showNotifications)}
                                    className="relative p-2 rounded-lg hover:bg-dark-800 text-dark-400 hover:text-white transition-colors"
                                >
                                    <Bell className="w-5 h-5" />
                                    <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
                                </button>

                                {showNotifications && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="absolute right-0 mt-2 w-80 glass-card p-0 overflow-hidden"
                                    >
                                        <div className="p-4 border-b border-dark-700">
                                            <h3 className="font-semibold text-white">Notifications</h3>
                                        </div>
                                        <div className="max-h-64 overflow-y-auto">
                                            {notifications.map((notif) => (
                                                <div
                                                    key={notif.id}
                                                    className="p-4 border-b border-dark-700/50 hover:bg-dark-800/50 cursor-pointer"
                                                >
                                                    <p className="text-sm text-white">{notif.message}</p>
                                                    <p className="text-xs text-dark-400 mt-1">{notif.time}</p>
                                                </div>
                                            ))}
                                        </div>
                                        <div className="p-3 text-center">
                                            <button className="text-sm text-primary-400 hover:text-primary-300">
                                                View all notifications
                                            </button>
                                        </div>
                                    </motion.div>
                                )}
                            </div>
                        </div>
                    </div>
                </header>

                {/* Page content */}
                <main className="flex-1 p-4 lg:p-8">
                    <motion.div
                        key={location.pathname}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                    >
                        {children}
                    </motion.div>
                </main>
            </div>
        </div>
    );
}
