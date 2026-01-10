/**
 * AOIA Demo Data Generator
 * Generates realistic operational data for Manufacturing scenario
 */

// Machines in the factory
export const machines = [
    { id: 'M1', name: 'CNC Machine 1', type: 'CNC', location: 'Floor A', costPerHour: 2500 },
    { id: 'M2', name: 'CNC Machine 2', type: 'CNC', location: 'Floor A', costPerHour: 2500 },
    { id: 'M3', name: 'Lathe Machine 1', type: 'Lathe', location: 'Floor B', costPerHour: 1800 },
    { id: 'M4', name: 'Press Machine 1', type: 'Press', location: 'Floor B', costPerHour: 2200 },
    { id: 'M5', name: 'Assembly Line 1', type: 'Assembly', location: 'Floor C', costPerHour: 3500 },
];

// Employees/Operators
export const employees = [
    { id: 'E1', name: 'Rajesh Kumar', role: 'Senior Operator', shift: 'A', skills: ['CNC', 'Lathe'] },
    { id: 'E2', name: 'Priya Singh', role: 'Operator', shift: 'A', skills: ['CNC'] },
    { id: 'E3', name: 'Amit Patel', role: 'Senior Operator', shift: 'B', skills: ['Press', 'Assembly'] },
    { id: 'E4', name: 'Suman Devi', role: 'Operator', shift: 'B', skills: ['Assembly'] },
    { id: 'E5', name: 'Vikram Rao', role: 'Operator', shift: 'C', skills: ['CNC', 'Lathe'] },
    { id: 'E6', name: 'Neha Sharma', role: 'Junior Operator', shift: 'C', skills: ['Assembly'] },
];

// Shift definitions
export const shifts = [
    { id: 'A', name: 'Morning Shift', startTime: '06:00', endTime: '14:00', targetEfficiency: 90 },
    { id: 'B', name: 'Afternoon Shift', startTime: '14:00', endTime: '22:00', targetEfficiency: 88 },
    { id: 'C', name: 'Night Shift', startTime: '22:00', endTime: '06:00', targetEfficiency: 85 },
];

// Generate random number in range
const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randFloat = (min, max) => Math.random() * (max - min) + min;

// Generate machine events for a day
export function generateMachineEvents(date = new Date()) {
    const events = [];
    const dayStart = new Date(date);
    dayStart.setHours(0, 0, 0, 0);

    machines.forEach(machine => {
        let currentTime = new Date(dayStart);

        // Generate events for 24 hours
        while (currentTime < new Date(dayStart.getTime() + 24 * 60 * 60 * 1000)) {
            const eventType = Math.random();

            if (eventType < 0.7) {
                // Production run (70% of time)
                const duration = rand(30, 180); // 30 min to 3 hours
                const efficiency = randFloat(75, 100);
                const output = Math.floor(duration * efficiency / 100 * rand(5, 15));

                events.push({
                    id: `${machine.id}-${currentTime.getTime()}`,
                    machineId: machine.id,
                    machineName: machine.name,
                    eventType: 'PRODUCTION',
                    startTime: new Date(currentTime),
                    endTime: new Date(currentTime.getTime() + duration * 60 * 1000),
                    duration,
                    efficiency,
                    output,
                    status: 'completed',
                });

                currentTime = new Date(currentTime.getTime() + duration * 60 * 1000);
            } else if (eventType < 0.85) {
                // Idle time (15%)
                const duration = rand(5, 45);
                const reason = ['Waiting for material', 'Operator break', 'Setup change', 'Quality check'][rand(0, 3)];

                events.push({
                    id: `${machine.id}-${currentTime.getTime()}`,
                    machineId: machine.id,
                    machineName: machine.name,
                    eventType: 'IDLE',
                    startTime: new Date(currentTime),
                    endTime: new Date(currentTime.getTime() + duration * 60 * 1000),
                    duration,
                    reason,
                    lossAmount: Math.floor(duration * machine.costPerHour / 60),
                    status: 'completed',
                });

                currentTime = new Date(currentTime.getTime() + duration * 60 * 1000);
            } else if (eventType < 0.95) {
                // Micro-downtime (10%)
                const duration = rand(1, 5);

                events.push({
                    id: `${machine.id}-${currentTime.getTime()}`,
                    machineId: machine.id,
                    machineName: machine.name,
                    eventType: 'MICRO_DOWNTIME',
                    startTime: new Date(currentTime),
                    endTime: new Date(currentTime.getTime() + duration * 60 * 1000),
                    duration,
                    reason: 'Brief stoppage',
                    lossAmount: Math.floor(duration * machine.costPerHour / 60),
                    hidden: true, // Hidden inefficiency
                    status: 'completed',
                });

                currentTime = new Date(currentTime.getTime() + duration * 60 * 1000);
            } else {
                // Breakdown (5%)
                const duration = rand(15, 120);

                events.push({
                    id: `${machine.id}-${currentTime.getTime()}`,
                    machineId: machine.id,
                    machineName: machine.name,
                    eventType: 'BREAKDOWN',
                    startTime: new Date(currentTime),
                    endTime: new Date(currentTime.getTime() + duration * 60 * 1000),
                    duration,
                    reason: ['Mechanical failure', 'Electrical issue', 'Sensor malfunction', 'Overheating'][rand(0, 3)],
                    lossAmount: Math.floor(duration * machine.costPerHour / 60),
                    severity: duration > 60 ? 'HIGH' : duration > 30 ? 'MEDIUM' : 'LOW',
                    status: 'completed',
                });

                currentTime = new Date(currentTime.getTime() + duration * 60 * 1000);
            }
        }
    });

    return events.sort((a, b) => a.startTime - b.startTime);
}

