import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
    console.log('🌱 Seeding database...\n');

    // Create demo organization
    const hashedPassword = await bcrypt.hash('demo123456', 12);

    const organization = await prisma.organization.upsert({
        where: { id: 'demo-org-001' },
        update: {},
        create: {
            id: 'demo-org-001',
            name: 'Acme Manufacturing Co.',
            industry: 'MANUFACTURING',
            costPerMinute: 75, // ₹75 per minute of operation
        },
    });

    console.log(`✅ Created organization: ${organization.name}`);

    // Create demo users
    const adminUser = await prisma.user.upsert({
        where: { email: 'admin@acme.com' },
        update: {},
        create: {
            email: 'admin@acme.com',
            password: hashedPassword,
            name: 'John Admin',
            role: 'ADMIN',
            organizationId: organization.id,
        },
    });

    const managerUser = await prisma.user.upsert({
        where: { email: 'manager@acme.com' },
        update: {},
        create: {
            email: 'manager@acme.com',
            password: hashedPassword,
            name: 'Sarah Manager',
            role: 'MANAGER',
            organizationId: organization.id,
        },
    });

    console.log(`✅ Created users: ${adminUser.email}, ${managerUser.email}`);
    console.log(`   Password for all demo users: demo123456\n`);

    // Generate metrics for the last 7 days
    const now = new Date();
    const metrics = [];
    const sources = ['machine-1', 'machine-2', 'machine-3', 'shift-a', 'shift-b', 'shift-c', 'agent-101', 'agent-102'];
    const metricTypes = ['UTILIZATION', 'THROUGHPUT', 'IDLE_TIME', 'RESPONSE_TIME', 'QUALITY_SCORE'] as const;

    for (let dayOffset = 6; dayOffset >= 0; dayOffset--) {
        for (let hour = 0; hour < 24; hour++) {
            for (const source of sources) {
                for (const metricType of metricTypes) {
                    const timestamp = new Date(now.getTime() - dayOffset * 24 * 60 * 60 * 1000);
                    timestamp.setHours(hour, Math.floor(Math.random() * 60), 0, 0);

                    let value: number;
                    switch (metricType) {
                        case 'UTILIZATION':
                            value = 60 + Math.random() * 35; // 60-95%
                            break;
                        case 'THROUGHPUT':
                            value = 80 + Math.random() * 40; // 80-120 units
                            break;
                        case 'IDLE_TIME':
                            value = Math.random() * 15; // 0-15 minutes
                            break;
                        case 'RESPONSE_TIME':
                            value = 100 + Math.random() * 200; // 100-300ms
                            break;
                        case 'QUALITY_SCORE':
                            value = 85 + Math.random() * 14; // 85-99%
                            break;
                        default:
                            value = Math.random() * 100;
                    }

                    metrics.push({
                        organizationId: organization.id,
                        timestamp,
                        metricType,
                        value: Math.round(value * 100) / 100,
                        unit: metricType === 'RESPONSE_TIME' ? 'ms' : metricType === 'IDLE_TIME' ? 'min' : '%',
                        source,
                    });
                }
            }
        }
    }

    // Insert metrics in batches
    const batchSize = 500;
    for (let i = 0; i < metrics.length; i += batchSize) {
        const batch = metrics.slice(i, i + batchSize);
        await prisma.metric.createMany({ data: batch });
    }
    console.log(`✅ Created ${metrics.length} metrics\n`);

    // Create anomalies
    const anomalyTypes = [
        { type: 'IDLE_SPIKE', desc: 'Unusual idle time detected', severity: 'MEDIUM' },
        { type: 'THROUGHPUT_DROP', desc: 'Significant drop in throughput', severity: 'HIGH' },
        { type: 'MACHINE_SLOWDOWN', desc: 'Machine operating below optimal speed', severity: 'MEDIUM' },
        { type: 'OVERLOAD', desc: 'Resource overload detected', severity: 'HIGH' },
        { type: 'QUALITY_DECLINE', desc: 'Quality metrics below threshold', severity: 'CRITICAL' },
        { type: 'PATTERN_BREAK', desc: 'Unusual operational pattern detected', severity: 'LOW' },
    ] as const;

    const anomalies = [];
    for (let i = 0; i < 25; i++) {
        const anomalyInfo = anomalyTypes[Math.floor(Math.random() * anomalyTypes.length)];
        const source = sources[Math.floor(Math.random() * sources.length)];
        const daysAgo = Math.floor(Math.random() * 7);
        const timestamp = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);

        const expectedValue = 80 + Math.random() * 15;
        const actualValue = expectedValue * (0.6 + Math.random() * 0.3);
        const deviation = ((actualValue - expectedValue) / expectedValue) * 100;

        anomalies.push({
            organizationId: organization.id,
            timestamp,
            anomalyType: anomalyInfo.type,
            severity: anomalyInfo.severity,
            source,
            description: `${anomalyInfo.desc} on ${source}`,
            value: Math.round(actualValue * 100) / 100,
            expectedValue: Math.round(expectedValue * 100) / 100,
            deviation: Math.round(deviation * 100) / 100,
            status: i < 10 ? 'OPEN' : i < 18 ? 'ACKNOWLEDGED' : 'RESOLVED',
        });
    }

    await prisma.anomaly.createMany({ data: anomalies as any });
    console.log(`✅ Created ${anomalies.length} anomalies\n`);

    // Create incidents
    const incidentData = [
        {
            title: 'Machine 1 Throughput Drop',
            description: 'Production line 1 experienced a 25% drop in throughput during morning shift',
            estimatedLoss: 45000,
            status: 'ACTIVE',
            rootCause: null,
        },
        {
            title: 'Shift B Idle Time Spike',
            description: 'Abnormal idle time pattern detected during Shift B operations',
            estimatedLoss: 28000,
            status: 'INVESTIGATING',
            rootCause: 'Initial analysis suggests workflow bottleneck at station 3',
        },
        {
            title: 'Quality Control Alert',
            description: 'Quality scores dropped below 90% threshold on multiple machines',
            estimatedLoss: 62000,
            status: 'MITIGATING',
            rootCause: 'Calibration drift detected on inspection sensors',
        },
        {
            title: 'Morning Shift Overload',
            description: 'Resource overload led to cascading delays across production floor',
            estimatedLoss: 35000,
            status: 'RESOLVED',
            rootCause: 'Insufficient staffing during peak hours',
            resolution: 'Adjusted shift scheduling and added buffer capacity',
        },
        {
            title: 'Machine 3 Micro-Downtime',
            description: 'Frequent micro-stoppages detected on Machine 3',
            estimatedLoss: 18500,
            status: 'RESOLVED',
            rootCause: 'Worn belt causing intermittent slippage',
            resolution: 'Replaced belt and scheduled preventive maintenance',
        },
    ];

    for (let i = 0; i < incidentData.length; i++) {
        const incident = incidentData[i];
        const daysAgo = i;
        const startTime = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);
        const endTime = incident.status === 'RESOLVED'
            ? new Date(startTime.getTime() + (2 + Math.random() * 4) * 60 * 60 * 1000)
            : null;

        await prisma.incident.create({
            data: {
                organizationId: organization.id,
                title: incident.title,
                description: incident.description,
                startTime,
                endTime,
                status: incident.status as any,
                estimatedLoss: incident.estimatedLoss,
                actualLoss: endTime ? incident.estimatedLoss * (0.8 + Math.random() * 0.3) : null,
                rootCause: incident.rootCause,
                resolution: incident.resolution || null,
            },
        });
    }
    console.log(`✅ Created ${incidentData.length} incidents\n`);

    // Create recommendations
    const recommendationData = [
        {
            title: 'Rebalance Shift B Workload',
            description: 'Redistribute tasks from overloaded stations to underutilized ones to reduce idle time by approximately 15%',
            actionType: 'REBALANCE_WORKLOAD',
            priority: 'HIGH',
            estimatedImpact: 32000,
            confidence: 0.89,
            reasoning: 'Analysis shows Station 3 is a bottleneck with 40% higher queue times. Redistributing 2 tasks to Station 4 would optimize flow.',
        },
        {
            title: 'Schedule Preventive Maintenance - Machine 2',
            description: 'Predictive model indicates Machine 2 is likely to experience issues within 48 hours based on vibration patterns',
            actionType: 'SCHEDULE_MAINTENANCE',
            priority: 'URGENT',
            estimatedImpact: 55000,
            confidence: 0.94,
            reasoning: 'Vibration signature matches pre-failure pattern with 94% confidence. Preventive maintenance cost: ₹12,000 vs potential downtime loss: ₹55,000.',
        },
        {
            title: 'Adjust Task Routing Algorithm',
            description: 'Modify routing logic to prioritize high-value orders during peak hours',
            actionType: 'ADJUST_ROUTING',
            priority: 'MEDIUM',
            estimatedImpact: 28000,
            confidence: 0.82,
            reasoning: 'Current FIFO routing causes high-value orders to wait. Priority routing would increase daily revenue by ~8%.',
        },
        {
            title: 'Training Required - Agent 101',
            description: 'Agent 101 performance metrics suggest additional training would improve efficiency',
            actionType: 'TRAINING_NEEDED',
            priority: 'LOW',
            estimatedImpact: 15000,
            confidence: 0.76,
            reasoning: 'Response times are 25% above average. Similar agents showed 30% improvement post-training.',
        },
        {
            title: 'Allocate Additional Resources to Line 2',
            description: 'Demand forecast predicts 40% spike next week. Add temporary resources now.',
            actionType: 'RESOURCE_ALLOCATION',
            priority: 'HIGH',
            estimatedImpact: 45000,
            confidence: 0.88,
            reasoning: 'Historical data and current orders indicate capacity constraints. Proactive allocation prevents ₹45,000 in overtime and delays.',
        },
    ];

    for (const rec of recommendationData) {
        await prisma.recommendation.create({
            data: {
                organizationId: organization.id,
                title: rec.title,
                description: rec.description,
                actionType: rec.actionType as any,
                priority: rec.priority as any,
                status: 'PENDING',
                estimatedImpact: rec.estimatedImpact,
                confidence: rec.confidence,
                reasoning: rec.reasoning,
            },
        });
    }
    console.log(`✅ Created ${recommendationData.length} recommendations\n`);

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 Database seeding completed!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('\n📧 Demo Login Credentials:');
    console.log('   Email: admin@acme.com');
    console.log('   Password: demo123456');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

main()
    .catch((e) => {
        console.error('Error seeding database:', e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
