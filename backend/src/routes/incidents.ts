import { Router } from 'express';
import prisma from '../lib/prisma';
import { asyncHandler } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

// Get all incidents
router.get('/', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { status, limit = 50 } = req.query;

    const incidents = await prisma.incident.findMany({
        where: {
            organizationId: req.user!.organizationId,
            ...(status && { status: status as any }),
        },
        orderBy: { startTime: 'desc' },
        take: Number(limit),
        include: {
            anomalies: {
                select: { id: true, anomalyType: true, severity: true },
            },
            recommendations: {
                select: { id: true, title: true, status: true, priority: true },
            },
        },
    });

    res.json({
        success: true,
        data: incidents,
    });
}));

// Get incident by ID
router.get('/:id', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;

    const incident = await prisma.incident.findUnique({
        where: { id },
        include: {
            anomalies: true,
            recommendations: true,
        },
    });

    res.json({
        success: true,
        data: incident,
    });
}));

// Get loss summary
router.get('/loss/summary', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { period = '7d' } = req.query;

    const now = new Date();
    let startDate: Date;

    switch (period) {
        case '24h':
            startDate = new Date(now.getTime() - 24 * 60 * 60 * 1000);
            break;
        case '7d':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            break;
        case '30d':
            startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
            break;
        default:
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    }

    const incidents = await prisma.incident.findMany({
        where: {
            organizationId: req.user!.organizationId,
            startTime: { gte: startDate },
        },
    });

    const totalLoss = incidents.reduce((sum, i) => sum + i.estimatedLoss, 0);
    const resolvedLoss = incidents
        .filter(i => i.status === 'RESOLVED' || i.status === 'CLOSED')
        .reduce((sum, i) => sum + i.estimatedLoss, 0);
    const activeLoss = incidents
        .filter(i => i.status === 'ACTIVE' || i.status === 'INVESTIGATING')
        .reduce((sum, i) => sum + i.estimatedLoss, 0);

    // Group by day
    const lossPerDay = incidents.reduce((acc, incident) => {
        const day = incident.startTime.toISOString().slice(0, 10);
        acc[day] = (acc[day] || 0) + incident.estimatedLoss;
        return acc;
    }, {} as Record<string, number>);

    res.json({
        success: true,
        data: {
            totalLoss: Math.round(totalLoss),
            resolvedLoss: Math.round(resolvedLoss),
            activeLoss: Math.round(activeLoss),
            incidentCount: incidents.length,
            period,
            trend: Object.entries(lossPerDay).map(([date, loss]) => ({ date, loss })),
        },
    });
}));

// Update incident
router.patch('/:id', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;
    const { status, rootCause, resolution } = req.body;

    const incident = await prisma.incident.update({
        where: { id },
        data: {
            ...(status && { status }),
            ...(rootCause && { rootCause }),
            ...(resolution && { resolution }),
            ...(status === 'RESOLVED' && { endTime: new Date() }),
        },
    });

    // Audit log
    await prisma.auditLog.create({
        data: {
            userId: req.user!.id,
            action: 'UPDATE_INCIDENT',
            entity: 'Incident',
            entityId: id,
            details: { status, rootCause, resolution },
        },
    });

    res.json({
        success: true,
        data: incident,
    });
}));

export default router;
