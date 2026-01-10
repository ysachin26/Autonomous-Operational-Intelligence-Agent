import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { createServer } from 'http';
import { Server } from 'socket.io';
import dotenv from 'dotenv';

import authRoutes from './routes/auth';
import metricsRoutes from './routes/metrics';
import anomalyRoutes from './routes/anomaly';
import incidentRoutes from './routes/incidents';
import recommendationRoutes from './routes/recommendations';
import dashboardRoutes from './routes/dashboard';
import chatRoutes from './routes/chat';
import { errorHandler } from './middleware/errorHandler';
import { setupSocketHandlers } from './socket';

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
    },
});

// Middleware
app.use(helmet());
app.use(cors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
    credentials: true,
}));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Make io accessible in routes
app.set('io', io);

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/metrics', metricsRoutes);
app.use('/api/anomaly', anomalyRoutes);
app.use('/api/incidents', incidentRoutes);
app.use('/api/recommendations', recommendationRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/chat', chatRoutes);

// Error handling
app.use(errorHandler);

// Socket.IO setup
setupSocketHandlers(io);

const PORT = process.env.BACKEND_PORT || 3001;

httpServer.listen(PORT, () => {
    console.log(`
  ╔═══════════════════════════════════════════════════════════╗
  ║                                                           ║
  ║     🧠 AOIA Backend Server                                ║
  ║     Autonomous Operational Intelligence Agent             ║
  ║                                                           ║
  ║     Server running on http://localhost:${PORT}              ║
  ║     WebSocket enabled                                     ║
  ║                                                           ║
  ╚═══════════════════════════════════════════════════════════╝
  `);
});

export { app, io };
