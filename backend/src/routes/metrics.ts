import { Router } from 'express';
import prisma from '../lib/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

// Get live metrics
router.get('/live', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { source, type, limit = 100 } = req.query;

    const metrics = await prisma.metric.findMany({
        where: {
            organizationId: req.user!.organizationId,
            ...(source && { source: source as string }),
            ...(type && { metricType: type as any }),
        },
        orderBy: { timestamp: 'desc' },
        take: Number(limit),
    });

    // Calculate summary stats
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);

    const recentMetrics = await prisma.metric.findMany({
        where: {
            organizationId: req.user!.organizationId,
            timestamp: { gte: oneHourAgo },
        },
    });

    const utilizationMetrics = recentMetrics.filter(m => m.metricType === 'UTILIZATION');
    const avgUtilization = utilizationMetrics.length > 0
        ? utilizationMetrics.reduce((sum, m) => sum + m.value, 0) / utilizationMetrics.length
        : 0;

    const throughputMetrics = recentMetrics.filter(m => m.metricType === 'THROUGHPUT');
    const avgThroughput = throughputMetrics.length > 0
        ? throughputMetrics.reduce((sum, m) => sum + m.value, 0) / throughputMetrics.length
        : 0;

    res.json({
        success: true,
        data: {
            metrics,
            summary: {
                avgUtilization: Math.round(avgUtilization * 100) / 100,
                avgThroughput: Math.round(avgThroughput * 100) / 100,
                totalDataPoints: recentMetrics.length,
                timeRange: '1h',
            },
        },
    });
}));

// Get metrics by time range
router.get('/range', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { start, end, type, groupBy = 'hour' } = req.query;

    const startDate = start ? new Date(start as string) : new Date(Date.now() - 24 * 60 * 60 * 1000);
    const endDate = end ? new Date(end as string) : new Date();

    const metrics = await prisma.metric.findMany({
        where: {
            organizationId: req.user!.organizationId,
            timestamp: {
                gte: startDate,
                lte: endDate,
            },
            ...(type && { metricType: type as any }),
        },
        orderBy: { timestamp: 'asc' },
    });

    // Group metrics by time period
    const grouped = metrics.reduce((acc, metric) => {
        const date = new Date(metric.timestamp);
        let key: string;

        if (groupBy === 'hour') {
            key = `${date.toISOString().slice(0, 13)}:00:00`;
        } else if (groupBy === 'day') {
            key = date.toISOString().slice(0, 10);
        } else {
            key = date.toISOString();
        }

        if (!acc[key]) {
            acc[key] = { timestamp: key, values: [], count: 0 };
        }
        acc[key].values.push(metric.value);
        acc[key].count++;

        return acc;
    }, {} as Record<string, { timestamp: string; values: number[]; count: number }>);

    const aggregated = Object.values(grouped).map(g => ({
        timestamp: g.timestamp,
        avg: g.values.reduce((a, b) => a + b, 0) / g.values.length,
        min: Math.min(...g.values),
        max: Math.max(...g.values),
        count: g.count,
    }));

    res.json({
        success: true,
        data: aggregated,
    });
}));

// Get sources (machines, agents, shifts, etc.)
router.get('/sources', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const sources = await prisma.metric.groupBy({
        by: ['source'],
        where: { organizationId: req.user!.organizationId },
        _count: true,
    });

    res.json({
        success: true,
        data: sources.map(s => ({
            name: s.source,
            dataPoints: s._count,
        })),
    });
}));

export default router;
