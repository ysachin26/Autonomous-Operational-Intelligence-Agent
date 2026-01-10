import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Send,
    Bot,
    User,
    Sparkles,
    Loader2,
    HelpCircle,
    TrendingDown,
    AlertTriangle,
    Lightbulb,
    RefreshCw,
} from 'lucide-react';
import api from '../services/api';

const quickActions = [
    { icon: HelpCircle, label: 'Show status', query: "What's the current operational status?" },
    { icon: AlertTriangle, label: 'View anomalies', query: 'What anomalies were detected today?' },
    { icon: TrendingDown, label: 'Loss analysis', query: 'How much money are we losing?' },
    { icon: Lightbulb, label: 'Get recommendations', query: 'What optimizations do you suggest?' },
];

export default function Agent() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            role: 'assistant',
            content: `👋 Hello! I'm **AOIA**, your Autonomous Operational Intelligence Agent.

I can help you with:
- 📊 **Status Overview** - Current operational metrics
- 🔍 **Anomaly Detection** - Issues and problems detected
- 💰 **Loss Analysis** - Financial impact of inefficiencies
- 💡 **Recommendations** - AI-powered optimization suggestions
- 📋 **Explanations** - Root cause analysis

What would you like to know about your operations?`,
        },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async (content) => {
        if (!content.trim()) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: content.trim(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await api.post('/api/chat', {
                message: content,
                sessionId,
            });

            if (response.data.success) {
                setSessionId(response.data.data.sessionId);
                setMessages((prev) => [
                    ...prev,
                    {
                        id: Date.now() + 1,
                        role: 'assistant',
                        content: response.data.data.message,
                    },
                ]);
            }
        } catch (error) {
            // Fallback to mock response
            const mockResponse = generateMockResponse(content);
            setMessages((prev) => [
                ...prev,
                {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: mockResponse,
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        sendMessage(input);
    };

    const handleQuickAction = (query) => {
        sendMessage(query);
    };

    const clearChat = () => {
        setMessages([
            {
                id: 1,
                role: 'assistant',
                content: `👋 Chat cleared! How can I help you with your operations?`,
            },
        ]);
        setSessionId(null);
    };

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h1 className="text-2xl lg:text-3xl font-display font-bold text-white flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                            <Bot className="w-6 h-6 text-white" />
                        </div>
                        AOIA Assistant
                    </h1>
                    <p className="text-dark-400 mt-1">Ask anything about your operations</p>
                </div>
                <button onClick={clearChat} className="btn-ghost">
                    <RefreshCw className="w-4 h-4" />
                    Clear Chat
                </button>
            </div>

            {/* Quick Actions */}
            <div className="flex flex-wrap gap-2 mb-4">
                {quickActions.map((action) => (
                    <button
                        key={action.label}
                        onClick={() => handleQuickAction(action.query)}
                        disabled={isLoading}
                        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-dark-800/50 border border-dark-700 hover:border-primary-500/50 text-sm text-dark-300 hover:text-white transition-all"
                    >
                        <action.icon className="w-4 h-4 text-primary-400" />
                        {action.label}
                    </button>
                ))}
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto glass-card p-4 space-y-4">
                <AnimatePresence>
                    {messages.map((message) => (
                        <motion.div
                            key={message.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div
                                className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${message.role === 'user'
                                        ? 'bg-primary-600'
                                        : 'bg-gradient-to-br from-primary-500 to-accent-500'
                                    }`}
                            >
                                {message.role === 'user' ? (
                                    <User className="w-4 h-4 text-white" />
                                ) : (
                                    <Sparkles className="w-4 h-4 text-white" />
                                )}
                            </div>
                            <div
                                className={`max-w-[80%] p-4 rounded-2xl ${message.role === 'user'
                                        ? 'bg-primary-600/20 border border-primary-500/30'
                                        : 'bg-dark-800/50 border border-dark-700/50'
                                    }`}
                            >
                                <div className="prose prose-invert prose-sm max-w-none">
                                    {formatMessage(message.content)}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex gap-3"
                    >
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                            <Sparkles className="w-4 h-4 text-white" />
                        </div>
                        <div className="p-4 rounded-2xl bg-dark-800/50 border border-dark-700/50">
                            <div className="flex items-center gap-2 text-dark-400">
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Analyzing your operations...
                            </div>
                        </div>
                    </motion.div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="mt-4">
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about operations, anomalies, losses, or optimizations..."
                        disabled={isLoading}
                        className="input flex-1"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="btn-primary px-6"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </form>
        </div>
    );
}

function formatMessage(content) {
    // Simple markdown-like formatting
    return content.split('\n').map((line, i) => {
        // Headers
        if (line.startsWith('##')) {
            return <h3 key={i} className="text-lg font-semibold text-white mt-4 mb-2">{line.replace('##', '').trim()}</h3>;
        }
        // Bold
        let formatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Lists
        if (line.startsWith('•') || line.startsWith('-')) {
            return <li key={i} className="ml-4 text-dark-200" dangerouslySetInnerHTML={{ __html: formatted.replace(/^[•-]\s*/, '') }} />;
        }
        // Numbers
        if (/^\d+\./.test(line)) {
            return <li key={i} className="ml-4 text-dark-200 list-decimal" dangerouslySetInnerHTML={{ __html: formatted.replace(/^\d+\.\s*/, '') }} />;
        }
        // Regular paragraph
        if (line.trim()) {
            return <p key={i} className="text-dark-200 mb-2" dangerouslySetInnerHTML={{ __html: formatted }} />;
        }
        return null;
    });
}

function generateMockResponse(query) {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('status') || lowerQuery.includes('overview')) {
        return `📊 **Current Operational Status**

Based on my analysis:
• **Efficiency Score:** 87% (+3.2% from yesterday)
• **Active Incidents:** 3 requiring attention
• **Open Anomalies:** 8 detected in last 24h
• **Pending Actions:** 5 recommendations available

⚠️ **Priority Alert:** Machine 2 showing degradation patterns. Recommend scheduling maintenance within 48 hours.

Would you like me to elaborate on any specific area?`;
    }

    if (lowerQuery.includes('anomal') || lowerQuery.includes('issue') || lowerQuery.includes('problem')) {
        return `🔍 **Anomaly Analysis**

I've detected **8 anomalies** in the last 24 hours:

| Type | Count | Severity |
|------|-------|----------|
| Idle Spike | 3 | Medium |
• **Throughput Drop:** 2 incidents (High)
• **Quality Decline:** 2 incidents (Medium)
• **Machine Slowdown:** 1 incident (Critical)

**Most Critical:** Machine 2 throughput dropped 25% below baseline at 09:45 AM. Deviation suggests possible mechanical issue.

Shall I investigate the root cause for any specific anomaly?`;
    }

    if (lowerQuery.includes('loss') || lowerQuery.includes('money') || lowerQuery.includes('cost')) {
        return `💰 **Loss Analysis**

**Last 24 Hours:**
• **Total Estimated Loss:** ₹45,000
• **Active Incident Impact:** ₹73,000

**By Category:**
1. Throughput drops: ₹28,000 (40%)
2. Idle time spikes: ₹18,000 (26%)
3. Quality issues: ₹15,000 (21%)
4. Machine downtime: ₹9,000 (13%)

**Top Contributor:** Machine 1 throughput drop (₹28,000)

💡 If you implement my top 3 recommendations, estimated recovery is **₹115,000** this week.`;
    }

    if (lowerQuery.includes('recommend') || lowerQuery.includes('suggest') || lowerQuery.includes('optim')) {
        return `💡 **Top Optimization Recommendations**

**1. Schedule Preventive Maintenance - Machine 2** 🔴 URGENT
• Estimated Impact: ₹55,000
• Confidence: 94%
• Reasoning: Vibration patterns match pre-failure signature

**2. Rebalance Shift B Workload** 🟡 HIGH
• Estimated Impact: ₹32,000
• Confidence: 89%
• Reasoning: Station 3 overloaded by 40%

**3. Optimize Task Routing** 🟢 MEDIUM
• Estimated Impact: ₹28,000
• Confidence: 82%
• Reasoning: Priority routing can improve throughput 8%

Would you like me to execute any of these recommendations?`;
    }

    return `🧠 I understand you're asking about: "${query}"

Based on my analysis of your operations:
• Current efficiency is at **87%**
• No critical alerts requiring immediate attention
• 5 optimization opportunities identified

I can help you with:
• **Status updates** - "What's the current status?"
• **Anomaly detection** - "Show recent anomalies"
• **Loss analysis** - "How much are we losing?"
• **Recommendations** - "What should we optimize?"

What specific information would you like?`;
}
