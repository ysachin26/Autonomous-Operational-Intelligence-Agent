import { Router } from 'express';
import axios from 'axios';
import prisma from '../lib/prisma';
import { asyncHandler, AppError } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

const ML_ENGINE_URL = process.env.ML_ENGINE_URL || 'http://localhost:8000';

// Send chat message
router.post('/', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { message, sessionId } = req.body;

    if (!message) {
        throw new AppError('Message is required', 400);
    }

    const session = sessionId || `session_${req.user!.id}_${Date.now()}`;

    // Save user message
    await prisma.chatMessage.create({
        data: {
            sessionId: session,
            role: 'USER',
            content: message,
        },
    });

    // Get context from database
    const [recentAnomalies, recentIncidents, pendingRecs] = await Promise.all([
        prisma.anomaly.findMany({
            where: { organizationId: req.user!.organizationId },
            orderBy: { timestamp: 'desc' },
            take: 5,
        }),
        prisma.incident.findMany({
            where: { organizationId: req.user!.organizationId },
            orderBy: { startTime: 'desc' },
            take: 5,
        }),
        prisma.recommendation.findMany({
            where: { organizationId: req.user!.organizationId, status: 'PENDING' },
            take: 5,
        }),
    ]);

    const context = {
        recentAnomalies,
        recentIncidents,
        pendingRecommendations: pendingRecs,
        organizationId: req.user!.organizationId,
    };

    // Call ML engine for response
    let assistantMessage: string;

    try {
        const response = await axios.post(`${ML_ENGINE_URL}/api/chat`, {
            message,
            context,
            sessionId: session,
        });
        assistantMessage = response.data.response;
    } catch (error) {
        // Fallback to mock response if ML engine is unavailable
        assistantMessage = generateMockResponse(message, context);
    }

    // Save assistant message
    await prisma.chatMessage.create({
        data: {
            sessionId: session,
            role: 'ASSISTANT',
            content: assistantMessage,
        },
    });

    res.json({
        success: true,
        data: {
            sessionId: session,
            message: assistantMessage,
        },
    });
}));

// Get chat history
router.get('/history', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { sessionId, limit = 50 } = req.query;

    if (!sessionId) {
        throw new AppError('Session ID is required', 400);
    }

    const messages = await prisma.chatMessage.findMany({
        where: { sessionId: sessionId as string },
        orderBy: { createdAt: 'asc' },
        take: Number(limit),
    });

    res.json({
        success: true,
        data: messages,
    });
}));

// Explain an anomaly or incident
router.post('/explain', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { entityType, entityId } = req.body;

    if (!entityType || !entityId) {
        throw new AppError('Entity type and ID are required', 400);
    }

    let entity: any;
    let context: any;

    if (entityType === 'anomaly') {
        entity = await prisma.anomaly.findUnique({ where: { id: entityId } });
        context = { anomaly: entity };
    } else if (entityType === 'incident') {
        entity = await prisma.incident.findUnique({
            where: { id: entityId },
            include: { anomalies: true },
        });
        context = { incident: entity };
    } else {
        throw new AppError('Invalid entity type', 400);
    }

    if (!entity) {
        throw new AppError('Entity not found', 404);
    }

    // Call ML engine for explanation
    let explanation: string;

    try {
        const response = await axios.post(`${ML_ENGINE_URL}/api/explain`, {
            entityType,
            entity,
            context,
        });
        explanation = response.data.explanation;
    } catch (error) {
        // Fallback mock explanation
        explanation = generateMockExplanation(entityType, entity);
    }

    res.json({
        success: true,
        data: { explanation },
    });
}));

// Mock response generator (fallback when ML engine is unavailable)
function generateMockResponse(message: string, context: any): string {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('status') || lowerMessage.includes('overview')) {
        return `📊 **Current Operational Status**

Based on my analysis:
- **${context.recentAnomalies.length}** anomalies detected recently
- **${context.recentIncidents.length}** incidents in the last 24 hours
- **${context.pendingRecommendations.length}** pending optimizations

Would you like me to elaborate on any specific area?`;
    }

    if (lowerMessage.includes('anomal') || lowerMessage.includes('issue')) {
        if (context.recentAnomalies.length === 0) {
            return `✅ No significant anomalies detected in your operations. Systems are running within normal parameters.`;
        }
        const anomaly = context.recentAnomalies[0];
        return `🔍 **Latest Anomaly Detected**

**Type:** ${anomaly.anomalyType.replace('_', ' ')}
**Source:** ${anomaly.source}
**Severity:** ${anomaly.severity}
**Description:** ${anomaly.description}

The deviation from expected value is ${Math.abs(anomaly.deviation).toFixed(1)}%. I recommend reviewing this area for potential optimization.`;
    }

    if (lowerMessage.includes('recommend') || lowerMessage.includes('suggest') || lowerMessage.includes('optimize')) {
        if (context.pendingRecommendations.length === 0) {
            return `✨ No pending recommendations at the moment. Your operations are optimized!`;
        }
        const rec = context.pendingRecommendations[0];
        return `💡 **Top Recommendation**

**${rec.title}**
${rec.description}

**Estimated Impact:** ₹${rec.estimatedImpact.toLocaleString()}
**Priority:** ${rec.priority}
**Confidence:** ${(rec.confidence * 100).toFixed(0)}%

Would you like me to execute this recommendation?`;
    }

    if (lowerMessage.includes('loss') || lowerMessage.includes('cost') || lowerMessage.includes('money')) {
        const totalLoss = context.recentIncidents.reduce((sum: number, i: any) => sum + i.estimatedLoss, 0);
        return `💰 **Loss Analysis**

In the recent period, I've identified an estimated loss of **₹${totalLoss.toLocaleString()}** across ${context.recentIncidents.length} incidents.

Main contributors:
${context.recentIncidents.slice(0, 3).map((i: any, idx: number) =>
            `${idx + 1}. ${i.title} - ₹${i.estimatedLoss.toLocaleString()}`
        ).join('\n')}

I can help you prioritize which areas to focus on first.`;
    }

    return `🧠 I'm AOIA, your Autonomous Operational Intelligence Agent. I can help you with:

• **Anomaly Detection** - "What anomalies were detected today?"
• **Loss Analysis** - "How much money are we losing?"
• **Recommendations** - "What optimizations do you suggest?"
• **Status Overview** - "Give me a status update"

What would you like to know?`;
}

// Mock explanation generator
function generateMockExplanation(entityType: string, entity: any): string {
    if (entityType === 'anomaly') {
        return `## Root Cause Analysis

**Anomaly:** ${entity.anomalyType.replace('_', ' ')}
**Source:** ${entity.source}

### Analysis

The detected anomaly shows a deviation of ${Math.abs(entity.deviation).toFixed(1)}% from the expected baseline.

### Potential Causes
1. **Operational Variance** - Normal fluctuation during peak hours
2. **Resource Constraint** - Possible overload condition
3. **Process Change** - Recent modifications to workflow

### Recommended Actions
- Monitor for recurrence in the next 2 hours
- Review logs from ${entity.source}
- Consider workload rebalancing if pattern persists`;
    }

    return `## Incident Analysis

**Incident:** ${entity.title}
**Status:** ${entity.status}
**Estimated Loss:** ₹${entity.estimatedLoss?.toLocaleString() || 'N/A'}

### Summary
This incident represents a significant operational deviation that requires attention.

### Impact Assessment
The estimated financial impact is based on reduced throughput and increased idle time during the incident period.

### Resolution Path
1. Immediate: Acknowledge and investigate
2. Short-term: Implement recommended optimizations
3. Long-term: Review and update operational protocols`;
}

export default router;