// Generate shift performance data
export function generateShiftPerformance(date = new Date()) {
    return shifts.map(shift => {
        const efficiency = randFloat(65, 95);
        const targetOutput = rand(800, 1200);
        const actualOutput = Math.floor(targetOutput * efficiency / 100);
        const lossAmount = Math.floor((targetOutput - actualOutput) * rand(50, 100));

        return {
            shiftId: shift.id,
            shiftName: shift.name,
            date: date.toISOString().split('T')[0],
            targetEfficiency: shift.targetEfficiency,
            actualEfficiency: Math.round(efficiency * 10) / 10,
            targetOutput,
            actualOutput,
            lossAmount,
            status: efficiency >= shift.targetEfficiency ? 'ON_TARGET' : efficiency >= shift.targetEfficiency - 10 ? 'BELOW_TARGET' : 'CRITICAL',
            operators: employees.filter(e => e.shift === shift.id).length,
        };
    });
}

// Generate anomalies/inefficiencies
export function generateAnomalies(events) {
    const anomalies = [];

    // Find patterns in events
    const idleEvents = events.filter(e => e.eventType === 'IDLE');
    const downtimeEvents = events.filter(e => e.eventType === 'BREAKDOWN' || e.eventType === 'MICRO_DOWNTIME');

    // Cluster idle times
    if (idleEvents.length > 3) {
        anomalies.push({
            id: `ANM-${Date.now()}-1`,
            type: 'IDLE_SPIKE',
            severity: 'MEDIUM',
            source: idleEvents[0].machineName,
            description: `Elevated idle time detected across ${idleEvents.length} instances`,
            detectedAt: new Date(),
            estimatedLoss: idleEvents.reduce((sum, e) => sum + (e.lossAmount || 0), 0),
            status: 'OPEN',
            confidence: 0.85,
        });
    }

    // Find throughput drops
    const productionEvents = events.filter(e => e.eventType === 'PRODUCTION');
    const lowEfficiency = productionEvents.filter(e => e.efficiency < 80);
    if (lowEfficiency.length > 2) {
        anomalies.push({
            id: `ANM-${Date.now()}-2`,
            type: 'THROUGHPUT_DROP',
            severity: 'HIGH',
            source: lowEfficiency[0].machineName,
            description: `Production efficiency below threshold in ${lowEfficiency.length} runs`,
            detectedAt: new Date(),
            estimatedLoss: Math.floor(lowEfficiency.reduce((sum, e) => sum + (100 - e.efficiency) * 50, 0)),
            status: 'OPEN',
            confidence: 0.92,
        });
    }

    // Hidden inefficiencies (micro-downtimes)
    const microDowntimes = events.filter(e => e.eventType === 'MICRO_DOWNTIME');
    if (microDowntimes.length > 0) {
        anomalies.push({
            id: `ANM-${Date.now()}-3`,
            type: 'HIDDEN_INEFFICIENCY',
            severity: 'LOW',
            source: 'Multiple Machines',
            description: `${microDowntimes.length} micro-downtimes detected (hidden losses)`,
            detectedAt: new Date(),
            estimatedLoss: microDowntimes.reduce((sum, e) => sum + (e.lossAmount || 0), 0),
            status: 'OPEN',
            confidence: 0.78,
            hidden: true,
        });
    }

    return anomalies;
}

// Calculate total loss
export function calculateTotalLoss(events) {
    const losses = {
        idle: 0,
        breakdown: 0,
        microDowntime: 0,
        lowEfficiency: 0,
        total: 0,
    };

    events.forEach(event => {
        if (event.eventType === 'IDLE') {
            losses.idle += event.lossAmount || 0;
        } else if (event.eventType === 'BREAKDOWN') {
            losses.breakdown += event.lossAmount || 0;
        } else if (event.eventType === 'MICRO_DOWNTIME') {
            losses.microDowntime += event.lossAmount || 0;
        } else if (event.eventType === 'PRODUCTION' && event.efficiency < 85) {
            losses.lowEfficiency += Math.floor((85 - event.efficiency) * event.duration * 10);
        }
    });

    losses.total = losses.idle + losses.breakdown + losses.microDowntime + losses.lowEfficiency;

    return losses;
}

// Generate 7 days of historical data
export function generateHistoricalData() {
    const data = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);

        const events = generateMachineEvents(date);
        const shifts = generateShiftPerformance(date);
        const losses = calculateTotalLoss(events);

        data.push({
            date: date.toISOString().split('T')[0],
            dayName: date.toLocaleDateString('en-US', { weekday: 'short' }),
            events,
            shifts,
            losses,
            totalLoss: losses.total,
            efficiency: Math.round(randFloat(75, 92) * 10) / 10,
        });
    }

    return data;
}

// Generate real-time metrics
export function generateRealtimeMetrics() {
    return {
        timestamp: new Date().toISOString(),
        activeMachines: rand(3, 5),
        totalMachines: 5,
        currentEfficiency: randFloat(78, 95),
        activeOperators: rand(4, 6),
        ongoingProduction: rand(2, 4),
        pendingAlerts: rand(1, 5),
        lossToday: rand(25000, 65000),
        lossThisHour: rand(1000, 5000),
    };
}
