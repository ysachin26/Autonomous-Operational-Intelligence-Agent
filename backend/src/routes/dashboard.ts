import { Router } from 'express';
import prisma from '../lib/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

// Get dashboard data
router.get('/', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const now = new Date();
    const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const last7d = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const lastMonth = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

    // Parallel queries for performance
    const [
        organization,
        activeIncidents,
        openAnomalies,
        pendingRecommendations,
        last24hLoss,
        last7dLoss,
        monthlyLoss,
        completedRecommendations,
        recentAnomalies,
        recentIncidents,
    ] = await Promise.all([
        // Organization details
        prisma.organization.findUnique({
            where: { id: req.user!.organizationId },
        }),

        // Active incidents count
        prisma.incident.count({
            where: {
                organizationId: req.user!.organizationId,
                status: { in: ['ACTIVE', 'INVESTIGATING', 'MITIGATING'] },
            },
        }),

        // Open anomalies count
        prisma.anomaly.count({
            where: {
                organizationId: req.user!.organizationId,
                status: 'OPEN',
            },
        }),

        // Pending recommendations count
        prisma.recommendation.count({
            where: {
                organizationId: req.user!.organizationId,
                status: 'PENDING',
            },
        }),

        // Loss in last 24h
        prisma.incident.aggregate({
            where: {
                organizationId: req.user!.organizationId,
                startTime: { gte: last24h },
            },
            _sum: { estimatedLoss: true },
        }),

        // Loss in last 7 days
        prisma.incident.aggregate({
            where: {
                organizationId: req.user!.organizationId,
                startTime: { gte: last7d },
            },
            _sum: { estimatedLoss: true },
        }),

        // Monthly loss trend
        prisma.incident.findMany({
            where: {
                organizationId: req.user!.organizationId,
                startTime: { gte: lastMonth },
            },
            select: { startTime: true, estimatedLoss: true },
        }),

        // Completed recommendations with impact
        prisma.recommendation.aggregate({
            where: {
                organizationId: req.user!.organizationId,
                status: 'COMPLETED',
                createdAt: { gte: lastMonth },
            },
            _sum: { actualImpact: true },
            _count: true,
        }),

        // Recent anomalies
        prisma.anomaly.findMany({
            where: { organizationId: req.user!.organizationId },
            orderBy: { timestamp: 'desc' },
            take: 5,
        }),

        // Recent incidents
        prisma.incident.findMany({
            where: { organizationId: req.user!.organizationId },
            orderBy: { startTime: 'desc' },
            take: 5,
        }),
    ]);

    // Calculate daily loss trend
    const lossPerDay = monthlyLoss.reduce((acc, incident) => {
        const day = incident.startTime.toISOString().slice(0, 10);
        acc[day] = (acc[day] || 0) + incident.estimatedLoss;
        return acc;
    }, {} as Record<string, number>);

    // Fill in missing days with 0
    const lossTrend = [];
    for (let i = 29; i >= 0; i--) {
        const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
        const dateStr = date.toISOString().slice(0, 10);
        lossTrend.push({
            date: dateStr,
            loss: Math.round(lossPerDay[dateStr] || 0),
        });
    }

    // Calculate efficiency score (simulated)
    const baseEfficiency = 85;
    const efficiencyPenalty = Math.min(15, activeIncidents * 2 + openAnomalies * 0.5);
    const efficiencyBonus = Math.min(10, completedRecommendations._count * 0.5);
    const efficiencyScore = Math.round(baseEfficiency - efficiencyPenalty + efficiencyBonus);

    res.json({
        success: true,
        data: {
            organization: {
                name: organization?.name,
                industry: organization?.industry,
            },
            kpis: {
                activeIncidents,
                openAnomalies,
                pendingRecommendations,
                efficiencyScore: Math.max(0, Math.min(100, efficiencyScore)),
            },
            loss: {
                last24h: Math.round(last24hLoss._sum.estimatedLoss || 0),
                last7d: Math.round(last7dLoss._sum.estimatedLoss || 0),
                trend: lossTrend,
            },
            savings: {
                total: Math.round(completedRecommendations._sum.actualImpact || 0),
                actionsCompleted: completedRecommendations._count,
            },
            recentAnomalies,
            recentIncidents,
        },
    });
}));

// Get shift-wise performance
router.get('/shifts', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const now = new Date();
    const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000);

    const metrics = await prisma.metric.findMany({
        where: {
            organizationId: req.user!.organizationId,
            timestamp: { gte: last24h },
            source: { startsWith: 'shift' },
        },
    });

    // Group by shift
    const shiftData = metrics.reduce((acc, metric) => {
        if (!acc[metric.source]) {
            acc[metric.source] = {
                source: metric.source,
                utilization: [],
                throughput: [],
                idleTime: [],
            };
        }

        if (metric.metricType === 'UTILIZATION') {
            acc[metric.source].utilization.push(metric.value);
        } else if (metric.metricType === 'THROUGHPUT') {
            acc[metric.source].throughput.push(metric.value);
        } else if (metric.metricType === 'IDLE_TIME') {
            acc[metric.source].idleTime.push(metric.value);
        }

        return acc;
    }, {} as Record<string, any>);

    const shifts = Object.values(shiftData).map((shift: any) => ({
        name: shift.source,
        avgUtilization: shift.utilization.length > 0
            ? Math.round(shift.utilization.reduce((a: number, b: number) => a + b, 0) / shift.utilization.length)
            : 0,
        avgThroughput: shift.throughput.length > 0
            ? Math.round(shift.throughput.reduce((a: number, b: number) => a + b, 0) / shift.throughput.length)
            : 0,
        avgIdleTime: shift.idleTime.length > 0
            ? Math.round(shift.idleTime.reduce((a: number, b: number) => a + b, 0) / shift.idleTime.length)
            : 0,
    }));

    res.json({
        success: true,
        data: shifts,
    });
}));

// Get heatmap data
router.get('/heatmap', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const now = new Date();
    const last7d = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const anomalies = await prisma.anomaly.findMany({
        where: {
            organizationId: req.user!.organizationId,
            timestamp: { gte: last7d },
        },
        select: {
            source: true,
            anomalyType: true,
            severity: true,
            timestamp: true,
        },
    });

    // Group by source and day
    const heatmapData: Record<string, Record<string, number>> = {};

    anomalies.forEach(anomaly => {
        const day = anomaly.timestamp.toISOString().slice(0, 10);
        const source = anomaly.source;

        if (!heatmapData[source]) {
            heatmapData[source] = {};
        }

        const severityWeight = {
            LOW: 1,
            MEDIUM: 2,
            HIGH: 3,
            CRITICAL: 5,
        };

        heatmapData[source][day] = (heatmapData[source][day] || 0) +
            (severityWeight[anomaly.severity] || 1);
    });

    // Convert to array format
    const heatmap = Object.entries(heatmapData).map(([source, days]) => ({
        source,
        data: Object.entries(days).map(([date, intensity]) => ({
            date,
            intensity: Math.min(10, intensity), // Cap at 10
        })),
    }));

    res.json({
        success: true,
        data: heatmap,
    });
}));

export default router;
