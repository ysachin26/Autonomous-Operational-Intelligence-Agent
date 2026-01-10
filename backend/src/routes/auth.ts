import { Router } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import prisma from '../lib/prisma';
import { asyncHandler, AppError } from '../middleware/errorHandler';
import { authenticate, AuthRequest } from '../middleware/auth';

const router = Router();

const registerSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
    name: z.string().min(2),
    organizationName: z.string().min(2),
    industry: z.enum(['BPO', 'MANUFACTURING', 'LOGISTICS', 'RETAIL', 'HEALTHCARE', 'GENERAL']).optional(),
});

const loginSchema = z.object({
    email: z.string().email(),
    password: z.string(),
});

// Register
router.post('/register', asyncHandler(async (req, res) => {
    const data = registerSchema.parse(req.body);

    const existingUser = await prisma.user.findUnique({
        where: { email: data.email },
    });

    if (existingUser) {
        throw new AppError('Email already registered', 400);
    }

    const hashedPassword = await bcrypt.hash(data.password, 12);

    // Create organization and user
    const organization = await prisma.organization.create({
        data: {
            name: data.organizationName,
            industry: data.industry || 'GENERAL',
            users: {
                create: {
                    email: data.email,
                    password: hashedPassword,
                    name: data.name,
                    role: 'ADMIN',
                },
            },
        },
        include: {
            users: true,
        },
    });

    const user = organization.users[0];
    const token = jwt.sign(
        { userId: user.id },
        process.env.JWT_SECRET || 'secret',
        { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );

    res.status(201).json({
        success: true,
        data: {
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role,
                organization: {
                    id: organization.id,
                    name: organization.name,
                },
            },
            token,
        },
    });
}));

// Login
router.post('/login', asyncHandler(async (req, res) => {
    const data = loginSchema.parse(req.body);

    const user = await prisma.user.findUnique({
        where: { email: data.email },
        include: { organization: true },
    });

    if (!user) {
        throw new AppError('Invalid credentials', 401);
    }

    const isValidPassword = await bcrypt.compare(data.password, user.password);

    if (!isValidPassword) {
        throw new AppError('Invalid credentials', 401);
    }

    const token = jwt.sign(
        { userId: user.id },
        process.env.JWT_SECRET || 'secret',
        { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );

    // Log the login
    await prisma.auditLog.create({
        data: {
            userId: user.id,
            action: 'LOGIN',
            entity: 'User',
            entityId: user.id,
            details: { ip: req.ip },
        },
    });

    res.json({
        success: true,
        data: {
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role,
                organization: {
                    id: user.organization.id,
                    name: user.organization.name,
                    industry: user.organization.industry,
                },
            },
            token,
        },
    });
}));

// Get current user
router.get('/me', authenticate, asyncHandler(async (req: AuthRequest, res) => {
    const user = await prisma.user.findUnique({
        where: { id: req.user!.id },
        include: { organization: true },
    });

    res.json({
        success: true,
        data: {
            id: user!.id,
            email: user!.email,
            name: user!.name,
            role: user!.role,
            organization: {
                id: user!.organization.id,
                name: user!.organization.name,
                industry: user!.organization.industry,
            },
        },
    });
}));

export default router;
