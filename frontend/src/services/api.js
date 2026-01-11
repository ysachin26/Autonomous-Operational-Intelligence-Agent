/**
 * AOIA + ASLOA API Service
 * Connects frontend to ML Engine endpoints
 */

import axios from 'axios';

// API base URLs
const ML_ENGINE_URL = 'http://localhost:8000';
const BACKEND_URL = 'http://localhost:3001';

// Create axios instances
const mlApi = axios.create({
    baseURL: ML_ENGINE_URL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000,
});

const backendApi = axios.create({
    baseURL: BACKEND_URL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 30000,
});

// Add auth token to backend requests
backendApi.interceptors.request.use((config) => {
    const token = localStorage.getItem('aoia_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

/**
 * AOIA Operations API
 */
export const aoiaApi = {
    // Run AOIA pipeline (BPO, Retail, SaaS, Healthcare, etc.)
    runPipeline: async (data) => {
        const response = await mlApi.post('/api/pipeline/run', data);
        return response.data;
    },

    // Get pipeline status
    getStatus: async () => {
        const response = await mlApi.get('/api/pipeline/status');
        return response.data;
    },

    // Set autonomy mode
    setMode: async (mode) => {
        const response = await mlApi.post('/api/pipeline/mode', { mode });
        return response.data;
    },

    // Run BPO demo
    runBpoDemo: async () => {
        const response = await mlApi.post('/api/demo/bpo-sla-prevention');
        return response.data;
    },

    // Get available demo scenarios
    getDemoScenarios: async () => {
        const response = await mlApi.get('/api/demo/scenarios');
        return response.data;
    },
};

/**
 * ASLOA Sales Automation API
 */
export const asloaApi = {
    // Process a lead through 7-agent pipeline
    processLead: async (leadData) => {
        const response = await mlApi.post('/api/asloa/process-lead', leadData);
        return response.data;
    },

    // Get sales dashboard
    getDashboard: async () => {
        const response = await mlApi.get('/api/asloa/dashboard');
        return response.data;
    },

    // Health check
    getHealth: async () => {
        const response = await mlApi.get('/api/asloa/health');
        return response.data;
    },
};

/**
 * Anomaly Detection API
 */
export const detectionApi = {
    // Detect anomalies
    detect: async (data) => {
        const response = await mlApi.post('/api/detect', data);
        return response.data;
    },

    // Batch detection
    detectBatch: async (batchData) => {
        const response = await mlApi.post('/api/detect/batch', batchData);
        return response.data;
    },
};

/**
 * Chat & Reasoning API
 */
export const chatApi = {
    // Send chat message
    chat: async (message, context = {}) => {
        const response = await mlApi.post('/api/chat', { message, context });
        return response.data;
    },

    // Get explanation for anomaly
    explain: async (anomalyId) => {
        const response = await mlApi.post('/api/chat/explain', { anomaly_id: anomalyId });
        return response.data;
    },
};

/**
 * Analytics API
 */
export const analyticsApi = {
    // Get loss analysis
    analyzeLoss: async (anomalies) => {
        const response = await mlApi.post('/api/analyze/loss', { anomalies });
        return response.data;
    },
};

/**
 * Health Check
 */
export const healthCheck = async () => {
    try {
        const [mlHealth, backendHealth] = await Promise.allSettled([
            mlApi.get('/health'),
            backendApi.get('/health'),
        ]);

        return {
            mlEngine: mlHealth.status === 'fulfilled' ? 'healthy' : 'unavailable',
            backend: backendHealth.status === 'fulfilled' ? 'healthy' : 'unavailable',
        };
    } catch (error) {
        return { mlEngine: 'error', backend: 'error', error: error.message };
    }
};

export default {
    aoia: aoiaApi,
    asloa: asloaApi,
    detection: detectionApi,
    chat: chatApi,
    analytics: analyticsApi,
    healthCheck,
};
