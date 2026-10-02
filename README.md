# NULLMESH DEFENSE // Multi-Domain C4ISR Architecture & Quantum Enclave

> **Autonomous Disruption-Tolerant Network (DTN), Post-Quantum Cryptography & Multi-Domain Mesh for Contested Environments.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![NIST FIPS 203](https://img.shields.io/badge/NIST-ML--KEM--768-00f3ff.svg?style=flat)](https://csrc.nist.gov)
[![QKD BB84](https://img.shields.io/badge/Quantum-BB84%20QKD-a855f7.svg?style=flat)](https://en.wikipedia.org/wiki/BB84)
[![Pytest](https://img.shields.io/badge/Tests-9%2F9%20Passing-00f59b.svg?style=flat)](https://docs.pytest.org)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg?style=flat&logo=vercel)](https://vercel.com)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7.svg?style=flat&logo=render)](https://render.com)

---

## 🌐 The 3 Dedicated Web Pages

1. **Sign In Web Page (`/signin.html`)**:
   - Original Vercel split-layout landing page.
   - Secure Commander Login & Registration.
   - Pre-authorized passwordless zero-trust access for `bhuvanjakkula@gmail.com`.

2. **Payment & Subscription Web Page (`/payment.html`)**:
   - Official Vercel Defense Access & Subscription Tiers.
   - Live Stripe Checkout links:
     - **Authorize SME ($14,999/mo)**
     - **Authorize Commandant ($89,999/mo)**
     - **Authorize Enterprise ($250k/mo)**
   - Pre-authorized defense clearance ($0.00 / month - Lifetime Defense License).

3. **Main Function Web Page (`/dashboard.html`)**:
   - 60 FPS Multi-Domain Canvas (Space, Air, Sea, Land).
   - Autonomous Node D Hot-Standby Failover (<18ms).
   - Causality & Disruption-Tolerant (CDT) Consensus ($T^* = \infty$).
   - Quantum Enclave (BB84 QKD + ML-KEM-768 Lattice Cryptography).
   - Python v0.1 Core Package Test Suite (9/9 passed).

---

## 🚀 Deployment

### 1. Vercel Deployment (Frontend)
Configured via `vercel.json` with clean URLs and security headers.
```bash
# Deploy to Vercel
npx vercel --prod
```

### 2. Render Deployment (Backend & WebSocket Stream)
Configured via `render.yaml` with Python 3.12 runtime and ASGI server:
```bash
# Build & Start
pip install -r backend/requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Local Development
```bash
# 1. Start Static Server (Port 5173)
python -m http.server 5173

# 2. Start FastAPI & WebSocket Backend (Port 8001)
python backend/main.py
```

---

## 🛡️ License
Government & Defense Enterprise Disruption-Tolerant License.
Owner: `bhuvanjakkula@gmail.com` (COMMANDANT_MAX Clearance).
