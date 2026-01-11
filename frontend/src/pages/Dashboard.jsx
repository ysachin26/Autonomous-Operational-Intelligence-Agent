import { useState, useEffect } from 'react';
import { useActions } from '../components/ActionProvider';
import {
    TrendingUp,
    TrendingDown,
    Activity,
    AlertCircle,
    DollarSign,
    CheckCircle,
    ArrowRight,
    Clock,
    Zap,
    Users,
    Factory,
    AlertTriangle,
    Eye,
    EyeOff,
} from 'lucide-react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
    AreaChart,
    Area,
} from 'recharts';
import {
    machines,
    employees,
    generateHistoricalData,
    generateRealtimeMetrics,
    generateAnomalies,
    generateMachineEvents,
    calculateTotalLoss,
} from '../data/demoData';

export default function Dashboard() {
    const { requestAction, executedActions } = useActions();
    const [historicalData, setHistoricalData] = useState([]);
    const [realtimeMetrics, setRealtimeMetrics] = useState(null);
    const [todayEvents, setTodayEvents] = useState([]);
    const [anomalies, setAnomalies] = useState([]);
    const [losses, setLosses] = useState({ total: 0, idle: 0, breakdown: 0, microDowntime: 0 });
    const [showHidden, setShowHidden] = useState(false);

    useEffect(() => {
        // Generate initial data
        const history = generateHistoricalData();
        setHistoricalData(history);

        const events = generateMachineEvents(new Date());
        setTodayEvents(events);

        const detectedAnomalies = generateAnomalies(events);
        setAnomalies(detectedAnomalies);

        const calculatedLosses = calculateTotalLoss(events);
        setLosses(calculatedLosses);

        // Update real-time metrics every 5 seconds
        const updateMetrics = () => setRealtimeMetrics(generateRealtimeMetrics());
        updateMetrics();
        const interval = setInterval(updateMetrics, 5000);

        return () => clearInterval(interval);
    }, []);

    const lossChartData = historicalData.map(d => ({
        day: d.dayName,
        loss: Math.round(d.totalLoss / 1000),
        efficiency: d.efficiency,
    }));

    const lossByType = [
        { name: 'Idle Time', value: losses.idle, color: '#6366f1' },
        { name: 'Breakdowns', value: losses.breakdown, color: '#ef4444' },
        { name: 'Hidden Loss', value: losses.microDowntime, color: '#f59e0b' },
        { name: 'Low Efficiency', value: losses.lowEfficiency, color: '#8b5cf6' },
    ].filter(l => l.value > 0);

    const machineStatus = machines.map(m => {
        const events = todayEvents.filter(e => e.machineId === m.id);
        const lastEvent = events[events.length - 1];
        return {
            ...m,
            status: lastEvent?.eventType === 'PRODUCTION' ? 'running' :
                lastEvent?.eventType === 'BREAKDOWN' ? 'down' : 'idle',
            currentEfficiency: lastEvent?.efficiency || 0,
        };
    });

    const recommendations = [
        {
            id: 1,
            title: 'Schedule preventive maintenance for M2',
            impact: 55000,
            confidence: 94,
            priority: 'high',
            reason: 'Frequent micro-downtimes detected',
            action: 'A maintenance ticket will be created for CNC Machine 2, scheduled for the next planned downtime window.',
        },
        {
            id: 2,
            title: 'Rebalance Shift B workload',
            impact: 32000,
            confidence: 89,
            priority: 'medium',
            reason: 'Operator overload pattern detected',
            action: 'Task assignments will be redistributed from Shift B to Shift C, reducing operator load by 20%.',
        },
        {
            id: 3,
            title: 'Reduce idle time during shift transitions',
            impact: 18000,
            confidence: 82,
            priority: 'medium',
            reason: 'Average 15 min gap between shifts',
            action: 'Shift handover process will be optimized with parallel checkout/checkin procedures.',
        },
    ];

    const handleExecute = (rec) => {
        // Check if already executed
        if (executedActions.find(a => a.title === rec.title)) {
            return; // Already executed
        }
        requestAction({
            title: rec.title,
            description: rec.reason,
            impact: rec.impact,
            confidence: rec.confidence,
            action: rec.action,
        });
    };

    const isExecuted = (rec) => executedActions.some(a => a.title === rec.title);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="page-header mb-0">
                    <h1 className="page-title">Live Operations Dashboard</h1>
                    <p className="page-subtitle">Real-time operational intelligence overview</p>
                </div>
                <button
                    onClick={() => setShowHidden(!showHidden)}
                    className={`btn ${showHidden ? 'btn-primary' : 'btn-secondary'}`}
                >
                    {showHidden ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                    {showHidden ? 'Showing Hidden Losses' : 'Show Hidden Losses'}
                </button>
            </div>

            {/* Real-time KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                <KPICard
                    icon={Activity}
                    label="Current Efficiency"
                    value={`${realtimeMetrics?.currentEfficiency?.toFixed(1) || 0}%`}
                    trend={3.2}
                    trendUp={true}
                    iconColor="text-primary-600"
                    iconBg="bg-primary-50"
                />
                <KPICard
                    icon={Factory}
                    label="Active Machines"
                    value={`${machineStatus.filter(m => m.status === 'running').length}/${machines.length}`}
                    subtitle="Running now"
                    iconColor="text-accent-600"
                    iconBg="bg-accent-50"
                />
                <KPICard
                    icon={AlertTriangle}
                    label="Active Alerts"
                    value={anomalies.filter(a => a.status === 'OPEN').length}
                    trend={2}
                    trendUp={false}
                    iconColor="text-amber-600"
                    iconBg="bg-amber-50"
                />
                <KPICard
                    icon={DollarSign}
                    label="Loss Today"
                    value={`₹${(realtimeMetrics?.lossToday || 0).toLocaleString()}`}
                    trend={15.4}
                    trendUp={false}
                    iconColor="text-red-600"
                    iconBg="bg-red-50"
                />
                <KPICard
                    icon={Zap}
                    label="Hidden Losses"
                    value={`₹${losses.microDowntime.toLocaleString()}`}
                    subtitle="Micro-downtimes"
                    iconColor="text-purple-600"
                    iconBg="bg-purple-50"
                    highlight={showHidden}
                />
            </div>

            {/* Machine Status Grid */}
            <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Machine Status</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                    {machineStatus.map(machine => (
                        <div key={machine.id} className="p-4 bg-gray-50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                                <span className="font-medium text-gray-900">{machine.id}</span>
                                <span className={`w-3 h-3 rounded-full ${machine.status === 'running' ? 'bg-accent-500 animate-pulse' :
                                    machine.status === 'down' ? 'bg-red-500' : 'bg-gray-400'
                                    }`} />
                            </div>
                            <p className="text-sm text-gray-500 truncate">{machine.name}</p>
                            <div className="mt-2 flex items-center justify-between">
                                <span className={`text-xs font-medium ${machine.status === 'running' ? 'text-accent-600' :
                                    machine.status === 'down' ? 'text-red-600' : 'text-gray-500'
                                    }`}>
                                    {machine.status.toUpperCase()}
                                </span>
                                {machine.status === 'running' && (
                                    <span className="text-xs text-gray-500">
                                        {machine.currentEfficiency.toFixed(0)}%
                                    </span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Loss Trend */}
                <div className="lg:col-span-2 card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">Loss Trend</h3>
                            <p className="text-sm text-gray-500">Last 7 days (₹ thousands)</p>
                        </div>
                        <div className="text-right">
                            <p className="text-2xl font-bold text-gray-900">
                                ₹{(historicalData.reduce((sum, d) => sum + d.totalLoss, 0) / 1000).toFixed(0)}K
                            </p>
                            <p className="text-sm text-gray-500">Total weekly loss</p>
                        </div>
                    </div>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={lossChartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                                <XAxis dataKey="day" stroke="#6b7280" fontSize={12} />
                                <YAxis stroke="#6b7280" fontSize={12} tickFormatter={(v) => `₹${v}k`} />
                                <Tooltip
                                    formatter={(value, name) => [
                                        name === 'loss' ? `₹${value}K` : `${value}%`,
                                        name === 'loss' ? 'Loss' : 'Efficiency'
                                    ]}
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '1px solid #e5e7eb',
                                        borderRadius: '8px',
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="loss"
                                    stroke="#ef4444"
                                    fill="#fecaca"
                                    strokeWidth={2}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Loss by Type */}
                <div className="card p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Loss Breakdown</h3>
                    <div className="h-48">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={lossByType}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={45}
                                    outerRadius={65}
                                    paddingAngle={2}
                                    dataKey="value"
                                >
                                    {lossByType.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value) => [`₹${value.toLocaleString()}`, '']}
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '1px solid #e5e7eb',
                                        borderRadius: '8px'
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="space-y-2 mt-2">
                        {lossByType.map((item) => (
                            <div key={item.name} className="flex items-center justify-between text-sm">
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                                    <span className="text-gray-600">{item.name}</span>
                                </div>
                                <span className="font-medium text-gray-900">₹{item.value.toLocaleString()}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* AI Recommendations */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">AI Recommendations</h3>
                            <p className="text-sm text-gray-500">Optimization suggestions</p>
                        </div>
                        <span className="badge-primary">₹{recommendations.reduce((s, r) => s + r.impact, 0).toLocaleString()} potential savings</span>
                    </div>
                    <div className="space-y-4">
                        {recommendations.map((rec) => (
                            <div key={rec.id} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                <div className="flex items-start gap-3">
                                    <div className={`w-2 h-2 rounded-full mt-2 ${rec.priority === 'high' ? 'bg-red-500' : 'bg-amber-500'
                                        }`} />
                                    <div className="flex-1">
                                        <p className="font-medium text-gray-900">{rec.title}</p>
                                        <p className="text-sm text-gray-500 mt-1">{rec.reason}</p>
                                        <div className="flex items-center gap-4 mt-2">
                                            <span className="text-sm font-medium text-accent-600">
                                                +₹{rec.impact.toLocaleString()} savings
                                            </span>
                                            <span className="text-sm text-gray-400">
                                                {rec.confidence}% confidence
                                            </span>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => handleExecute(rec)}
                                        disabled={isExecuted(rec)}
                                        className={`text-xs py-1.5 px-3 ${isExecuted(rec) ? 'btn-success cursor-default' : 'btn-primary'}`}
                                    >
                                        {isExecuted(rec) ? '✓ Executed' : 'Execute'}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Active Anomalies */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-semibold text-gray-900">Detected Anomalies</h3>
                        <span className="badge-danger">{anomalies.length} active</span>
                    </div>
                    <div className="space-y-4">
                        {anomalies.map((anomaly) => (
                            <div key={anomaly.id} className={`p-4 rounded-lg border ${anomaly.hidden && showHidden ? 'border-purple-300 bg-purple-50' :
                                anomaly.hidden ? 'border-gray-200 bg-gray-50 opacity-50' :
                                    'border-gray-200 bg-gray-50'
                                }`}>
                                <div className="flex items-start gap-3">
                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${anomaly.severity === 'HIGH' ? 'bg-red-100' :
                                        anomaly.severity === 'MEDIUM' ? 'bg-amber-100' : 'bg-gray-100'
                                        }`}>
                                        {anomaly.hidden ? (
                                            <EyeOff className={`w-5 h-5 ${showHidden ? 'text-purple-600' : 'text-gray-400'}`} />
                                        ) : (
                                            <AlertCircle className={`w-5 h-5 ${anomaly.severity === 'HIGH' ? 'text-red-600' :
                                                anomaly.severity === 'MEDIUM' ? 'text-amber-600' : 'text-gray-600'
                                                }`} />
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            <span className={`badge ${anomaly.severity === 'HIGH' ? 'badge-danger' :
                                                anomaly.severity === 'MEDIUM' ? 'badge-warning' : 'badge-secondary'
                                                }`}>
                                                {anomaly.severity}
                                            </span>
                                            {anomaly.hidden && (
                                                <span className="badge bg-purple-100 text-purple-700">HIDDEN</span>
                                            )}
                                            <span className="text-sm text-gray-500">{anomaly.source}</span>
                                        </div>
                                        <p className="font-medium text-gray-900 mt-1">{anomaly.description}</p>
                                        <p className="text-sm text-red-600 mt-1">
                                            Est. Loss: ₹{anomaly.estimatedLoss.toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

function KPICard({ icon: Icon, label, value, trend, trendUp, subtitle, iconColor, iconBg, highlight }) {
    return (
        <div className={`stat-card ${highlight ? 'ring-2 ring-purple-400 bg-purple-50' : ''}`}>
            <div className="flex items-start justify-between">
                <div className={`w-10 h-10 rounded-lg ${iconBg} flex items-center justify-center`}>
                    <Icon className={`w-5 h-5 ${iconColor}`} />
                </div>
                {trend !== undefined && (
                    <div className={`flex items-center gap-1 ${trendUp ? 'text-accent-600' : 'text-red-600'}`}>
                        {trendUp ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                        <span className="text-sm font-medium">{trend}%</span>
                    </div>
                )}
            </div>
            <div className="mt-3">
                <p className="text-2xl font-bold text-gray-900">{value}</p>
                <p className="text-sm text-gray-500">{subtitle || label}</p>
            </div>
        </div>
    );
}
