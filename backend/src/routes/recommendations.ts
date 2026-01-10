import { Router } from 'express';
import axios from 'axios';
import prisma from '../lib/prisma';
import { asyncHandler, AppError } from '../middleware/errorHandler';
import { authenticate, authorize, AuthRequest } from '../middleware/auth';

const router = Router();

const ML_ENGINE_URL = process.env.ML_ENGINE_URL || 'http://localhost:8000';

// Get all recommendations
router.get('/', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { status, priority, limit = 50 } = req.query;

    const recommendations = await prisma.recommendation.findMany({
        where: {
            organizationId: req.user!.organizationId,
            ...(status && { status: status as any }),
            ...(priority && { priority: priority as any }),
        },
        orderBy: [
            { priority: 'desc' },
            { createdAt: 'desc' },
        ],
        take: Number(limit),
        include: {
            incident: {
                select: { id: true, title: true },
            },
        },
    });

    res.json({
        success: true,
        data: recommendations,
    });
}));

// Get recommendation by ID
router.get('/:id', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;

    const recommendation = await prisma.recommendation.findUnique({
        where: { id },
        include: {
            incident: true,
        },
    });

    if (!recommendation) {
        throw new AppError('Recommendation not found', 404);
    }

    res.json({
        success: true,
        data: recommendation,
    });
}));

// Execute recommendation
router.post('/:id/execute', authenticate, authorize('ADMIN', 'MANAGER'), asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;

    const recommendation = await prisma.recommendation.findUnique({
        where: { id },
    });

    if (!recommendation) {
        throw new AppError('Recommendation not found', 404);
    }

    if (recommendation.status !== 'PENDING' && recommendation.status !== 'APPROVED') {
        throw new AppError('Recommendation cannot be executed in current state', 400);
    }

    // Update status to executing
    await prisma.recommendation.update({
        where: { id },
        data: { status: 'EXECUTING' },
    });

    // Call ML engine to execute the action
    try {
        const response = await axios.post(`${ML_ENGINE_URL}/api/execute`, {
            recommendationId: id,
            actionType: recommendation.actionType,
            payload: recommendation.actionPayload,
        });

        // Update as completed
        const updated = await prisma.recommendation.update({
            where: { id },
            data: {
                status: 'COMPLETED',
                executedAt: new Date(),
                executedBy: req.user!.id,
                actualImpact: response.data.actualImpact || recommendation.estimatedImpact,
            },
        });

        // Audit log
        await prisma.auditLog.create({
            data: {
                userId: req.user!.id,
                action: 'EXECUTE_RECOMMENDATION',
                entity: 'Recommendation',
                entityId: id,
                details: {
                    actionType: recommendation.actionType,
                    estimatedImpact: recommendation.estimatedImpact,
                },
            },
        });

        // Emit socket event
        const io = req.app.get('io');
        io.emit('recommendation:executed', { recommendation: updated });

        res.json({
            success: true,
            data: updated,
            message: 'Recommendation executed successfully',
        });
    } catch (error) {
        // Mark as failed
        await prisma.recommendation.update({
            where: { id },
            data: { status: 'FAILED' },
        });

        throw new AppError('Failed to execute recommendation', 500);
    }
}));

// Approve/Reject recommendation
router.patch('/:id/status', authenticate, authorize('ADMIN', 'MANAGER'), asyncHandler(async (req: AuthRequest, res) => {
    const { id } = req.params;
    const { status } = req.body;

    if (!['APPROVED', 'REJECTED'].includes(status)) {
        throw new AppError('Invalid status', 400);
    }

    const updated = await prisma.recommendation.update({
        where: { id },
        data: { status },
    });

    // Audit log
    await prisma.auditLog.create({
        data: {
            userId: req.user!.id,
            action: `${status}_RECOMMENDATION`,
            entity: 'Recommendation',
            entityId: id,
        },
    });

    res.json({
        success: true,
        data: updated,
    });
}));

// Get recommendation statistics
router.get('/stats/summary', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const [total, pending, completed, totalImpact] = await Promise.all([
        prisma.recommendation.count({ where: { organizationId: req.user!.organizationId } }),
        prisma.recommendation.count({
            where: { organizationId: req.user!.organizationId, status: 'PENDING' },
        }),
        prisma.recommendation.count({
            where: { organizationId: req.user!.organizationId, status: 'COMPLETED' },
        }),
        prisma.recommendation.aggregate({
            where: { organizationId: req.user!.organizationId, status: 'COMPLETED' },
            _sum: { actualImpact: true },
        }),
    ]);

    res.json({
        success: true,
        data: {
            total,
            pending,
            completed,
            successRate: total > 0 ? Math.round((completed / total) * 100) : 0,
            totalImpact: totalImpact._sum.actualImpact || 0,
        },
    });
}));

export default router;
