import { useState, useEffect } from 'react';
import {
    Search,
    Filter,
    AlertCircle,
    Clock,
    CheckCircle,
    ChevronDown,
    ChevronUp,
    AlertTriangle,
    Factory,
    DollarSign,
    ArrowRight,
    Eye,
    Zap,
} from 'lucide-react';
import {
    generateHistoricalData,
    generateMachineEvents,
    generateAnomalies,
    machines,
} from '../data/demoData';

export default function Incidents() {
    const [incidents, setIncidents] = useState([]);
    const [expandedId, setExpandedId] = useState(null);
    const [statusFilter, setStatusFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [timeline, setTimeline] = useState([]);

    useEffect(() => {
        // Generate incidents from anomalies
        const events = generateMachineEvents(new Date());
        const anomalies = generateAnomalies(events);

        // Convert anomalies to incidents with more details
        const generatedIncidents = [
            {
                id: 'INC-001',
                title: 'Machine 2 Throughput Drop',
                description: 'CNC Machine 2 showing 23% reduction in throughput compared to baseline. Pattern detected over last 4 hours.',
                status: 'active',
                severity: 'high',
                startTime: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                source: 'M2 - CNC Machine 2',
                estimatedLoss: 28000,
                anomalies: 3,
                rootCause: null,
                assignee: null,
                timeline: [
                    { time: '10:30', event: 'Anomaly detected: efficiency dropped to 72%' },
                    { time: '10:45', event: 'Pattern confirmed: consistent underperformance' },
                    { time: '11:00', event: 'Incident created automatically' },
                    { time: '11:15', event: 'AOIA: Preliminary analysis suggests bearing wear' },
                ],
            },
            {
                id: 'INC-002',
                title: 'Shift B Extended Idle Time',
                description: 'Cumulative idle time for Shift B exceeded threshold by 45%. Multiple operators affected.',
                status: 'investigating',
                severity: 'medium',
                startTime: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
                source: 'Shift B',
                estimatedLoss: 15000,
                anomalies: 2,
                rootCause: 'Material shortage suspected',
                assignee: 'Amit Patel',
                timeline: [
                    { time: '14:30', event: 'Idle time threshold exceeded' },
                    { time: '15:00', event: 'Assigned to Amit Patel for investigation' },
                    { time: '15:30', event: 'Root cause identified: waiting for materials' },
                ],
            },
            {
                id: 'INC-003',
                title: 'Hidden Micro-Downtimes Cluster',
                description: '12 micro-downtimes (<3 min each) detected across Assembly Line 1. Cumulative impact exceeds normal threshold.',
                status: 'active',
                severity: 'medium',
                startTime: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
                source: 'M5 - Assembly Line 1',
                estimatedLoss: 8500,
                anomalies: 12,
                rootCause: null,
                assignee: null,
                hidden: true,
                timeline: [
                    { time: '08:00', event: 'First micro-downtime detected (45 sec)' },
                    { time: '09:30', event: 'Pattern detected: recurring brief stoppages' },
                    { time: '11:00', event: 'Cluster analysis complete: 12 events, hidden loss ₹8,500' },
                ],
            },
            {
                id: 'INC-004',
                title: 'Quality Score Decline',
                description: 'Product quality scores dropped below acceptable threshold on Press Machine 1.',
                status: 'resolved',
                severity: 'medium',
                startTime: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
                endTime: new Date(Date.now() - 20 * 60 * 60 * 1000).toISOString(),
                source: 'M4 - Press Machine 1',
                estimatedLoss: 12000,
                actualLoss: 9500,
                anomalies: 1,
                rootCause: 'Equipment calibration drift',
                resolution: 'Recalibrated press settings and die alignment',
                assignee: 'Vikram Rao',
                timeline: [
                    { time: 'Yesterday 14:00', event: 'Quality anomaly detected' },
                    { time: 'Yesterday 15:00', event: 'Investigation started' },
                    { time: 'Yesterday 16:30', event: 'Root cause identified' },
                    { time: 'Yesterday 18:00', event: 'Resolution applied, quality normalized' },
                ],
            },
            {
                id: 'INC-005',
                title: 'Shift Transition Gap',
                description: 'Average 18-minute unproductive gap detected during Shift A to B transitions this week.',
                status: 'investigating',
                severity: 'low',
                startTime: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
                source: 'All Machines',
                estimatedLoss: 22000,
                anomalies: 5,
                rootCause: 'Handover process inefficiency',
                assignee: null,
                hidden: true,
                timeline: [
                    { time: '3 days ago', event: 'Pattern analysis started' },
                    { time: '2 days ago', event: 'Confirmed: consistent gaps during transitions' },
                    { time: 'Yesterday', event: 'AOIA recommendation: optimize handover checklist' },
                ],
            },
        ];

        setIncidents(generatedIncidents);

        // Build event timeline from today's events
        const recentEvents = events
            .filter(e => e.eventType !== 'PRODUCTION')
            .slice(-20)
            .map(e => ({
                time: new Date(e.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                type: e.eventType,
                machine: e.machineName,
                duration: e.duration,
                loss: e.lossAmount || 0,
                reason: e.reason,
            }));
        setTimeline(recentEvents.reverse());
    }, []);

    const filteredIncidents = incidents.filter((inc) => {
        const matchesStatus = statusFilter === 'all' || inc.status === statusFilter;
        const matchesSearch = inc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            inc.description.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesStatus && matchesSearch;
    });

    const getStatusStyle = (status) => {
        switch (status) {
            case 'active': return 'badge-danger';
            case 'investigating': return 'badge-warning';
            case 'resolved': return 'badge-success';
            default: return 'badge-secondary';
        }
    };

    const getSeverityStyle = (severity) => {
        switch (severity) {
            case 'high': return 'text-red-600';
            case 'medium': return 'text-amber-600';
            case 'low': return 'text-gray-600';
            default: return 'text-gray-600';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'active': return <AlertCircle className="w-5 h-5 text-red-600" />;
            case 'investigating': return <Clock className="w-5 h-5 text-amber-600" />;
            case 'resolved': return <CheckCircle className="w-5 h-5 text-accent-600" />;
            default: return <AlertCircle className="w-5 h-5 text-gray-600" />;
        }
    };

    const stats = {
        total: incidents.length,
        active: incidents.filter(i => i.status === 'active').length,
        investigating: incidents.filter(i => i.status === 'investigating').length,
        resolved: incidents.filter(i => i.status === 'resolved').length,
        totalLoss: incidents.reduce((sum, i) => sum + (i.actualLoss || i.estimatedLoss), 0),
        hiddenLoss: incidents.filter(i => i.hidden).reduce((sum, i) => sum + i.estimatedLoss, 0),
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="page-header">
                <h1 className="page-title">Incidents & Anomalies</h1>
                <p className="page-subtitle">Track, investigate, and resolve operational incidents</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center">
                        <AlertTriangle className="w-5 h-5 text-gray-600" />
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                        <p className="text-xs text-gray-500">Total</p>
                    </div>
                </div>
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-red-50 flex items-center justify-center">
                        <AlertCircle className="w-5 h-5 text-red-600" />
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-900">{stats.active}</p>
                        <p className="text-xs text-gray-500">Active</p>
                    </div>
                </div>
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center">
                        <Clock className="w-5 h-5 text-amber-600" />
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-900">{stats.investigating}</p>
                        <p className="text-xs text-gray-500">Investigating</p>
                    </div>
                </div>
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-accent-50 flex items-center justify-center">
                        <CheckCircle className="w-5 h-5 text-accent-600" />
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-900">{stats.resolved}</p>
                        <p className="text-xs text-gray-500">Resolved</p>
                    </div>
                </div>
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-red-50 flex items-center justify-center">
                        <DollarSign className="w-5 h-5 text-red-600" />
                    </div>
                    <div>
                        <p className="text-xl font-bold text-gray-900">₹{(stats.totalLoss / 1000).toFixed(0)}K</p>
                        <p className="text-xs text-gray-500">Total Loss</p>
                    </div>
                </div>
                <div className="card p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-purple-50 flex items-center justify-center">
                        <Zap className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                        <p className="text-xl font-bold text-gray-900">₹{(stats.hiddenLoss / 1000).toFixed(0)}K</p>
                        <p className="text-xs text-gray-500">Hidden Loss</p>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="card p-4">
                <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search incidents..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="input pl-10"
                        />
                    </div>
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                        className="input w-auto"
                    >
                        <option value="all">All Status</option>
                        <option value="active">Active</option>
                        <option value="investigating">Investigating</option>
                        <option value="resolved">Resolved</option>
                    </select>
                </div>
            </div>

            {/* Incident List */}
            <div className="space-y-4">
                {filteredIncidents.map((incident) => (
                    <div key={incident.id} className={`card ${incident.hidden ? 'border-purple-200' : ''}`}>
                        <div
                            className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                            onClick={() => setExpandedId(expandedId === incident.id ? null : incident.id)}
                        >
                            <div className="flex items-start gap-4">
                                <div className="mt-1">{getStatusIcon(incident.status)}</div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-start justify-between gap-4">
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <span className="text-sm text-gray-400">{incident.id}</span>
                                                {incident.hidden && (
                                                    <span className="badge bg-purple-100 text-purple-700">HIDDEN</span>
                                                )}
                                            </div>
                                            <h3 className="font-semibold text-gray-900 mt-1">{incident.title}</h3>
                                            <p className="text-sm text-gray-500 mt-1">{incident.description}</p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <span className={getStatusStyle(incident.status)}>
                                                {incident.status}
                                            </span>
                                            {expandedId === incident.id ? (
                                                <ChevronUp className="w-5 h-5 text-gray-400" />
                                            ) : (
                                                <ChevronDown className="w-5 h-5 text-gray-400" />
                                            )}
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4 mt-3 text-sm">
                                        <span className={`font-medium ${getSeverityStyle(incident.severity)}`}>
                                            {incident.severity.toUpperCase()}
                                        </span>
                                        <span className="text-gray-500">{incident.source}</span>
                                        <span className="text-gray-500">
                                            {incident.anomalies} anomalies
                                        </span>
                                        <span className="font-semibold text-red-600">
                                            ₹{incident.estimatedLoss.toLocaleString()}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Expanded Details */}
                        {expandedId === incident.id && (
                            <div className="px-4 pb-4 pt-0 border-t border-gray-100">
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-4">
                                    <div className="space-y-4">
                                        <div>
                                            <p className="text-sm font-medium text-gray-500">Root Cause</p>
                                            <p className="text-gray-900 mt-1">
                                                {incident.rootCause || 'Under investigation'}
                                            </p>
                                        </div>
                                        {incident.resolution && (
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Resolution</p>
                                                <p className="text-gray-900 mt-1">{incident.resolution}</p>
                                            </div>
                                        )}
                                        {incident.assignee && (
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Assigned To</p>
                                                <p className="text-gray-900 mt-1">{incident.assignee}</p>
                                            </div>
                                        )}
                                    </div>

                                    {/* Timeline */}
                                    <div>
                                        <p className="text-sm font-medium text-gray-500 mb-3">Timeline</p>
                                        <div className="space-y-3">
                                            {incident.timeline?.map((event, index) => (
                                                <div key={index} className="flex gap-3">
                                                    <span className="text-xs text-gray-400 w-20 flex-shrink-0">{event.time}</span>
                                                    <div className="relative">
                                                        <div className="absolute left-0 top-2 w-2 h-2 rounded-full bg-gray-300" />
                                                        <p className="text-sm text-gray-700 pl-5">{event.event}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-3 mt-6">
                                    {incident.status !== 'resolved' && (
                                        <>
                                            <button className="btn-primary text-sm">
                                                Update Status
                                            </button>
                                            <button className="btn-secondary text-sm">
                                                Assign
                                            </button>
                                            <button className="btn-secondary text-sm">
                                                Ask AOIA
                                            </button>
                                        </>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}
