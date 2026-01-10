import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    TrendingUp,
    TrendingDown,
    AlertTriangle,
    Zap,
    DollarSign,
    Activity,
    Clock,
    Target,
    ArrowUpRight,
    ArrowDownRight,
    PlayCircle,
} from 'lucide-react';
import {
    LineChart,
    Line,
    AreaChart,
    Area,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
} from 'recharts';
import api from '../services/api';

const COLORS = ['#8b5cf6', '#06b6d4', '#22c55e', '#f59e0b', '#ef4444'];

export default function Dashboard() {
    const [dashboardData, setDashboardData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        fetchDashboardData();
        fetchRecommendations();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await api.get('/api/dashboard');
            setDashboardData(response.data.data);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
            // Use mock data for demo
            setDashboardData(getMockDashboardData());
        } finally {
            setIsLoading(false);
        }
    };

    const fetchRecommendations = async () => {
        try {
            const response = await api.get('/api/recommendations?limit=3');
            setRecommendations(response.data.data || []);
        } catch (error) {
            setRecommendations(getMockRecommendations());
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    const kpis = [
        {
            title: 'Efficiency Score',
            value: dashboardData?.kpis?.efficiencyScore || 87,
            suffix: '%',
            change: +3.2,
            icon: Target,
            color: 'primary',
        },
        {
            title: 'Active Incidents',
            value: dashboardData?.kpis?.activeIncidents || 3,
            change: -2,
            icon: AlertTriangle,
            color: 'warning',
        },
        {
            title: 'Loss (24h)',
            value: dashboardData?.loss?.last24h || 45000,
            prefix: '₹',
            change: -15.4,
            icon: DollarSign,
            color: 'danger',
        },
        {
            title: 'Pending Actions',
            value: dashboardData?.kpis?.pendingRecommendations || 5,
            change: +2,
            icon: Zap,
            color: 'accent',
        },
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-2xl lg:text-3xl font-display font-bold text-white">
                        Operations Dashboard
                    </h1>
                    <p className="text-dark-400 mt-1">Real-time operational intelligence overview</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-dark-800/50 border border-dark-700">
                        <Activity className="w-4 h-4 text-green-400 animate-pulse" />
                        <span className="text-sm text-dark-300">Monitoring active</span>
                    </div>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
                {kpis.map((kpi, index) => (
                    <motion.div
                        key={kpi.title}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="kpi-card group"
                    >
                        <div className="flex items-start justify-between mb-4">
                            <div className={`p-3 rounded-xl bg-${kpi.color === 'primary' ? 'primary' : kpi.color === 'accent' ? 'accent' : kpi.color === 'warning' ? 'yellow' : 'red'}-500/20`}>
                                <kpi.icon className={`w-5 h-5 text-${kpi.color === 'primary' ? 'primary' : kpi.color === 'accent' ? 'accent' : kpi.color === 'warning' ? 'yellow' : 'red'}-400`} />
                            </div>
                            <div className={`flex items-center gap-1 text-sm ${kpi.change > 0 && kpi.title !== 'Loss (24h)' ? 'text-green-400' : kpi.change < 0 && kpi.title === 'Loss (24h)' ? 'text-green-400' : kpi.change < 0 && kpi.title !== 'Loss (24h)' ? 'text-red-400' : 'text-dark-400'}`}>
                                {kpi.change > 0 ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                                {Math.abs(kpi.change)}%
                            </div>
                        </div>
                        <p className="text-sm text-dark-400 mb-1">{kpi.title}</p>
                        <p className="text-2xl lg:text-3xl font-display font-bold text-white">
                            {kpi.prefix}
                            {typeof kpi.value === 'number' ? kpi.value.toLocaleString() : kpi.value}
                            {kpi.suffix}
                        </p>
                    </motion.div>
                ))}
            </div>

            {/* Main Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Loss Trend Chart */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="lg:col-span-2 glass-card"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-white">Loss Trend</h3>
                            <p className="text-sm text-dark-400">Last 30 days operational loss</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-primary-500" />
                                <span className="text-sm text-dark-400">Daily Loss (₹)</span>
                            </div>
                        </div>
                    </div>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={dashboardData?.loss?.trend || getMockLossTrend()}>
                                <defs>
                                    <linearGradient id="lossGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis dataKey="date" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 12 }} />
                                <YAxis stroke="#64748b" tick={{ fill: '#64748b', fontSize: 12 }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px' }}
                                    labelStyle={{ color: '#f1f5f9' }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="loss"
                                    stroke="#8b5cf6"
                                    strokeWidth={2}
                                    fill="url(#lossGradient)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Anomaly Distribution */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="glass-card"
                >
                    <h3 className="text-lg font-semibold text-white mb-6">Anomaly Distribution</h3>
                    <div className="h-48">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={getAnomalyDistribution()}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={50}
                                    outerRadius={70}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {getAnomalyDistribution().map((entry, index) => (
                                        <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="grid grid-cols-2 gap-2 mt-4">
                        {getAnomalyDistribution().map((item, index) => (
                            <div key={item.name} className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[index] }} />
                                <span className="text-xs text-dark-400">{item.name}</span>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* AI Recommendations */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="glass-card"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-white">AI Recommendations</h3>
                            <p className="text-sm text-dark-400">Autonomous optimization suggestions</p>
                        </div>
                        <a href="/agent" className="text-sm text-primary-400 hover:text-primary-300">
                            View all →
                        </a>
                    </div>
                    <div className="space-y-4">
                        {(recommendations.length > 0 ? recommendations : getMockRecommendations()).map((rec, index) => (
                            <div
                                key={rec.id || index}
                                className="p-4 rounded-xl bg-dark-800/50 border border-dark-700/50 hover:border-primary-500/50 transition-all cursor-pointer"
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <h4 className="font-medium text-white">{rec.title}</h4>
                                    <span className={`badge ${rec.priority === 'URGENT' || rec.priority === 'HIGH' ? 'badge-danger' : 'badge-primary'}`}>
                                        {rec.priority}
                                    </span>
                                </div>
                                <p className="text-sm text-dark-400 mb-3">{rec.description}</p>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <span className="text-sm text-green-400">
                                            +₹{rec.estimatedImpact?.toLocaleString() || '25,000'}
                                        </span>
                                        <span className="text-sm text-dark-500">
                                            {(rec.confidence * 100)?.toFixed(0) || 85}% confidence
                                        </span>
                                    </div>
                                    <button className="btn-ghost text-sm py-1.5 px-3">
                                        <PlayCircle className="w-4 h-4" />
                                        Execute
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Recent Incidents */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.7 }}
                    className="glass-card"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-white">Recent Incidents</h3>
                            <p className="text-sm text-dark-400">Latest operational incidents</p>
                        </div>
                        <a href="/incidents" className="text-sm text-primary-400 hover:text-primary-300">
                            View all →
                        </a>
                    </div>
                    <div className="space-y-3">
                        {(dashboardData?.recentIncidents || getMockIncidents()).map((incident, index) => (
                            <div
                                key={incident.id || index}
                                className="flex items-center gap-4 p-3 rounded-xl hover:bg-dark-800/50 transition-colors cursor-pointer"
                            >
                                <div className={`p-2 rounded-lg ${incident.status === 'ACTIVE' ? 'bg-red-500/20' :
                                        incident.status === 'INVESTIGATING' ? 'bg-yellow-500/20' :
                                            'bg-green-500/20'
                                    }`}>
                                    <AlertTriangle className={`w-4 h-4 ${incident.status === 'ACTIVE' ? 'text-red-400' :
                                            incident.status === 'INVESTIGATING' ? 'text-yellow-400' :
                                                'text-green-400'
                                        }`} />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-white truncate">{incident.title}</p>
                                    <p className="text-xs text-dark-400">
                                        Loss: ₹{incident.estimatedLoss?.toLocaleString() || '0'}
                                    </p>
                                </div>
                                <span className={`badge text-xs ${incident.status === 'ACTIVE' ? 'badge-danger' :
                                        incident.status === 'INVESTIGATING' ? 'badge-warning' :
                                            'badge-success'
                                    }`}>
                                    {incident.status}
                                </span>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}

// Mock data functions
function getMockDashboardData() {
    return {
        kpis: {
            efficiencyScore: 87,
            activeIncidents: 3,
            openAnomalies: 8,
            pendingRecommendations: 5,
        },
        loss: {
            last24h: 45000,
            last7d: 285000,
            trend: getMockLossTrend(),
        },
        recentIncidents: getMockIncidents(),
    };
}

function getMockLossTrend() {
    const data = [];
    for (let i = 29; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        data.push({
            date: date.toISOString().slice(5, 10),
            loss: Math.floor(10000 + Math.random() * 50000),
        });
    }
    return data;
}

function getAnomalyDistribution() {
    return [
        { name: 'Idle Spike', value: 35 },
        { name: 'Throughput', value: 25 },
        { name: 'Quality', value: 20 },
        { name: 'Downtime', value: 12 },
        { name: 'Other', value: 8 },
    ];
}

function getMockRecommendations() {
    return [
        {
            id: 1,
            title: 'Rebalance Shift B Workload',
            description: 'Redistribute tasks to reduce idle time by 15%',
            priority: 'HIGH',
            estimatedImpact: 32000,
            confidence: 0.89,
        },
        {
            id: 2,
            title: 'Schedule Maintenance - Machine 2',
            description: 'Predictive model indicates issue within 48h',
            priority: 'URGENT',
            estimatedImpact: 55000,
            confidence: 0.94,
        },
        {
            id: 3,
            title: 'Optimize Task Routing',
            description: 'Adjust routing for high-value orders',
            priority: 'MEDIUM',
            estimatedImpact: 28000,
            confidence: 0.82,
        },
    ];
}

function getMockIncidents() {
    return [
        { id: 1, title: 'Machine 1 Throughput Drop', status: 'ACTIVE', estimatedLoss: 45000 },
        { id: 2, title: 'Shift B Idle Time Spike', status: 'INVESTIGATING', estimatedLoss: 28000 },
        { id: 3, title: 'Quality Control Alert', status: 'MITIGATING', estimatedLoss: 62000 },
        { id: 4, title: 'Morning Shift Overload', status: 'RESOLVED', estimatedLoss: 35000 },
    ];
}
