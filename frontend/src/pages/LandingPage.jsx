import { useNavigate } from 'react-router-dom';
import {
    Bot,
    Cpu,
    BarChart3,
    ShieldCheck,
    Zap,
    Globe,
    ArrowRight,
    CheckCircle2
} from 'lucide-react';

export default function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-white">
            {/* Header/Nav */}
            <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
                                <span className="text-white font-bold text-sm">A</span>
                            </div>
                            <span className="text-xl font-bold text-gray-900">AOIA</span>
                        </div>
                        <nav className="hidden md:flex items-center gap-8">
                            <a href="#features" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">Features</a>
                            <a href="#solutions" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">Solutions</a>
                            <a href="#about" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">About</a>
                        </nav>
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200"
                        >
                            Get Started
                        </button>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-28 overflow-hidden">
                <div className="absolute inset-0 z-0">
                    <div className="absolute top-0 right-0 w-1/2 h-full bg-primary-50/50 rounded-l-[100px] transform skew-x-6"></div>
                    <div className="absolute bottom-0 left-0 w-64 h-64 bg-accent-50/50 rounded-full blur-3xl"></div>
                </div>

                <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="lg:grid lg:grid-cols-2 lg:gap-16 items-center">
                        <div>
                            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-100 text-primary-700 text-sm font-semibold mb-6">
                                <Bot className="w-4 h-4" />
                                <span>Future of Operations</span>
                            </div>
                            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
                                Autonomous <span className="text-primary-600">Operational Intelligence</span> Agent
                            </h1>
                            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                                Transform your business operations with AI-driven insights, automated incident response, and predictive analytics.
                                The intelligent agent that never sleeps.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4">
                                <button
                                    onClick={() => navigate('/dashboard')}
                                    className="inline-flex items-center justify-center px-8 py-3 text-base font-semibold text-white bg-primary-600 rounded-xl hover:bg-primary-700 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200"
                                >
                                    Launch Dashboard
                                    <ArrowRight className="ml-2 w-5 h-5" />
                                </button>
                                <button className="inline-flex items-center justify-center px-8 py-3 text-base font-semibold text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all duration-200">
                                    View Demo
                                </button>
                            </div>
                            <div className="mt-8 flex items-center gap-6 text-sm text-gray-500">
                                <div className="flex items-center gap-2">
                                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                                    <span>No credit card required</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                                    <span>Instant setup</span>
                                </div>
                            </div>
                        </div>
                        <div className="mt-16 lg:mt-0 relative">
                            <div className="relative rounded-2xl bg-white shadow-2xl p-2 border border-gray-100">
                                <div className="rounded-xl overflow-hidden bg-gray-900 aspect-[4/3] flex items-center justify-center relative group">
                                    <div className="absolute inset-0 bg-gradient-to-br from-primary-900/40 to-black/60 z-10"></div>
                                    <div className="relative z-20 text-center p-8">
                                        <div className="w-16 h-16 bg-white/10 backdrop-blur-md rounded-2xl flex items-center justify-center mx-auto mb-4 border border-white/20 shadow-inner">
                                            <Zap className="w-8 h-8 text-yellow-400" />
                                        </div>
                                        <h3 className="text-white text-xl font-semibold mb-2">AI Engine Active</h3>
                                        <p className="text-gray-300">Processing 1.2M events/sec</p>
                                    </div>

                                    {/* Abstract UI Elements */}
                                    <div className="absolute top-4 right-4 z-20 w-32 h-10 bg-white/10 backdrop-blur-sm rounded-lg border border-white/10"></div>
                                    <div className="absolute bottom-8 left-8 z-20 w-48 h-16 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 flex items-center px-4 gap-3">
                                        <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center border border-green-500/30">
                                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                                        </div>
                                        <div className="h-2 w-20 bg-white/20 rounded"></div>
                                    </div>
                                </div>
                            </div>
                            {/* Decorative background blobs */}
                            <div className="absolute -z-10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-gradient-to-tr from-primary-200/30 to-accent-200/30 blur-3xl rounded-full opacity-60"></div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-20 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-3xl mx-auto mb-16">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose AOIA?</h2>
                        <p className="text-lg text-gray-600">
                            Our platform combines advanced machine learning with real-time operational data to solve complex problems before they impact your business.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {/* Feature 1 */}
                        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
                            <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center text-primary-600 mb-6">
                                <Cpu className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Autonomous Optimization</h3>
                            <p className="text-gray-600">
                                AI agents continuously monitor and optimize your workflows, reducing manual intervention by up to 80%.
                            </p>
                        </div>

                        {/* Feature 2 */}
                        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
                            <div className="w-12 h-12 bg-accent-50 rounded-xl flex items-center justify-center text-accent-600 mb-6">
                                <BarChart3 className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Predictive Analytics</h3>
                            <p className="text-gray-600">
                                Forecast trends and potential bottlenecks with high accuracy, enabling proactive decision-making.
                            </p>
                        </div>

                        {/* Feature 3 */}
                        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
                            <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center text-green-600 mb-6">
                                <ShieldCheck className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">Enterprise Security</h3>
                            <p className="text-gray-600">
                                Bank-grade security with automated compliance monitoring and threat detection built-in.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Problem/Solution Section */}
            <section id="solutions" className="py-20 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row items-center gap-12">
                        <div className="md:w-1/2">
                            <div className="relative">
                                <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-accent-600 rounded-2xl transform rotate-3 opacity-20"></div>
                                <div className="relative bg-gray-900 rounded-2xl p-8 text-white shadow-xl">
                                    <div className="flex items-center gap-3 mb-6">
                                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                                        <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                    </div>
                                    <div className="space-y-4 font-mono text-sm text-gray-300">
                                        <div className="flex gap-4">
                                            <span className="text-gray-500">09:41:23</span>
                                            <span className="text-red-400">Error</span>
                                            <span>Connection timeout in cluster-a</span>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="text-gray-500">09:41:24</span>
                                            <span className="text-yellow-400">Warn</span>
                                            <span>Latency spike detected (2500ms)</span>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="text-gray-500">09:41:25</span>
                                            <span className="text-primary-400">Info</span>
                                            <span>AOIA Auto-scaling triggered...</span>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="text-gray-500">09:41:30</span>
                                            <span className="text-green-400">Success</span>
                                            <span>Performance restored. Latency: 45ms</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="md:w-1/2">
                            <h2 className="text-3xl font-bold text-gray-900 mb-6">The Problem: Operational Noise</h2>
                            <p className="text-lg text-gray-600 mb-6">
                                Modern systems generate massive amounts of data. Filtering through noise to find critical signals is impossible for humans at scale, leading to downtime and lost revenue.
                            </p>
                            <h3 className="text-xl font-bold text-gray-900 mb-3">The Solution: Intelligent Automation</h3>
                            <ul className="space-y-4">
                                <li className="flex items-start gap-3">
                                    <div className="mt-1 w-5 h-5 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 shrink-0">
                                        <CheckCircle2 className="w-3 h-3" />
                                    </div>
                                    <span className="text-gray-700">Automated root cause analysis in milliseconds</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <div className="mt-1 w-5 h-5 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 shrink-0">
                                        <CheckCircle2 className="w-3 h-3" />
                                    </div>
                                    <span className="text-gray-700">Self-healing infrastructure monitoring</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <div className="mt-1 w-5 h-5 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 shrink-0">
                                        <CheckCircle2 className="w-3 h-3" />
                                    </div>
                                    <span className="text-gray-700">Real-time resource optimization</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-primary-900 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-96 h-96 bg-primary-800 rounded-full blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2"></div>
                <div className="absolute bottom-0 left-0 w-96 h-96 bg-accent-900 rounded-full blur-3xl opacity-50 translate-y-1/2 -translate-x-1/2"></div>

                <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">Ready to transform your operations?</h2>
                    <p className="text-primary-100 text-lg mb-10 max-w-2xl mx-auto">
                        Join forward-thinking companies using AOIA to drive efficiency and innovation. Start free today.
                    </p>
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-primary-900 bg-white rounded-xl hover:bg-gray-100 transition-all duration-200"
                    >
                        Get Started Now
                        <ArrowRight className="ml-2 w-5 h-5" />
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-50 border-t border-gray-200 py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row justify-between items-center">
                        <div className="flex items-center gap-2 mb-4 md:mb-0">
                            <div className="w-8 h-8 rounded-lg bg-gray-900 flex items-center justify-center">
                                <span className="text-white font-bold text-sm">A</span>
                            </div>
                            <span className="text-xl font-bold text-gray-900">AOIA</span>
                        </div>
                        <div className="text-gray-500 text-sm">
                            © 2024 Autonomous Operational Intelligence Agent. All rights reserved.
                        </div>
                        <div className="flex gap-6 mt-4 md:mt-0">
                            <a href="#" className="text-gray-400 hover:text-gray-600 transition-colors"><Globe className="w-5 h-5" /></a>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
