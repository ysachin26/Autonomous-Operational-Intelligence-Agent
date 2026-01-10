import { useState, useEffect } from 'react';
import {
    Calendar,
    Filter,
    Download,
    TrendingUp,
    TrendingDown,
    Eye,
    EyeOff,
    AlertTriangle,
    Clock,
    DollarSign,
} from 'lucide-react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    LineChart,
    Line,
    ComposedChart,
    Area,
} from 'recharts';
import {
    machines,
    shifts,
    generateHistoricalData,
    generateShiftPerformance,
} from '../data/demoData';

export default function Analytics() {
    const [timeRange, setTimeRange] = useState('7d');
    const [showHiddenLosses, setShowHiddenLosses] = useState(false);
    const [historicalData, setHistoricalData] = useState([]);
    const [shiftData, setShiftData] = useState([]);

    useEffect(() => {
        const history = generateHistoricalData();
        setHistoricalData(history);
        setShiftData(generateShiftPerformance(new Date()));
    }, []);

    // Build heatmap data (Machine × Day)
    const heatmapData = machines.map(machine => {
        const row = { source: machine.name, id: machine.id };
        historicalData.forEach((day, index) => {
            const machineEvents = day.events.filter(e => e.machineId === machine.id);
            const productionEvents = machineEvents.filter(e => e.eventType === 'PRODUCTION');
            const avgEfficiency = productionEvents.length > 0
                ? productionEvents.reduce((sum, e) => sum + e.efficiency, 0) / productionEvents.length
                : 0;
            row[day.dayName] = Math.round(avgEfficiency);

            // Track losses separately
            const totalLoss = machineEvents
                .filter(e => e.lossAmount)
                .reduce((sum, e) => sum + e.lossAmount, 0);
            row[`${day.dayName}_loss`] = totalLoss;
        });
        return row;
    });

    // Loss by source
    const lossBySource = machines.map(machine => {
        const totalLoss = historicalData.reduce((sum, day) => {
            const machineEvents = day.events.filter(e => e.machineId === machine.id && e.lossAmount);
            return sum + machineEvents.reduce((s, e) => s + e.lossAmount, 0);
        }, 0);
        return {
            source: machine.id,
            name: machine.name,
            loss: totalLoss,
            costPerHour: machine.costPerHour,
        };
    }).sort((a, b) => b.loss - a.loss);

    // Hourly pattern (mock data for now)
    const hourlyData = Array.from({ length: 24 }, (_, i) => ({
        hour: i,
        hourLabel: `${i}:00`,
        efficiency: 60 + Math.random() * 35 + (i >= 10 && i <= 14 ? 10 : 0) - (i >= 22 || i <= 5 ? 15 : 0),
        loss: Math.floor(Math.random() * 5000 + (i >= 22 || i <= 5 ? 3000 : 1000)),
    }));

    // Shift comparison
    const shiftComparison = shiftData.map(s => ({
        shift: s.shiftName,
        efficiency: s.actualEfficiency,
        target: s.targetEfficiency,
        loss: s.lossAmount,
        operators: s.operators,
        status: s.status,
    }));

    const getHeatmapColor = (value) => {
        if (value >= 90) return 'bg-accent-100 text-accent-700';
        if (value >= 80) return 'bg-blue-100 text-blue-700';
        if (value >= 70) return 'bg-amber-100 text-amber-700';
        if (value > 0) return 'bg-red-100 text-red-700';
        return 'bg-gray-100 text-gray-400';
    };

    const days = historicalData.map(d => d.dayName);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div className="page-header mb-0">
                    <h1 className="page-title">Operational Analytics</h1>
                    <p className="page-subtitle">Deep-dive into performance patterns and losses</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setShowHiddenLosses(!showHiddenLosses)}
                        className={`btn ${showHiddenLosses ? 'btn-primary' : 'btn-secondary'}`}
                    >
                        {showHiddenLosses ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                        Hidden Losses
                    </button>
                    <button className="btn-secondary">
                        <Download className="w-4 h-4" />
                        Export
                    </button>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <div className="card p-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-red-50 flex items-center justify-center">
                            <DollarSign className="w-5 h-5 text-red-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-gray-900">
                                ₹{(historicalData.reduce((s, d) => s + d.totalLoss, 0) / 1000).toFixed(0)}K
                            </p>
                            <p className="text-sm text-gray-500">Weekly Loss</p>
                        </div>
                    </div>
                </div>
                <div className="card p-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center">
                            <Clock className="w-5 h-5 text-amber-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-gray-900">
                                {historicalData.reduce((s, d) => s + d.events.filter(e => e.eventType === 'IDLE').length, 0)}
                            </p>
                            <p className="text-sm text-gray-500">Idle Events</p>
                        </div>
                    </div>
                </div>
                <div className="card p-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
                            <TrendingUp className="w-5 h-5 text-primary-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-gray-900">
                                {(historicalData.reduce((s, d) => s + d.efficiency, 0) / historicalData.length || 0).toFixed(1)}%
                            </p>
                            <p className="text-sm text-gray-500">Avg Efficiency</p>
                        </div>
                    </div>
                </div>
                <div className="card p-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-purple-50 flex items-center justify-center">
                            <EyeOff className="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-gray-900">
                                ₹{(historicalData.reduce((s, d) => s + d.losses.microDowntime, 0) / 1000).toFixed(0)}K
                            </p>
                            <p className="text-sm text-gray-500">Hidden Loss</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Efficiency Heatmap */}
            <div className="card p-6">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900">Efficiency Heatmap</h3>
                        <p className="text-sm text-gray-500">Machine performance by day</p>
                    </div>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr>
                                <th className="text-left text-sm font-medium text-gray-500 pb-4 pr-4">Machine</th>
                                {days.map((day) => (
                                    <th key={day} className="text-center text-sm font-medium text-gray-500 pb-4 px-2 min-w-[60px]">
                                        {day}
                                    </th>
                                ))}
                                <th className="text-right text-sm font-medium text-gray-500 pb-4 pl-4">Total Loss</th>
                            </tr>
                        </thead>
                        <tbody>
                            {heatmapData.map((row) => (
                                <tr key={row.id}>
                                    <td className="text-sm font-medium text-gray-900 py-2 pr-4">
                                        <div>
                                            <span className="font-semibold">{row.id}</span>
                                            <p className="text-xs text-gray-500 truncate max-w-[120px]">{row.source}</p>
                                        </div>
                                    </td>
                                    {days.map((day) => (
                                        <td key={day} className="px-1 py-2">
                                            <div className={`h-12 rounded-lg flex flex-col items-center justify-center ${getHeatmapColor(row[day])}`}>
                                                <span className="text-sm font-semibold">{row[day]}%</span>
                                                {showHiddenLosses && row[`${day}_loss`] > 0 && (
                                                    <span className="text-xs opacity-75">-₹{(row[`${day}_loss`] / 1000).toFixed(0)}k</span>
                                                )}
                                            </div>
                                        </td>
                                    ))}
                                    <td className="text-right pl-4">
                                        <span className="font-semibold text-red-600">
                                            ₹{days.reduce((sum, day) => sum + (row[`${day}_loss`] || 0), 0).toLocaleString()}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="flex items-center justify-center gap-6 mt-6 text-sm border-t border-gray-100 pt-4">
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-accent-100" />
                        <span className="text-gray-600">≥90% Excellent</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-blue-100" />
                        <span className="text-gray-600">80-89% Good</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-amber-100" />
                        <span className="text-gray-600">70-79% Fair</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-red-100" />
                        <span className="text-gray-600">&lt;70% Poor</span>
                    </div>
                </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Loss by Machine */}
                <div className="card p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Loss by Machine</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={lossBySource} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                                <XAxis type="number" stroke="#6b7280" fontSize={12} tickFormatter={(v) => `₹${v / 1000}k`} />
                                <YAxis dataKey="source" type="category" stroke="#6b7280" fontSize={12} width={50} />
                                <Tooltip
                                    formatter={(value) => [`₹${value.toLocaleString()}`, 'Loss']}
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '1px solid #e5e7eb',
                                        borderRadius: '8px',
                                    }}
                                />
                                <Bar dataKey="loss" fill="#ef4444" radius={[0, 4, 4, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Shift Comparison */}
                <div className="card p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Shift Performance</h3>
                    <div className="space-y-6">
                        {shiftComparison.map((shift) => (
                            <div key={shift.shift}>
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-2">
                                        <span className="font-medium text-gray-900">{shift.shift}</span>
                                        <span className={`badge ${shift.status === 'ON_TARGET' ? 'badge-success' :
                                                shift.status === 'BELOW_TARGET' ? 'badge-warning' : 'badge-danger'
                                            }`}>
                                            {shift.status.replace('_', ' ')}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-4 text-sm">
                                        <span className={shift.efficiency >= shift.target ? 'text-accent-600 font-semibold' : 'text-red-600 font-semibold'}>
                                            {shift.efficiency.toFixed(1)}%
                                        </span>
                                        <span className="text-gray-500">
                                            Loss: ₹{shift.loss.toLocaleString()}
                                        </span>
                                    </div>
                                </div>
                                <div className="relative h-3 bg-gray-100 rounded-full overflow-hidden">
                                    {/* Target line */}
                                    <div
                                        className="absolute top-0 bottom-0 w-0.5 bg-gray-400 z-10"
                                        style={{ left: `${shift.target}%` }}
                                    />
                                    {/* Efficiency bar */}
                                    <div
                                        className={`h-full rounded-full transition-all duration-500 ${shift.efficiency >= shift.target ? 'bg-accent-500' :
                                                shift.efficiency >= shift.target - 10 ? 'bg-amber-500' : 'bg-red-500'
                                            }`}
                                        style={{ width: `${shift.efficiency}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Hourly Pattern */}
            <div className="card p-6">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900">Hourly Pattern</h3>
                        <p className="text-sm text-gray-500">Efficiency and loss by hour of day</p>
                    </div>
                </div>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <ComposedChart data={hourlyData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                            <XAxis dataKey="hour" stroke="#6b7280" fontSize={10} tickFormatter={(v) => `${v}:00`} />
                            <YAxis yAxisId="left" stroke="#6b7280" fontSize={12} domain={[0, 100]} />
                            <YAxis yAxisId="right" orientation="right" stroke="#ef4444" fontSize={12} tickFormatter={(v) => `₹${v / 1000}k`} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'white',
                                    border: '1px solid #e5e7eb',
                                    borderRadius: '8px',
                                }}
                            />
                            <Area
                                yAxisId="left"
                                type="monotone"
                                dataKey="efficiency"
                                fill="#c7d2fe"
                                stroke="#4f46e5"
                                strokeWidth={2}
                            />
                            <Line
                                yAxisId="right"
                                type="monotone"
                                dataKey="loss"
                                stroke="#ef4444"
                                strokeWidth={2}
                                dot={false}
                            />
                        </ComposedChart>
                    </ResponsiveContainer>
                </div>
                <div className="flex items-center justify-center gap-6 mt-4 text-sm">
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-1 bg-primary-500 rounded" />
                        <span className="text-gray-600">Efficiency %</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-1 bg-red-500 rounded" />
                        <span className="text-gray-600">Loss (₹)</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
