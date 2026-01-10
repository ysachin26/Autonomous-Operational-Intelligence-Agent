import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    AlertTriangle,
    Clock,
    DollarSign,
    CheckCircle,
    XCircle,
    Search,
    Filter,
    ChevronDown,
    ChevronUp,
    ExternalLink,
} from 'lucide-react';
import { format } from 'date-fns';
import api from '../services/api';

export default function Incidents() {
    const [incidents, setIncidents] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [expandedId, setExpandedId] = useState(null);
    const [filter, setFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        fetchIncidents();
    }, []);

    const fetchIncidents = async () => {
        try {
            const response = await api.get('/api/incidents');
            setIncidents(response.data.data || []);
        } catch (error) {
            console.error('Failed to fetch incidents:', error);
            setIncidents(getMockIncidents());
        } finally {
            setIsLoading(false);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'ACTIVE': return 'badge-danger';
            case 'INVESTIGATING': return 'badge-warning';
            case 'MITIGATING': return 'badge-info';
            case 'RESOLVED': return 'badge-success';
            case 'CLOSED': return 'badge-secondary';
            default: return 'badge-primary';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'ACTIVE': return <AlertTriangle className="w-4 h-4 text-red-400" />;
            case 'INVESTIGATING': return <Clock className="w-4 h-4 text-yellow-400" />;
            case 'RESOLVED': return <CheckCircle className="w-4 h-4 text-green-400" />;
            default: return <AlertTriangle className="w-4 h-4 text-dark-400" />;
        }
    };

    const filteredIncidents = incidents.filter((incident) => {
        const matchesFilter = filter === 'all' || incident.status === filter;
        const matchesSearch = incident.title?.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesFilter && matchesSearch;
    });

    const statusCounts = {
        all: incidents.length,
        ACTIVE: incidents.filter((i) => i.status === 'ACTIVE').length,
        INVESTIGATING: incidents.filter((i) => i.status === 'INVESTIGATING').length,
        RESOLVED: incidents.filter((i) => i.status === 'RESOLVED' || i.status === 'CLOSED').length,
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-2xl lg:text-3xl font-display font-bold text-white">
                        Incident Management
                    </h1>
                    <p className="text-dark-400 mt-1">Track and resolve operational incidents</p>
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                    { label: 'Total Incidents', value: statusCounts.all, color: 'primary' },
                    { label: 'Active', value: statusCounts.ACTIVE, color: 'danger' },
                    { label: 'Investigating', value: statusCounts.INVESTIGATING, color: 'warning' },
                    { label: 'Resolved', value: statusCounts.RESOLVED, color: 'success' },
                ].map((stat) => (
                    <div key={stat.label} className="glass-card text-center py-4">
                        <p className="text-2xl font-bold text-white">{stat.value}</p>
                        <p className="text-sm text-dark-400">{stat.label}</p>
                    </div>
                ))}
            </div>

            {/* Filters */}
            <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-400" />
                    <input
                        type="text"
                        placeholder="Search incidents..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="input pl-10"
                    />
                </div>
                <div className="flex gap-2">
                    {['all', 'ACTIVE', 'INVESTIGATING', 'RESOLVED'].map((status) => (
                        <button
                            key={status}
                            onClick={() => setFilter(status)}
                            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${filter === status
                                    ? 'bg-primary-600 text-white'
                                    : 'bg-dark-800/50 text-dark-300 hover:bg-dark-700'
                                }`}
                        >
                            {status === 'all' ? 'All' : status.charAt(0) + status.slice(1).toLowerCase()}
                        </button>
                    ))}
                </div>
            </div>

            {/* Incidents List */}
            <div className="space-y-4">
                {filteredIncidents.length === 0 ? (
                    <div className="glass-card text-center py-12">
                        <AlertTriangle className="w-12 h-12 text-dark-500 mx-auto mb-4" />
                        <p className="text-dark-400">No incidents found</p>
                    </div>
                ) : (
                    filteredIncidents.map((incident, index) => (
                        <motion.div
                            key={incident.id || index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className="glass-card p-0 overflow-hidden"
                        >
                            {/* Header */}
                            <div
                                className="flex items-center gap-4 p-4 cursor-pointer hover:bg-dark-800/30 transition-colors"
                                onClick={() => setExpandedId(expandedId === incident.id ? null : incident.id)}
                            >
                                <div className={`p-3 rounded-xl ${incident.status === 'ACTIVE' ? 'bg-red-500/20' :
                                        incident.status === 'INVESTIGATING' ? 'bg-yellow-500/20' :
                                            'bg-green-500/20'
                                    }`}>
                                    {getStatusIcon(incident.status)}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-3 mb-1">
                                        <h3 className="font-semibold text-white truncate">{incident.title}</h3>
                                        <span className={`badge ${getStatusColor(incident.status)}`}>
                                            {incident.status}
                                        </span>
                                    </div>
                                    <p className="text-sm text-dark-400 truncate">{incident.description}</p>
                                </div>
                                <div className="text-right hidden sm:block">
                                    <p className="text-lg font-semibold text-white">
                                        ₹{incident.estimatedLoss?.toLocaleString() || 0}
                                    </p>
                                    <p className="text-xs text-dark-400">Estimated Loss</p>
                                </div>
                                <div className="text-dark-400">
                                    {expandedId === incident.id ? (
                                        <ChevronUp className="w-5 h-5" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5" />
                                    )}
                                </div>
                            </div>

                            {/* Expanded Details */}
                            {expandedId === incident.id && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: 'auto', opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className="border-t border-dark-700/50"
                                >
                                    <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <p className="text-sm text-dark-400 mb-1">Description</p>
                                            <p className="text-white">{incident.description}</p>
                                        </div>
                                        <div>
                                            <p className="text-sm text-dark-400 mb-1">Root Cause</p>
                                            <p className="text-white">{incident.rootCause || 'Under investigation'}</p>
                                        </div>
                                        <div>
                                            <p className="text-sm text-dark-400 mb-1">Start Time</p>
                                            <p className="text-white">
                                                {incident.startTime ? format(new Date(incident.startTime), 'PPpp') : 'N/A'}
                                            </p>
                                        </div>
                                        <div>
                                            <p className="text-sm text-dark-400 mb-1">Resolution</p>
                                            <p className="text-white">{incident.resolution || 'Pending'}</p>
                                        </div>
                                    </div>
                                    <div className="p-4 border-t border-dark-700/50 flex gap-3">
                                        <button className="btn-primary text-sm">
                                            View Details
                                            <ExternalLink className="w-4 h-4" />
                                        </button>
                                        <button className="btn-secondary text-sm">
                                            Update Status
                                        </button>
                                        {incident.status !== 'RESOLVED' && (
                                            <button className="btn-success text-sm">
                                                <CheckCircle className="w-4 h-4" />
                                                Mark Resolved
                                            </button>
                                        )}
                                    </div>
                                </motion.div>
                            )}
                        </motion.div>
                    ))
                )}
            </div>
        </div>
    );
}

function getMockIncidents() {
    return [
        {
            id: '1',
            title: 'Machine 1 Throughput Drop',
            description: 'Production line 1 experienced a 25% drop in throughput during morning shift',
            status: 'ACTIVE',
            estimatedLoss: 45000,
            startTime: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
            rootCause: null,
            resolution: null,
        },
        {
            id: '2',
            title: 'Shift B Idle Time Spike',
            description: 'Abnormal idle time pattern detected during Shift B operations',
            status: 'INVESTIGATING',
            estimatedLoss: 28000,
            startTime: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
            rootCause: 'Initial analysis suggests workflow bottleneck at station 3',
            resolution: null,
        },
        {
            id: '3',
            title: 'Quality Control Alert',
            description: 'Quality scores dropped below 90% threshold on multiple machines',
            status: 'MITIGATING',
            estimatedLoss: 62000,
            startTime: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
            rootCause: 'Calibration drift detected on inspection sensors',
            resolution: 'Recalibration in progress',
        },
        {
            id: '4',
            title: 'Morning Shift Overload',
            description: 'Resource overload led to cascading delays across production floor',
            status: 'RESOLVED',
            estimatedLoss: 35000,
            startTime: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
            rootCause: 'Insufficient staffing during peak hours',
            resolution: 'Adjusted shift scheduling and added buffer capacity',
        },
        {
            id: '5',
            title: 'Machine 3 Micro-Downtime',
            description: 'Frequent micro-stoppages detected on Machine 3',
            status: 'RESOLVED',
            estimatedLoss: 18500,
            startTime: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
            rootCause: 'Worn belt causing intermittent slippage',
            resolution: 'Replaced belt and scheduled preventive maintenance',
        },
    ];
}
