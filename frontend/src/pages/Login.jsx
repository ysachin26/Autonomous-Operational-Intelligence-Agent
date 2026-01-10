import { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Eye, EyeOff, ArrowRight, Sparkles } from 'lucide-react';
import api from '../services/api';

export default function Login({ onLogin }) {
    const [isLogin, setIsLogin] = useState(true);
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        name: '',
        organizationName: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
            const payload = isLogin
                ? { email: formData.email, password: formData.password }
                : formData;

            const response = await api.post(endpoint, payload);

            if (response.data.success) {
                onLogin(response.data.data.user, response.data.data.token);
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Authentication failed');
        } finally {
            setIsLoading(false);
        }
    };

    const handleDemoLogin = async () => {
        setError('');
        setIsLoading(true);

        try {
            const response = await api.post('/api/auth/login', {
                email: 'admin@acme.com',
                password: 'demo123456',
            });

            if (response.data.success) {
                onLogin(response.data.data.user, response.data.data.token);
            }
        } catch (err) {
            setError('Demo login failed. Please ensure the backend is running and database is seeded.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-dark-950 flex">
            {/* Left side - Branding */}
            <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-primary-900/50 via-dark-900 to-accent-900/30" />

                {/* Animated background elements */}
                <div className="absolute inset-0 overflow-hidden">
                    <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary-500/20 rounded-full blur-3xl animate-float" />
                    <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }} />
                </div>

                <div className="relative z-10 flex flex-col justify-center px-12 lg:px-20">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <div className="flex items-center gap-4 mb-8">
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center glow-primary">
                                <Brain className="w-10 h-10 text-white" />
                            </div>
                            <div>
                                <h1 className="text-4xl font-display font-bold gradient-text">AOIA</h1>
                                <p className="text-dark-300">Autonomous Operational Intelligence</p>
                            </div>
                        </div>

                        <h2 className="text-3xl lg:text-4xl font-display font-bold text-white mb-6 leading-tight">
                            Turn invisible operational loss into{' '}
                            <span className="gradient-text">measurable intelligence</span>
                        </h2>

                        <p className="text-lg text-dark-300 mb-8 max-w-md">
                            The world's first autonomous operations brain that detects inefficiencies,
                            calculates monetary impact, and triggers optimizations automatically.
                        </p>

                        <div className="space-y-4">
                            {[
                                'Real-time anomaly detection',
                                'AI-powered root cause analysis',
                                'Automatic loss quantification',
                                'Autonomous optimization actions',
                            ].map((feature, i) => (
                                <motion.div
                                    key={feature}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.3 + i * 0.1 }}
                                    className="flex items-center gap-3"
                                >
                                    <div className="w-6 h-6 rounded-full bg-primary-500/20 flex items-center justify-center">
                                        <Sparkles className="w-3 h-3 text-primary-400" />
                                    </div>
                                    <span className="text-dark-200">{feature}</span>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Right side - Auth form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="w-full max-w-md"
                >
                    {/* Mobile logo */}
                    <div className="lg:hidden flex items-center justify-center gap-3 mb-8">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                            <Brain className="w-7 h-7 text-white" />
                        </div>
                        <h1 className="text-2xl font-display font-bold gradient-text">AOIA</h1>
                    </div>

                    <div className="glass-card">
                        <div className="text-center mb-8">
                            <h2 className="text-2xl font-display font-bold text-white mb-2">
                                {isLogin ? 'Welcome back' : 'Create your account'}
                            </h2>
                            <p className="text-dark-400">
                                {isLogin
                                    ? 'Sign in to access your operational intelligence dashboard'
                                    : 'Start detecting and eliminating operational inefficiencies'}
                            </p>
                        </div>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm"
                            >
                                {error}
                            </motion.div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-5">
                            {!isLogin && (
                                <>
                                    <div>
                                        <label className="block text-sm font-medium text-dark-300 mb-2">
                                            Your Name
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                            className="input"
                                            placeholder="John Smith"
                                            required={!isLogin}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-dark-300 mb-2">
                                            Organization Name
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.organizationName}
                                            onChange={(e) => setFormData({ ...formData, organizationName: e.target.value })}
                                            className="input"
                                            placeholder="Acme Inc."
                                            required={!isLogin}
                                        />
                                    </div>
                                </>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-dark-300 mb-2">
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="input"
                                    placeholder="you@company.com"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-dark-300 mb-2">
                                    Password
                                </label>
                                <div className="relative">
                                    <input
                                        type={showPassword ? 'text' : 'password'}
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                        className="input pr-12"
                                        placeholder="••••••••"
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-white"
                                    >
                                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                    </button>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="btn-primary w-full justify-center py-3 text-base"
                            >
                                {isLoading ? (
                                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                ) : (
                                    <>
                                        {isLogin ? 'Sign In' : 'Create Account'}
                                        <ArrowRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>
                        </form>

                        <div className="mt-6">
                            <div className="relative">
                                <div className="absolute inset-0 flex items-center">
                                    <div className="w-full border-t border-dark-700" />
                                </div>
                                <div className="relative flex justify-center text-sm">
                                    <span className="px-4 bg-dark-900 text-dark-400">or</span>
                                </div>
                            </div>

                            <button
                                type="button"
                                onClick={handleDemoLogin}
                                disabled={isLoading}
                                className="btn-secondary w-full justify-center py-3 mt-6"
                            >
                                <Sparkles className="w-5 h-5 text-primary-400" />
                                Try Demo Account
                            </button>
                        </div>

                        <p className="mt-6 text-center text-sm text-dark-400">
                            {isLogin ? "Don't have an account? " : 'Already have an account? '}
                            <button
                                type="button"
                                onClick={() => setIsLogin(!isLogin)}
                                className="text-primary-400 hover:text-primary-300 font-medium"
                            >
                                {isLogin ? 'Sign up' : 'Sign in'}
                            </button>
                        </p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
