import { Server, Socket } from 'socket.io';

export function setupSocketHandlers(io: Server) {
    io.on('connection', (socket: Socket) => {
        console.log(`Client connected: ${socket.id}`);

        // Join organization room for targeted broadcasts
        socket.on('join:organization', (organizationId: string) => {
            socket.join(`org:${organizationId}`);
            console.log(`Socket ${socket.id} joined organization: ${organizationId}`);
        });

        // Handle real-time metric updates
        socket.on('metric:update', (data) => {
            const { organizationId, ...metric } = data;
            io.to(`org:${organizationId}`).emit('metric:new', metric);
        });

        // Handle anomaly alerts
        socket.on('anomaly:detected', (data) => {
            const { organizationId, ...anomaly } = data;
            io.to(`org:${organizationId}`).emit('anomaly:new', anomaly);
        });

        // Handle recommendation updates
        socket.on('recommendation:created', (data) => {
            const { organizationId, ...recommendation } = data;
            io.to(`org:${organizationId}`).emit('recommendation:new', recommendation);
        });

        socket.on('disconnect', () => {
            console.log(`Client disconnected: ${socket.id}`);
        });
    });

    // Emit simulated real-time data (for demo purposes)
    setInterval(() => {
        const simulatedMetric = {
            type: 'UTILIZATION',
            value: 70 + Math.random() * 25,
            source: `machine-${Math.floor(Math.random() * 5) + 1}`,
            timestamp: new Date().toISOString(),
        };
        io.emit('metric:live', simulatedMetric);
    }, 5000);
}
