import { useState, useRef, useEffect } from 'react';
import {
    Send,
    Bot,
    User,
    Sparkles,
    Lightbulb,
    AlertCircle,
    BarChart3,
    Loader2,
    Factory,
    DollarSign,
    TrendingUp,
    Clock,
    Zap,
} from 'lucide-react';
import {
    machines,
    employees,
    shifts,
    generateHistoricalData,
    generateRealtimeMetrics,
    generateMachineEvents,
    calculateTotalLoss,
    generateAnomalies,
} from '../data/demoData';

const quickActions = [
    { icon: AlertCircle, label: 'Explain top incident', query: 'What is the most critical issue right now?' },
    { icon: Factory, label: 'Machine status', query: 'Show me the status of all machines' },
    { icon: DollarSign, label: 'Loss breakdown', query: 'Break down today\'s losses by category' },
    { icon: Zap, label: 'Hidden losses', query: 'What hidden losses have you detected?' },
    { icon: Lightbulb, label: 'Recommendations', query: 'What are your top recommendations?' },
];

export default function Agent() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [operationalData, setOperationalData] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Load operational data for context
        const events = generateMachineEvents(new Date());
        const losses = calculateTotalLoss(events);
        const anomalies = generateAnomalies(events);
        const metrics = generateRealtimeMetrics();
        const history = generateHistoricalData();

        setOperationalData({ events, losses, anomalies, metrics, history });

        // Welcome message
        setMessages([{
            id: 1,
            role: 'assistant',
            content: `Hello! I'm **AOIA**, your Autonomous Operational Intelligence Agent.

I'm currently monitoring your operations and have detected:
- **${anomalies.length} active anomalies** requiring attention
- **₹${losses.total.toLocaleString()} in losses** today
- **${losses.microDowntime > 0 ? `₹${losses.microDowntime.toLocaleString()} in hidden losses` : 'No hidden losses'}** from micro-downtimes

How can I help you optimize operations today?`,
            timestamp: new Date(),
        }]);
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const generateResponse = (query) => {
        const lowerQuery = query.toLowerCase();
        const { events, losses, anomalies, metrics, history } = operationalData;

        // Machine status query
        if (lowerQuery.includes('machine') && (lowerQuery.includes('status') || lowerQuery.includes('how'))) {
            const machineStatus = machines.map(m => {
                const machineEvents = events.filter(e => e.machineId === m.id);
                const productionEvents = machineEvents.filter(e => e.eventType === 'PRODUCTION');
                const idleEvents = machineEvents.filter(e => e.eventType === 'IDLE' || e.eventType === 'MICRO_DOWNTIME');
                const avgEfficiency = productionEvents.length > 0
                    ? (productionEvents.reduce((s, e) => s + e.efficiency, 0) / productionEvents.length).toFixed(1)
                    : 0;
                const totalLoss = machineEvents.filter(e => e.lossAmount).reduce((s, e) => s + e.lossAmount, 0);

                return `| ${m.id} | ${m.name} | ${avgEfficiency}% | ₹${totalLoss.toLocaleString()} |`;
            }).join('\n');

            return `## Machine Status Overview

| ID | Machine | Efficiency | Loss Today |
|----|---------|------------|------------|
${machineStatus}

### Key Insights
- **Best performer:** ${machines[0].id} with highest efficiency
- **Needs attention:** M2 showing elevated losses from idle time
- **Recommendation:** Schedule preventive maintenance for underperforming machines`;
        }

        // Loss breakdown query
        if (lowerQuery.includes('loss') && (lowerQuery.includes('breakdown') || lowerQuery.includes('category'))) {
            return `## Today's Loss Breakdown

| Category | Amount | % of Total |
|----------|--------|------------|
| Idle Time | ₹${losses.idle.toLocaleString()} | ${((losses.idle / losses.total) * 100).toFixed(0)}% |
| Breakdowns | ₹${losses.breakdown.toLocaleString()} | ${((losses.breakdown / losses.total) * 100).toFixed(0)}% |
| Hidden (Micro-downtimes) | ₹${losses.microDowntime.toLocaleString()} | ${((losses.microDowntime / losses.total) * 100).toFixed(0)}% |
| Low Efficiency | ₹${losses.lowEfficiency.toLocaleString()} | ${((losses.lowEfficiency / losses.total) * 100).toFixed(0)}% |
| **Total** | **₹${losses.total.toLocaleString()}** | 100% |

### Analysis
- **Biggest contributor:** ${losses.idle > losses.breakdown ? 'Idle time' : 'Breakdowns'} causing ${Math.max((losses.idle / losses.total) * 100, (losses.breakdown / losses.total) * 100).toFixed(0)}% of losses
- **Hidden losses:** ₹${losses.microDowntime.toLocaleString()} from ${events.filter(e => e.eventType === 'MICRO_DOWNTIME').length} micro-downtimes
- **Potential savings:** Optimizing idle time could save ₹${Math.floor(losses.idle * 0.6).toLocaleString()}/day`;
        }

        // Hidden losses query
        if (lowerQuery.includes('hidden')) {
            const microDowntimes = events.filter(e => e.eventType === 'MICRO_DOWNTIME');
            return `## Hidden Loss Analysis

I've detected **${microDowntimes.length} micro-downtimes** today that individually appear minor but collectively cause significant losses.

### Summary
- **Total hidden loss:** ₹${losses.microDowntime.toLocaleString()}
- **Average duration:** ${microDowntimes.length > 0 ? (microDowntimes.reduce((s, e) => s + e.duration, 0) / microDowntimes.length).toFixed(1) : 0} minutes
- **Most affected:** ${microDowntimes.length > 0 ? microDowntimes[0].machineName : 'N/A'}

### Why These Are Hidden
These inefficiencies are typically:
- ⏱️ **Too short** (<3 minutes) to trigger standard alerts
- 🔄 **Too frequent** to investigate individually
- 📊 **Not visible** in daily reports

### Recommendation
Schedule proactive maintenance for machines with recurring micro-downtimes. Estimated savings: **₹${Math.floor(losses.microDowntime * 0.7).toLocaleString()}/day**`;
        }

        // Critical issue query
        if (lowerQuery.includes('critical') || lowerQuery.includes('issue') || lowerQuery.includes('incident')) {
            const criticalAnomaly = anomalies.find(a => a.severity === 'HIGH') || anomalies[0];
            if (criticalAnomaly) {
                return `## Most Critical Issue

### ${criticalAnomaly.type.replace('_', ' ')}
**Severity:** ${criticalAnomaly.severity} | **Confidence:** ${(criticalAnomaly.confidence * 100).toFixed(0)}%

**Source:** ${criticalAnomaly.source}
**Description:** ${criticalAnomaly.description}
**Estimated Loss:** ₹${criticalAnomaly.estimatedLoss.toLocaleString()}

### Root Cause Analysis
Based on pattern analysis, the most likely causes are:
1. **Equipment wear** (75% confidence) - Component degradation affecting performance
2. **Process variation** (60% confidence) - Inconsistent input quality

### Recommended Actions
1. ⚡ Immediate: Inspect affected equipment for visible issues
2. 🔧 Short-term: Schedule maintenance window within 24 hours
3. 📊 Long-term: Implement predictive maintenance sensors

Would you like me to create a maintenance ticket?`;
            }
        }

        // Recommendations query
        if (lowerQuery.includes('recommend') || lowerQuery.includes('suggest') || lowerQuery.includes('optim')) {
            return `## Top AI Recommendations

Based on the last 7 days of operational data, here are my optimization suggestions:

### 1. Schedule Preventive Maintenance for M2
- **Potential savings:** ₹55,000/week
- **Confidence:** 94%
- **Reason:** Machine showing 15% efficiency decline pattern
- **Action:** Schedule during next planned downtime

### 2. Rebalance Shift B Workload
- **Potential savings:** ₹32,000/week  
- **Confidence:** 89%
- **Reason:** Operator overload detected, causing 23% more idle time
- **Action:** Redistribute 2 tasks to Shift C

### 3. Optimize Shift Transitions
- **Potential savings:** ₹18,000/week
- **Confidence:** 82%
- **Reason:** Average 15-min gap between shifts
- **Action:** Implement parallel handover process

### 4. Address Hidden Micro-Downtimes
- **Potential savings:** ₹12,000/week
- **Confidence:** 78%
- **Reason:** ${events.filter(e => e.eventType === 'MICRO_DOWNTIME').length} cumulative small stoppages
- **Action:** Investigate root causes, likely sensor calibration

**Total potential weekly savings: ₹1,17,000**

Would you like me to execute any of these recommendations?`;
        }

        // Shift performance
        if (lowerQuery.includes('shift')) {
            return `## Shift Performance Analysis

| Shift | Efficiency | Target | Gap | Est. Loss |
|-------|------------|--------|-----|-----------|
| Shift A (06:00-14:00) | 86% | 90% | -4% | ₹32,000 |
| Shift B (14:00-22:00) | 72% | 88% | -16% | ₹58,000 |
| Shift C (22:00-06:00) | 84% | 85% | -1% | ₹35,000 |

### Key Findings
- **Shift B is significantly underperforming** with a 16% efficiency gap
- Root cause: Operator shortage + material wait times
- Peak efficiency across all shifts: 10:00-12:00

### Recommendations
1. Add 1 operator to Shift B during peak hours
2. Pre-stage materials before shift transitions
3. Investigate night shift (C) energy consumption patterns`;
        }

        // Default response
        return `I understand you're asking about: "${query}"

Here's what I can help you with:
- **Machine status** - "How are the machines performing?"
- **Loss analysis** - "Break down today's losses"
- **Hidden losses** - "What hidden inefficiencies have you found?"
- **Incidents** - "What's the most critical issue?"
- **Recommendations** - "What should we optimize?"
- **Shift analysis** - "How are the shifts performing?"

What would you like to explore?`;
    };

    const handleSend = async (query = input) => {
        if (!query.trim() || !operationalData) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: query,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Simulate AI processing
        await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1000));

        const response = generateResponse(query);

        const assistantMessage = {
            id: Date.now() + 1,
            role: 'assistant',
            content: response,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setIsLoading(false);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col">
            {/* Header */}
            <div className="flex-shrink-0 mb-4">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg">
                        <Bot className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-gray-900">AOIA Co-Pilot</h1>
                        <p className="text-sm text-gray-500">Your autonomous operational intelligence assistant</p>
                    </div>
                    <div className="ml-auto flex items-center gap-2 text-sm text-accent-600">
                        <span className="w-2 h-2 rounded-full bg-accent-500 animate-pulse" />
                        Monitoring {machines.length} machines
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="flex-shrink-0 mb-4">
                <div className="flex flex-wrap gap-2">
                    {quickActions.map((action, index) => (
                        <button
                            key={index}
                            onClick={() => handleSend(action.query)}
                            className="btn-secondary text-sm"
                            disabled={isLoading}
                        >
                            <action.icon className="w-4 h-4" />
                            {action.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto card p-4 space-y-4">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${message.role === 'user'
                            ? 'bg-primary-100'
                            : 'bg-gradient-to-br from-primary-500 to-primary-700'
                            }`}>
                            {message.role === 'user' ? (
                                <User className="w-4 h-4 text-primary-600" />
                            ) : (
                                <Bot className="w-4 h-4 text-white" />
                            )}
                        </div>
                        <div className={`max-w-[85%] ${message.role === 'user' ? 'text-right' : ''}`}>
                            <div className={`inline-block rounded-xl px-4 py-3 ${message.role === 'user'
                                ? 'bg-primary-600 text-white'
                                : 'bg-gray-50 text-gray-900 border border-gray-200'
                                }`}>
                                <MessageContent content={message.content} isUser={message.role === 'user'} />
                            </div>
                            <p className="text-xs text-gray-400 mt-1">
                                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
                            <Bot className="w-4 h-4 text-white" />
                        </div>
                        <div className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3">
                            <div className="flex items-center gap-2 text-gray-500">
                                <Loader2 className="w-4 h-4 animate-spin" />
                                <span className="text-sm">Analyzing operations...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="flex-shrink-0 mt-4">
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask about operations, losses, recommendations..."
                        className="input flex-1"
                        disabled={isLoading}
                    />
                    <button
                        onClick={() => handleSend()}
                        disabled={!input.trim() || isLoading}
                        className="btn-primary"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}

function MessageContent({ content, isUser }) {
    if (isUser) {
        return <p>{content}</p>;
    }

    const lines = content.split('\n');

    return (
        <div className="prose prose-sm max-w-none">
            {lines.map((line, i) => {
                // Headers
                if (line.startsWith('## ')) {
                    return <h3 key={i} className="font-bold text-base mt-3 first:mt-0 mb-2 text-gray-900">{line.slice(3)}</h3>;
                }
                if (line.startsWith('### ')) {
                    return <h4 key={i} className="font-semibold text-sm mt-3 mb-1 text-gray-800">{line.slice(4)}</h4>;
                }
                // List items
                if (line.startsWith('- ') || line.startsWith('• ')) {
                    return <p key={i} className="pl-3 py-0.5 text-sm" dangerouslySetInnerHTML={{ __html: formatText(line) }} />;
                }
                // Numbered items
                if (/^\d+\.\s/.test(line)) {
                    return <p key={i} className="pl-3 py-0.5 text-sm" dangerouslySetInnerHTML={{ __html: formatText(line) }} />;
                }
                // Table rows
                if (line.startsWith('|')) {
                    return null; // Tables need special handling, skip for now
                }
                // Regular text
                if (line.trim()) {
                    return <p key={i} className="py-0.5 text-sm" dangerouslySetInnerHTML={{ __html: formatText(line) }} />;
                }
                return null;
            })}
        </div>
    );
}

function formatText(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}
