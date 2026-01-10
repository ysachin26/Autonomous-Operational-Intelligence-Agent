# 🧠 Autonomous Operational Intelligence Agent (AOIA)

<div align="center">

![AOIA Banner](https://img.shields.io/badge/AOIA-Autonomous%20Operations%20Brain-blueviolet?style=for-the-badge&logo=brain)

**Turn invisible operational loss into measurable, actionable intelligence — autonomously.**

[![React](https://img.shields.io/badge/React-18-61dafb?style=flat-square&logo=react)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://postgresql.org/)

</div>

---

## 🎯 What is AOIA?

AOIA is an **AI-powered operational intelligence platform** designed to help SMBs, factories, and BPOs detect, quantify, and eliminate hidden operational inefficiencies.

### The Problem
Every business loses **5–15% revenue** in hidden operational inefficiencies:
- ⏰ Micro-idle time
- 🔄 Workflow bottlenecks
- ⚙️ Machine micro-downtime
- 📊 Overloaded shifts
- 🔁 Repetitive tasks
- 👤 Undetected underperformance

### The Solution
AOIA becomes your **Autonomous Operations Brain** that:
- 📡 **Monitors** operations in real-time
- 🔍 **Detects** inefficiencies automatically
- 💰 **Calculates** monetary loss
- 🧠 **Analyzes** root causes using AI
- ⚡ **Triggers** optimization actions

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Live Dashboard** | Real-time operational metrics & KPIs |
| 🔥 **Loss Heatmap** | Visual problem area identification |
| 🤖 **AI Recommendations** | Actionable optimization suggestions |
| 📈 **Incident Timeline** | Chronological inefficiency tracking |
| 💬 **Chat Assistant** | Natural language operational queries |
| 📉 **Loss Calculator** | Monetary impact of inefficiencies |
| 🧠 **Root Cause Analysis** | LLM-powered reasoning |
| ⚙️ **Auto-Optimization** | Autonomous improvement actions |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aoia.git
cd aoia

# Start databases
docker-compose up -d

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Run database migrations
npm run db:migrate

# Seed demo data
npm run db:seed

# Start development servers
npm run dev
```

### Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **ML Engine**: http://localhost:8000

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                       │
│  Dashboard │ Heatmap │ Timeline │ Chat │ Recommendations │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                  BACKEND API (Node.js)                    │
│     REST API │ WebSocket │ Auth │ Business Logic          │
└──────────────────────────┬───────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│  ML ENGINE (Python)  │    │      DATA LAYER             │
│  Anomaly Detection   │    │  PostgreSQL │ Redis         │
│  Loss Calculation    │    └─────────────────────────────┘
│  LLM Reasoning       │
│  Optimization        │
└─────────────────────┘
```

---

## 📁 Project Structure

```
AOIA/
├── frontend/          # React + TailwindCSS application
├── backend/           # Node.js Express API
├── ml-engine/         # Python FastAPI ML services
├── shared/            # Shared types & utilities
├── docker-compose.yml # Database containers
└── package.json       # Monorepo configuration
```

---

## 🎭 Demo Scenarios

### BPO/Call Center
- Detect agent idle time spikes
- Calculate call handling inefficiency costs
- Recommend workload rebalancing

### Manufacturing
- Monitor machine micro-downtime
- Predict maintenance needs
- Optimize shift allocations

---

## 📊 KPIs Tracked

| Business KPIs | Technical KPIs |
|--------------|----------------|
| Operational loss reduced (₹) | Model accuracy |
| Bottlenecks resolved | Alert precision |
| Downtime reduced | Action success rate |
| Efficiency improvement | System uptime |

---

## 🔐 Security

- JWT authentication
- Role-Based Access Control (RBAC)
- Encrypted data at rest
- Complete audit trails
- CORS protection

---

## 🛣️ Roadmap

- [x] Core platform
- [x] Anomaly detection
- [x] Loss quantification
- [x] LLM reasoning
- [ ] Real IoT integration
- [ ] Mobile app
- [ ] Slack/Teams alerts
- [ ] FreeMind AI integration

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ for operational excellence**

</div>
