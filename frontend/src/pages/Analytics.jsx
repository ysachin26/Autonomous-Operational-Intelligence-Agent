import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    TrendingDown,
    Filter,
    Calendar,
    Download,
    RefreshCw,
} from 'lucide-react';
import {
    AreaChart,
    Area,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from 'recharts';

export default function Analytics() {
    const [timeRange, setTimeRange] = useState('7d');
    const [isLoading, setIsLoading] = useState(false);

    const shiftData = [
        { name: 'Shift A', utilization: 85, throughput: 92, idleTime: 8 },
        { name: 'Shift B', utilization: 72, throughput: 78, idleTime: 15 },
        { name: 'Shift C', utilization: 88, throughput: 95, idleTime: 6 },
    ];

    const machineData = [
        { name: 'Machine 1', efficiency: 92, downtime: 3, quality: 98 },
        { name: 'Machine 2', efficiency: 78, downtime: 12, quality: 94 },
        { name: 'Machine 3', efficiency: 85, downtime: 7, quality: 96 },
        { name: 'Machine 4', efficiency: 90, downtime: 4, quality: 97 },
        { name: 'Machine 5', efficiency: 82, downtime: 9, quality: 95 },
    ];

    const hourlyData = Array.from({ length: 24 }, (_, i) => ({
        hour: `${i.toString().padStart(2, '0')}:00`,
        utilization: 60 + Math.random() * 35,
        anomalies: Math.floor(Math.random() * 5),
    }));

    const heatmapData = generateHeatmapData();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-2xl lg:text-3xl font-display font-bold text-white">
                        Analytics & Insights
                    </h1>
                    <p className="text-dark-400 mt-1">Deep-dive operational analysis and trends</p>
                </div>
                <div className="flex items-center gap-3">
                    <select
                        value={timeRange}
                        onChange={(e) => setTimeRange(e.target.value)}
                        className="px-4 py-2 rounded-xl bg-dark-800/50 border border-dark-700 text-white text-sm focus:border-primary-500 outline-none"
                    >
                        <option value="24h">Last 24 hours</option>
                        <option value="7d">Last 7 days</option>
                        <option value="30d">Last 30 days</option>
                        <option value="90d">Last 90 days</option>
                    </select>
                    <button className="btn-secondary">
                        <Filter className="w-4 h-4" />
                        Filters
                    </button>
                    <button className="btn-secondary">
                        <Download className="w-4 h-4" />
                        Export
                    </button>
                </div>
            </div>

            {/* Loss Heatmap */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card"
            >
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-lg font-semibold text-white">Loss Heatmap</h3>
                        <p className="text-sm text-dark-400">Problem areas by source and day</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="text-xs text-dark-400">Intensity:</span>
                        <div className="flex items-center gap-1">
                            <div className="w-4 h-4 rounded bg-green-500/30" />
                            <div className="w-4 h-4 rounded bg-yellow-500/50" />
                            <div className="w-4 h-4 rounded bg-orange-500/70" />
                            <div className="w-4 h-4 rounded bg-red-500/90" />
                        </div>
                    </div>
                </div>
                <div className="overflow-x-auto">
                    <div className="min-w-[600px]">
                        {/* Days header */}
                        <div className="flex mb-2">
                            <div className="w-24" />
                            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
                                <div key={day} className="flex-1 text-center text-xs text-dark-400">
                                    {day}
                                </div>
                            ))}
                        </div>
                        {/* Heatmap rows */}
                        {heatmapData.map((row) => (
                            <div key={row.source} className="flex items-center mb-2">
                                <div className="w-24 text-sm text-dark-300 truncate pr-2">{row.source}</div>
                                {row.values.map((value, i) => (
                                    <div key={i} className="flex-1 px-0.5">
                                        <div
                                            className="h-8 rounded transition-all hover:scale-110 cursor-pointer"
                                            style={{
                                                backgroundColor: getHeatmapColor(value),
                                            }}
                                            title={`${row.source} - Day ${i + 1}: ${value} issues`}
                                        />
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            </motion.div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Shift Performance */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="glass-card"
                >
                    <h3 className="text-lg font-semibold text-white mb-6">Shift Performance</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={shiftData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis dataKey="name" stroke="#64748b" />
                                <YAxis stroke="#64748b" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px' }}
                                />
                                <Legend />
                                <Bar dataKey="utilization" fill="#8b5cf6" name="Utilization %" radius={[4, 4, 0, 0]} />
                                <Bar dataKey="throughput" fill="#06b6d4" name="Throughput %" radius={[4, 4, 0, 0]} />
                                <Bar dataKey="idleTime" fill="#f59e0b" name="Idle Time %" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Machine Efficiency */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="glass-card"
                >
                    <h3 className="text-lg font-semibold text-white mb-6">Machine Efficiency</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={machineData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis type="number" stroke="#64748b" />
                                <YAxis dataKey="name" type="category" stroke="#64748b" width={80} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px' }}
                                />
                                <Bar dataKey="efficiency" fill="#22c55e" name="Efficiency %" radius={[0, 4, 4, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            </div>

            {/* Hourly Pattern */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass-card"
            >
                <h3 className="text-lg font-semibold text-white mb-6">Hourly Utilization Pattern</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={hourlyData}>
                            <defs>
                                <linearGradient id="utilizationGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="hour" stroke="#64748b" interval={2} />
                            <YAxis stroke="#64748b" />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px' }}
                            />
                            <Area
                                type="monotone"
                                dataKey="utilization"
                                stroke="#06b6d4"
                                strokeWidth={2}
                                fill="url(#utilizationGradient)"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </motion.div>

            {/* Summary Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                    { label: 'Avg. Utilization', value: '82.5%', trend: '+3.2%' },
                    { label: 'Total Downtime', value: '4.2h', trend: '-15%' },
                    { label: 'Anomalies Detected', value: '23', trend: '-8' },
                    { label: 'Resolution Rate', value: '91%', trend: '+5%' },
                ].map((stat, i) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 + i * 0.1 }}
                        className="glass-card text-center"
                    >
                        <p className="text-sm text-dark-400 mb-2">{stat.label}</p>
                        <p className="text-2xl font-bold text-white">{stat.value}</p>
                        <p className="text-sm text-green-400 mt-1">{stat.trend}</p>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

function generateHeatmapData() {
    const sources = ['Machine 1', 'Machine 2', 'Machine 3', 'Shift A', 'Shift B', 'Shift C'];
    return sources.map((source) => ({
        source,
        values: Array.from({ length: 7 }, () => Math.floor(Math.random() * 10)),
    }));
}

function getHeatmapColor(value) {
    if (value <= 2) return 'rgba(34, 197, 94, 0.3)';
    if (value <= 4) return 'rgba(234, 179, 8, 0.5)';
    if (value <= 6) return 'rgba(249, 115, 22, 0.7)';
    return 'rgba(239, 68, 68, 0.9)';
}
