import { Router } from 'express';
import prisma from '../lib/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

// Get all anomalies
router.get('/', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { status, severity, type, limit = 50 } = req.query;

    const anomalies = await prisma.anomaly.findMany({
        where: {
            organizationId: req.user!.organizationId,
            ...(status && { status: status as any }),
            ...(severity && { severity: severity as any }),
            ...(type && { anomalyType: type as any }),
        },
        orderBy: { timestamp: 'desc' },
        take: Number(limit),
        include: {
            incident: {
                select: { id: true, title: true, status: true },
            },
        },
    });

    res.json({
        success: true,
        data: anomalies,
    });
}));

// Get anomaly statistics
router.get('/stats', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const now = new Date();
    const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const last7d = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const [total, last24hCount, last7dCount, bySeverity, byType, openCount] = await Promise.all([
        prisma.anomaly.count({ where: { organizationId: req.user!.organizationId } }),
        prisma.anomaly.count({
            where: {
                organizationId: req.user!.organizationId,
                timestamp: { gte: last24h },
            },
        }),
        prisma.anomaly.count({
            where: {
                organizationId: req.user!.organizationId,
                timestamp: { gte: last7d },
            },
        }),
        prisma.anomaly.groupBy({
            by: ['severity'],
            where: { organizationId: req.user!.organizationId },
            _count: true,
        }),
        prisma.anomaly.groupBy({
            by: ['anomalyType'],
            where: { organizationId: req.user!.organizationId },
            _count: true,
        }),
        prisma.anomaly.count({
            where: {
                organizationId: req.user!.organizationId,
                status: 'OPEN',
            },
        }),
    ]);

    res.json({
        success: true,
        data: {
            total,
            last24h: last24hCount,
            last7d: last7dCount,
            open: openCount,
            bySeverity: bySeverity.reduce((acc, s) => ({ ...acc, [s.severity]: s._count }), {}),
            byType: byType.reduce((acc, t) => ({ ...acc, [t.anomalyType]: t._count }), {}),
        },
    });
}));

// Update anomaly status
router.patch('/:id/status', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;
    const { status } = req.body;

    const anomaly = await prisma.anomaly.update({
        where: { id },
        data: { status },
    });

    // Audit log
    await prisma.auditLog.create({
        data: {
            userId: req.user!.id,
            action: 'UPDATE_ANOMALY_STATUS',
            entity: 'Anomaly',
            entityId: id,
            details: { newStatus: status },
        },
    });

    res.json({
        success: true,
        data: anomaly,
    });
}));

export default router;
