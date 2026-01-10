// AOIA Shared Types

// User & Organization
export interface User {
    id: string;
    email: string;
    name: string;
    role: 'ADMIN' | 'MANAGER' | 'OPERATOR';
    organizationId: string;
}

export interface Organization {
    id: string;
    name: string;
    industry: Industry;
    costPerMinute: number;
}

export type Industry =
    | 'BPO'
    | 'MANUFACTURING'
    | 'LOGISTICS'
    | 'RETAIL'
    | 'HEALTHCARE'
    | 'GENERAL';

// Metrics
export interface Metric {
    id: string;
    organizationId: string;
    timestamp: string;
    metricType: MetricType;
    value: number;
    unit: string;
    source: string;
    metadata?: Record<string, any>;
}

export type MetricType =
    | 'UTILIZATION'
    | 'THROUGHPUT'
    | 'IDLE_TIME'
    | 'RESPONSE_TIME'
    | 'ERROR_RATE'
    | 'DOWNTIME'
    | 'CALL_DURATION'
    | 'TASK_COMPLETION'
    | 'MACHINE_SPEED'
    | 'QUALITY_SCORE';

// Anomalies
export interface Anomaly {
    id: string;
    organizationId: string;
    timestamp: string;
    anomalyType: AnomalyType;
    severity: Severity;
    source: string;
    description: string;
    value: number;
    expectedValue: number;
    deviation: number;
    status: AnomalyStatus;
}

export type AnomalyType =
    | 'IDLE_SPIKE'
    | 'THROUGHPUT_DROP'
    | 'RESPONSE_DELAY'
    | 'MACHINE_SLOWDOWN'
    | 'QUALITY_DECLINE'
    | 'OVERLOAD'
    | 'UNDERPERFORMANCE'
    | 'PATTERN_BREAK';

export type Severity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type AnomalyStatus =
    | 'OPEN'
    | 'ACKNOWLEDGED'
    | 'INVESTIGATING'
    | 'RESOLVED'
    | 'FALSE_POSITIVE';

// Incidents
export interface Incident {
    id: string;
    organizationId: string;
    title: string;
    description: string;
    startTime: string;
    endTime?: string;
    status: IncidentStatus;
    estimatedLoss: number;
    actualLoss?: number;
    rootCause?: string;
    resolution?: string;
}

export type IncidentStatus =
    | 'ACTIVE'
    | 'INVESTIGATING'
    | 'MITIGATING'
    | 'RESOLVED'
    | 'CLOSED';

// Recommendations
export interface Recommendation {
    id: string;
    organizationId: string;
    incidentId?: string;
    title: string;
    description: string;
    actionType: ActionType;
    priority: Priority;
    status: RecommendationStatus;
    estimatedImpact: number;
    actualImpact?: number;
    confidence: number;
    reasoning: string;
    actionPayload?: Record<string, any>;
}

export type ActionType =
    | 'REBALANCE_WORKLOAD'
    | 'SCHEDULE_MAINTENANCE'
    | 'ADJUST_ROUTING'
    | 'ALERT_SUPERVISOR'
    | 'MODIFY_PROCESS'
    | 'TRAINING_NEEDED'
    | 'RESOURCE_ALLOCATION'
    | 'CUSTOM';

export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';

export type RecommendationStatus =
    | 'PENDING'
    | 'APPROVED'
    | 'EXECUTING'
    | 'COMPLETED'
    | 'REJECTED'
    | 'FAILED';

// API Responses
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
}

// Dashboard
export interface DashboardData {
    organization: {
        name: string;
        industry: Industry;
    };
    kpis: {
        activeIncidents: number;
        openAnomalies: number;
        pendingRecommendations: number;
        efficiencyScore: number;
    };
    loss: {
        last24h: number;
        last7d: number;
        trend: Array<{ date: string; loss: number }>;
    };
    savings: {
        total: number;
        actionsCompleted: number;
    };
    recentAnomalies: Anomaly[];
    recentIncidents: Incident[];
}

// Chat
export interface ChatMessage {
    id: string;
    sessionId: string;
    role: 'USER' | 'ASSISTANT' | 'SYSTEM';
    content: string;
    metadata?: Record<string, any>;
    createdAt: string;
}

module.exports = {};
