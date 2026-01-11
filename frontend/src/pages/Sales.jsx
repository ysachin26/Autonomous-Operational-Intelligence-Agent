import { useState } from 'react';
import {
    Users,
    Target,
    Mail,
    Building,
    TrendingUp,
    Clock,
    CheckCircle,
    AlertCircle,
    DollarSign,
    UserPlus,
    Send,
    BarChart3,
    RefreshCw,
} from 'lucide-react';
import { asloaApi } from '../services/api';

export default function Sales() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    // Lead form state
    const [leadForm, setLeadForm] = useState({
        company: '',
        company_size: 100,
        industry: 'technology',
        contact_name: '',
        contact_title: '',
        contact_email: '',
        source: 'website',
        budget: 50000,
        budget_confirmed: false,
        deal_size_estimate: 50000,
        pain_points: [],
        timeline: 90,
    });

    const [painPointInput, setPainPointInput] = useState('');

    const industries = [
        'technology', 'saas', 'fintech', 'healthcare',
        'manufacturing', 'retail', 'ecommerce', 'logistics'
    ];

    const sources = [
        'website', 'linkedin', 'referral', 'demo_request',
        'contact_form', 'conference', 'cold_outreach'
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await asloaApi.processLead(leadForm);
            setResult(response);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to process lead');
        } finally {
            setLoading(false);
        }
    };

    const addPainPoint = () => {
        if (painPointInput.trim()) {
            setLeadForm(prev => ({
                ...prev,
                pain_points: [...prev.pain_points, painPointInput.trim()]
            }));
            setPainPointInput('');
        }
    };

    const removePainPoint = (index) => {
        setLeadForm(prev => ({
            ...prev,
            pain_points: prev.pain_points.filter((_, i) => i !== index)
        }));
    };

    const handleDemoLead = () => {
        setLeadForm({
            company: 'TechCorp Industries',
            company_size: 350,
            industry: 'saas',
            contact_name: 'Priya Sharma',
            contact_title: 'VP of Engineering',
            contact_email: 'priya@techcorp.com',
            source: 'linkedin',
            budget: 85000,
            budget_confirmed: true,
            deal_size_estimate: 120000,
            pain_points: ['Developer productivity bottleneck', 'Slow deployment cycles'],
            timeline: 45,
        });
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="page-header">
                <h1 className="page-title">ASLOA Sales Pipeline</h1>
                <p className="page-subtitle">AI-Powered Sales Lead Automation - Process leads through 7 intelligent agents</p>
            </div>

            {/* Pipeline Visualization */}
            <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">7-Agent Pipeline</h3>
                <div className="flex items-center justify-between overflow-x-auto pb-2">
                    {[
                        { icon: Target, label: 'Score', color: 'bg-blue-500' },
                        { icon: CheckCircle, label: 'BANT', color: 'bg-green-500' },
                        { icon: Building, label: 'Research', color: 'bg-purple-500' },
                        { icon: Mail, label: 'Outreach', color: 'bg-orange-500' },
                        { icon: Users, label: 'Route', color: 'bg-pink-500' },
                        { icon: RefreshCw, label: 'CRM', color: 'bg-cyan-500' },
                        { icon: BarChart3, label: 'Analytics', color: 'bg-indigo-500' },
                    ].map((step, index) => (
                        <div key={step.label} className="flex items-center">
                            <div className="flex flex-col items-center min-w-[80px]">
                                <div className={`w-12 h-12 rounded-full ${step.color} flex items-center justify-center text-white`}>
                                    <step.icon className="w-6 h-6" />
                                </div>
                                <span className="text-xs mt-2 text-gray-600">{step.label}</span>
                            </div>
                            {index < 6 && (
                                <div className="w-8 h-0.5 bg-gray-300 mx-1" />
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Lead Input Form */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-semibold text-gray-900">Process New Lead</h3>
                        <button
                            onClick={handleDemoLead}
                            className="btn btn-secondary text-xs"
                        >
                            Load Demo Lead
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                                <input
                                    type="text"
                                    value={leadForm.company}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, company: e.target.value }))}
                                    className="input"
                                    placeholder="Company name"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Company Size</label>
                                <input
                                    type="number"
                                    value={leadForm.company_size}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, company_size: parseInt(e.target.value) }))}
                                    className="input"
                                    min="1"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                                <select
                                    value={leadForm.industry}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, industry: e.target.value }))}
                                    className="input"
                                >
                                    {industries.map(ind => (
                                        <option key={ind} value={ind}>{ind.charAt(0).toUpperCase() + ind.slice(1)}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
                                <select
                                    value={leadForm.source}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, source: e.target.value }))}
                                    className="input"
                                >
                                    {sources.map(src => (
                                        <option key={src} value={src}>{src.replace('_', ' ').charAt(0).toUpperCase() + src.slice(1)}</option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Contact Name</label>
                                <input
                                    type="text"
                                    value={leadForm.contact_name}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, contact_name: e.target.value }))}
                                    className="input"
                                    placeholder="Full name"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                                <input
                                    type="text"
                                    value={leadForm.contact_title}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, contact_title: e.target.value }))}
                                    className="input"
                                    placeholder="e.g. VP of Sales"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                            <input
                                type="email"
                                value={leadForm.contact_email}
                                onChange={(e) => setLeadForm(prev => ({ ...prev, contact_email: e.target.value }))}
                                className="input"
                                placeholder="email@company.com"
                                required
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Budget ($)</label>
                                <input
                                    type="number"
                                    value={leadForm.budget}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, budget: parseInt(e.target.value) }))}
                                    className="input"
                                    min="0"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Timeline (days)</label>
                                <input
                                    type="number"
                                    value={leadForm.timeline}
                                    onChange={(e) => setLeadForm(prev => ({ ...prev, timeline: parseInt(e.target.value) }))}
                                    className="input"
                                    min="1"
                                />
                            </div>
                        </div>

                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="budget_confirmed"
                                checked={leadForm.budget_confirmed}
                                onChange={(e) => setLeadForm(prev => ({ ...prev, budget_confirmed: e.target.checked }))}
                                className="rounded"
                            />
                            <label htmlFor="budget_confirmed" className="text-sm text-gray-700">Budget Confirmed</label>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Pain Points</label>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={painPointInput}
                                    onChange={(e) => setPainPointInput(e.target.value)}
                                    className="input flex-1"
                                    placeholder="Add pain point"
                                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addPainPoint())}
                                />
                                <button type="button" onClick={addPainPoint} className="btn btn-secondary">Add</button>
                            </div>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {leadForm.pain_points.map((pain, index) => (
                                    <span key={index} className="badge-primary flex items-center gap-1">
                                        {pain}
                                        <button type="button" onClick={() => removePainPoint(index)} className="hover:text-red-500">x</button>
                                    </span>
                                ))}
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn btn-primary w-full"
                        >
                            {loading ? (
                                <>
                                    <RefreshCw className="w-4 h-4 animate-spin" />
                                    Processing through 7 agents...
                                </>
                            ) : (
                                <>
                                    <Send className="w-4 h-4" />
                                    Process Lead
                                </>
                            )}
                        </button>
                    </form>

                    {error && (
                        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <div className="flex items-center gap-2 text-red-700">
                                <AlertCircle className="w-5 h-5" />
                                <span className="font-medium">Error</span>
                            </div>
                            <p className="text-sm text-red-600 mt-1">{error}</p>
                        </div>
                    )}
                </div>

                {/* Results Panel */}
                <div className="space-y-6">
                    {result ? (
                        <>
                            {/* Summary Card */}
                            <div className="card p-6 bg-gradient-to-r from-primary-50 to-accent-50">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900">
                                            {result.summary?.headline || 'Lead Processed'}
                                        </h3>
                                        <p className="text-sm text-gray-600 mt-1">
                                            {result.summary?.message_for_ui}
                                        </p>
                                    </div>
                                    <span className={`badge ${result.scoring?.tier === 'HOT' ? 'badge-danger' : result.scoring?.tier === 'WARM' ? 'badge-warning' : 'badge-secondary'}`}>
                                        {result.scoring?.tier}
                                    </span>
                                </div>
                                <div className="grid grid-cols-3 gap-4 mt-4">
                                    <div className="text-center">
                                        <p className="text-2xl font-bold text-primary-600">{result.scoring?.score}/100</p>
                                        <p className="text-xs text-gray-500">Score</p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-2xl font-bold text-accent-600">{result.qualification?.qualified_criteria}/4</p>
                                        <p className="text-xs text-gray-500">BANT</p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-2xl font-bold text-purple-600">{result.analytics?.time_saved?.this_lead_minutes} min</p>
                                        <p className="text-xs text-gray-500">Saved</p>
                                    </div>
                                </div>
                            </div>

                            {/* Actions Taken */}
                            <div className="card p-6">
                                <h4 className="font-semibold text-gray-900 mb-4">Actions Executed</h4>
                                <div className="space-y-2">
                                    {result.actions_taken?.map((action, index) => (
                                        <div key={index} className="flex items-center gap-3 p-2 bg-gray-50 rounded">
                                            <CheckCircle className="w-5 h-5 text-green-500" />
                                            <span className="text-sm text-gray-700">{action.action.replace(/_/g, ' ')}</span>
                                            <span className="text-xs text-gray-400 ml-auto">{action.status}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Routing Info */}
                            {result.routing?.assigned_to && (
                                <div className="card p-6">
                                    <h4 className="font-semibold text-gray-900 mb-4">Assigned To</h4>
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                                            <Users className="w-6 h-6 text-primary-600" />
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-900">{result.routing.assigned_to.name}</p>
                                            <p className="text-sm text-gray-500">{result.routing.assigned_to.email}</p>
                                            <p className="text-xs text-accent-600 mt-1">
                                                Expected response: {result.routing.expected_response_time}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Outreach Preview */}
                            {result.outreach?.email && (
                                <div className="card p-6">
                                    <h4 className="font-semibold text-gray-900 mb-4">Generated Email</h4>
                                    <div className="bg-gray-50 rounded-lg p-4">
                                        <p className="text-sm font-medium text-gray-700">
                                            Subject: {result.outreach.email.subject}
                                        </p>
                                        <pre className="text-sm text-gray-600 mt-3 whitespace-pre-wrap font-sans">
                                            {result.outreach.email.body}
                                        </pre>
                                    </div>
                                </div>
                            )}
                        </>
                    ) : (
                        <div className="card p-12 text-center">
                            <UserPlus className="w-16 h-16 text-gray-300 mx-auto" />
                            <h3 className="text-lg font-medium text-gray-500 mt-4">No Lead Processed Yet</h3>
                            <p className="text-sm text-gray-400 mt-2">
                                Enter lead details and click "Process Lead" to run the 7-agent pipeline
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
