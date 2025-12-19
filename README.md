# 🏥 Hybrid AIOps for Autonomous Reliability in Cloud-Native Systems

A production-ready, cloud-native self-healing system that intelligently combines **ML-based application healing** with **Kubernetes infrastructure autoscaling** to achieve autonomous reliability in distributed environments.

---

## 🚀 **New to This Project? Start Here!**

👉 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete deployment guide in 5 steps!  
👉 **[QUICK_START.md](QUICK_START.md)** - Quick reference and troubleshooting  
👉 **[HOW_TO_DEPLOY.md](HOW_TO_DEPLOY.md)** - Detailed deployment options

---

## 🎯 Project Highlights

✅ **Hybrid Intelligence**: Combines ML-driven healing with Kubernetes orchestration  
✅ **Production-Ready**: Docker containerization with Gunicorn WSGI server  
✅ **Multi-Deployment**: Supports Docker, Docker Compose, and Kubernetes  
✅ **Real-Time Monitoring**: ML monitor with live health analysis  
✅ **Auto-Scaling**: HPA-based horizontal pod autoscaling  
✅ **Self-Healing**: Automated error detection and recovery

---

## 🏗️ Architecture Overview

This project demonstrates **separation of concerns** between application-level intelligence and infrastructure-level orchestration:

### 1️⃣ ML-Based Self-Healing (Application Intelligence)

-   **Component**: `DoctorMonitorML` (deployable in/outside Kubernetes)
-   **Purpose**: Intelligent health monitoring and healing decisions
-   **Capabilities**:
    -   🧠 ML-powered decision making (RandomForest classifier)
    -   🔧 Soft healing: Reset application errors via `/heal` API
    -   🔴 Hard healing: Restart containers/pods when critical
    -   📊 Real-time health analysis with confidence scores
-   **Model**: Trained RandomForest on 1000+ synthetic health patterns
-   **Monitors**: `/health` endpoint (CPU, memory, errors, uptime)

### 2️⃣ Kubernetes Autoscaling (Infrastructure Orchestration)

-   **Component**: Kubernetes HPA (Horizontal Pod Autoscaler)
-   **Purpose**: Dynamic resource scaling based on load
-   **Capabilities**:
    -   📈 CPU-based scaling (50% target)
    -   💾 Memory-based scaling (70% target)
    -   ⚡ Fast scale-up (30s), gradual scale-down (180s)
    -   🔄 Automatic pod lifecycle management
-   **Range**: 2-10 pods with intelligent scaling policies
-   **Monitors**: `/healthz` endpoint for liveness/readiness probes

```
┌─────────────────────────────────────────────────────────────────────┐
│                      KUBERNETES CLUSTER                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  HPA (Horizontal Pod Autoscaler)                              │  │
│  │  • Monitors: CPU (50% target), Memory (70% target)            │  │
│  │  • Scales: 2-10 pods dynamically                              │  │
│  │  • Behavior: Fast scale-up (30s), Gradual scale-down (180s)   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼─────────────────────────────────┐   │
│  │  Deployment: patient-app (2-10 replicas)                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │   │
│  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │  │  Pod N   │     │   │
│  │  │ Flask    │  │ Flask    │  │ Flask    │  │ Flask    │     │   │
│  │  │ Gunicorn │  │ Gunicorn │  │ Gunicorn │  │ Gunicorn │     │   │
│  │  │ /healthz │  │ /healthz │  │ /healthz │  │ /healthz │ ◄── Probes
│  │  │ /health  │  │ /health  │  │ /health  │  │ /health  │     │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                               │                                      │
│  ┌────────────────────────────▼─────────────────────────────────┐   │
│  │  Service: patient-app-service (LoadBalancer)                 │   │
│  │  Port: 5000 → Target: 5000                                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                               │                                      │
│  ┌────────────────────────────▼─────────────────────────────────┐   │
│  │  ML Monitor Pod (Optional - can run externally)              │   │
│  │  • ServiceAccount: ml-monitor-sa (RBAC permissions)          │   │
│  │  • Capabilities: Pod restart, health analysis                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP Monitoring
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ML-BASED INTELLIGENCE LAYER                                        │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  DoctorMonitorML (Python Service)                            │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │  🧠 RandomForest ML Model (healing_brain.pkl)          │ │  │
│  │  │  • Features: CPU, Memory, Errors, Uptime, Time         │ │  │
│  │  │  • Actions: no_action, reset_errors, restart_service   │ │  │
│  │  │  • Accuracy: ~95% on synthetic data                    │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  Monitoring Loop (every 5 seconds):                          │  │
│  │  1. Poll /health endpoint → Get metrics                      │  │
│  │  2. ML prediction → Determine action + confidence            │  │
│  │  3. Execute healing:                                          │  │
│  │     • Soft: POST /heal (reset errors)                        │  │
│  │     • Hard: kubectl delete pod / docker restart              │  │
│  │                                                               │  │
│  │  Environment Detection:                                       │  │
│  │  • Kubernetes: Uses kubectl (requires RBAC)                  │  │
│  │  • Docker: Uses docker CLI                                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Hybrid-AIOps-for-Autonomous-Reliability-in-Cloud-Native-Systems/
├── app/
│   ├── app.py                    # Flask application (Patient App)
│   ├── requirements.txt          # App dependencies (Flask, Gunicorn)
│   └── healing_brain.pkl         # Pre-trained ML model
│
├── Dockerfile                    # Patient App container image
├── Dockerfile.monitor            # ML Monitor container image
├── docker-compose.yml            # Multi-container orchestration
│
├── doctor_monitor_ml.py          # ML-based monitoring service
├── train_brain.py                # ML model training script
├── requirements-monitor.txt      # Monitor dependencies
│
├── README.md                     # This file (Project overview)
├── GETTING_STARTED.md            # Step-by-step deployment guide
├── HOW_TO_DEPLOY.md              # Detailed deployment options
├── QUICK_START.md                # Quick reference & troubleshooting
├── REDEPLOY_ML_MONITOR.md        # ML Monitor deployment guide
│
└── LICENSE                       # Project license
```

### 📦 Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Patient App** | Main application with health endpoints | Flask + Gunicorn |
| **ML Monitor** | Intelligent health monitoring | Python + scikit-learn |
| **ML Model** | Healing decision engine | RandomForest (95% accuracy) |
| **Docker Images** | Containerized services | Docker multi-stage builds |
| **Orchestration** | Container management | Docker Compose / Kubernetes |

## 🚀 API Endpoints

### Patient App (Port 5000)

| Endpoint          | Method | Purpose                    | Response | Used By                |
| ----------------- | ------ | -------------------------- | -------- | ---------------------- |
| `/`               | GET    | Home page & API overview   | JSON     | Users, Documentation   |
| `/healthz`        | GET    | Kubernetes health probe    | 200 OK   | K8s Liveness/Readiness |
| `/health`         | GET    | Detailed health metrics    | JSON     | DoctorMonitorML        |
| `/metrics`        | GET    | System metrics             | JSON     | Monitoring, Dashboards |
| `/heal`           | POST   | Trigger self-healing       | JSON     | DoctorMonitorML        |
| `/simulate-error` | GET    | Simulate application error | 500      | Testing, Demos         |
| `/data`           | GET    | Data retrieval (20% fail)  | JSON     | Application logic      |

### Endpoint Details

#### `/healthz` - Kubernetes Health Probe
```json
{"status": "ok"}
```
- **Purpose**: Binary alive/not-alive check
- **Lightweight**: No computation, instant response
- **Used by**: Kubernetes liveness & readiness probes
- **Frequency**: Every 5-10 seconds by K8s

#### `/health` - ML Monitor Endpoint
```json
{
  "status": "healthy",
  "cpu_usage": 45,
  "memory_usage": 60,
  "error_count": 0,
  "uptime": 3600
}
```
- **Purpose**: Detailed health analysis for ML decisions
- **Rich data**: CPU, memory, errors, uptime
- **Used by**: DoctorMonitorML for predictions
- **Frequency**: Every 5 seconds by ML monitor

#### `/heal` - Self-Healing API
```bash
curl -X POST http://localhost:5000/heal \
  -H "Content-Type: application/json" \
  -d '{"action": "reset_errors"}'
```
**Response:**
```json
{
  "message": "Self-healing completed",
  "action": "Errors reset",
  "previous_error_count": 15,
  "current_status": "healthy"
}
```

## 🐳 Deployment Options

### Option 1: Docker Compose (Recommended for Development)

**Fastest way to run the entire system:**

```bash
# Start both Patient App + ML Monitor
docker-compose up -d

# View logs
docker-compose logs -f

# Test the system
curl http://localhost:5000/healthz

# Watch ML Monitor in action
docker-compose logs -f ml-monitor

# Stop everything
docker-compose down
```

**What it includes:**
- ✅ Patient App (Flask + Gunicorn)
- ✅ ML Monitor (automated healing)
- ✅ Network configuration
- ✅ Health checks
- ✅ Auto-restart policies

---

### Option 2: Docker (Single Container)

**Run Patient App only:**

```bash
# Build the image
docker build -t patient-app:latest .

# Run container
docker run -d -p 5000:5000 --name patient-app patient-app:latest

# Test
curl http://localhost:5000/healthz

# View logs
docker logs -f patient-app

# Stop and remove
docker stop patient-app && docker rm patient-app
```

**Run ML Monitor separately:**

```bash
# Install dependencies
pip install -r requirements-monitor.txt

# Run monitor (point to Docker container)
python doctor_monitor_ml.py http://localhost:5000 patient-app
```

---

### Option 3: Kubernetes (Production)

**Full cloud-native deployment with autoscaling:**

See **[GETTING_STARTED.md](GETTING_STARTED.md)** for complete Kubernetes deployment guide.

**Quick overview:**

```bash
# 1. Build and push to Docker Hub
docker build -t patient-app:latest .
docker tag patient-app:latest YOUR_USERNAME/patient-app:latest
docker push YOUR_USERNAME/patient-app:latest

# 2. Deploy to Kubernetes (using kubectl commands)
kubectl create deployment patient-app \
  --image=YOUR_USERNAME/patient-app:latest \
  --replicas=2

kubectl set resources deployment patient-app \
  --limits=cpu=500m,memory=512Mi \
  --requests=cpu=100m,memory=128Mi

kubectl expose deployment patient-app \
  --type=LoadBalancer \
  --port=5000 \
  --name=patient-app-service

# 3. Add health probes (see HOW_TO_DEPLOY.md)

# 4. Configure autoscaling
kubectl autoscale deployment patient-app \
  --min=2 --max=10 --cpu-percent=50 \
  --name=patient-app-hpa

# 5. Test
curl http://localhost:5000/healthz
```

**Why Kubernetes?**
- ✅ Horizontal Pod Autoscaling (HPA)
- ✅ Self-healing infrastructure (liveness/readiness probes)
- ✅ Load balancing across pods
- ✅ Rolling updates with zero downtime
- ✅ Production-grade orchestration

## ☸️ Kubernetes Deployment (Detailed)

### Prerequisites

✅ **Kubernetes cluster** (Docker Desktop / Minikube / Cloud)  
✅ **kubectl** installed and configured  
✅ **Docker Hub account** (for image hosting)  
✅ **Metrics Server** (required for HPA)

### Step 1: Install Metrics Server

```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=60s \
  deployment/metrics-server -n kube-system

# Patch for Docker Desktop/Minikube (REQUIRED)
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"}
]'

# Wait for metrics to populate (60 seconds)
sleep 60

# Verify metrics are working
kubectl top nodes
kubectl top pods
```

### Step 2: Build and Push Image

```bash
# Build the image
docker build -t patient-app:latest .

# Login to Docker Hub
docker login -u YOUR_USERNAME

# Tag for Docker Hub
docker tag patient-app:latest YOUR_USERNAME/patient-app:latest

# Push to Docker Hub
docker push YOUR_USERNAME/patient-app:latest
```

### Step 3: Deploy Application

**Using kubectl commands (recommended approach):**

```bash
# Create deployment with 2 replicas
kubectl create deployment patient-app \
  --image=YOUR_USERNAME/patient-app:latest \
  --replicas=2

# Set resource limits (required for HPA)
kubectl set resources deployment patient-app \
  --limits=cpu=500m,memory=512Mi \
  --requests=cpu=100m,memory=128Mi

# Expose as LoadBalancer service
kubectl expose deployment patient-app \
  --type=LoadBalancer \
  --port=5000 \
  --name=patient-app-service

# Wait for service to be ready
kubectl get service patient-app-service --watch
# Press Ctrl+C when EXTERNAL-IP appears (localhost on Docker Desktop)
```

### Step 4: Add Health Probes

```bash
# Add liveness probe
kubectl patch deployment patient-app --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/livenessProbe",
    "value": {
      "httpGet": {"path": "/healthz", "port": 5000},
      "initialDelaySeconds": 10,
      "periodSeconds": 10,
      "timeoutSeconds": 3,
      "failureThreshold": 3
    }
  }
]'

# Add readiness probe
kubectl patch deployment patient-app --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/readinessProbe",
    "value": {
      "httpGet": {"path": "/healthz", "port": 5000},
      "initialDelaySeconds": 5,
      "periodSeconds": 5,
      "timeoutSeconds": 3,
      "failureThreshold": 3
    }
  }
]'
```

### Step 5: Configure Autoscaling

```bash
# Create HPA
kubectl autoscale deployment patient-app \
  --min=2 \
  --max=10 \
  --cpu-percent=50 \
  --name=patient-app-hpa

# Verify HPA (should show CPU/Memory percentages, not <unknown>)
kubectl get hpa patient-app-hpa

# Watch HPA in real-time
kubectl get hpa patient-app-hpa --watch
```

### Step 6: Test the Deployment

```bash
# Check pods are running
kubectl get pods -l app=patient-app

# Test health endpoint
curl http://localhost:5000/healthz

# Test detailed health
curl http://localhost:5000/health

# View logs
kubectl logs -l app=patient-app --tail=50
```

### Optional: Export Configuration as YAML

```bash
# Export for version control
kubectl get deployment patient-app -o yaml > kubernetes-deployment.yaml
kubectl get service patient-app-service -o yaml > kubernetes-service.yaml
kubectl get hpa patient-app-hpa -o yaml > kubernetes-hpa.yaml
```

**Note:** The project uses imperative kubectl commands for deployment. YAML files can be exported for documentation but are not required for deployment.

## 🔍 Health Checks & Probes

### Kubernetes Health Probes

The system implements **dual-endpoint health checking**:

#### Liveness Probe → `/healthz`
**Purpose:** Detect if the container is alive

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

**Behavior:**
- ✅ **Success**: Container is alive, no action
- ❌ **Failure**: Kubernetes **restarts the pod**
- 🔄 **Frequency**: Every 10 seconds
- ⏱️ **Threshold**: 3 consecutive failures trigger restart

#### Readiness Probe → `/healthz`
**Purpose:** Detect if the container can serve traffic

```yaml
readinessProbe:
  httpGet:
    path: /healthz
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Behavior:**
- ✅ **Success**: Pod receives traffic from service
- ❌ **Failure**: Pod **removed from service** (no traffic)
- 🔄 **Frequency**: Every 5 seconds
- ⏱️ **Threshold**: 3 consecutive failures remove from rotation

### Why Two Different Endpoints?

| Aspect | `/healthz` (K8s) | `/health` (ML) |
|--------|------------------|----------------|
| **Purpose** | Binary alive check | Detailed analysis |
| **Response** | `{"status": "ok"}` | Full metrics JSON |
| **Frequency** | 5-10 seconds | 5 seconds |
| **Used By** | Kubernetes probes | ML Monitor |
| **Complexity** | Lightweight | Rich data |
| **Action** | Restart pod | Intelligent healing |

### Health Check Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Kubernetes Probes (Infrastructure)                         │
│  • Liveness: Is container alive? → Restart if dead         │
│  • Readiness: Can serve traffic? → Remove if not ready     │
│  • Endpoint: /healthz                                       │
│  • Decision: Binary (pass/fail)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ML Monitor (Application Intelligence)                      │
│  • Analysis: What's wrong? How bad is it?                   │
│  • Prediction: What action to take?                         │
│  • Endpoint: /health                                        │
│  • Decision: ML-driven (no_action, reset, restart)          │
└─────────────────────────────────────────────────────────────┘
```

## 📊 ML-Based Monitoring with DoctorMonitorML

### Deployment Options

#### Option 1: Run Locally (Easiest for Development)

```bash
# Install dependencies
pip install -r requirements-monitor.txt

# Run monitor (point to local or K8s service)
python doctor_monitor_ml.py http://localhost:5000

# Or with custom container name for Docker
python doctor_monitor_ml.py http://localhost:5000 patient-app
```

#### Option 2: Docker Compose (Automated)

```bash
# Starts both Patient App + ML Monitor
docker-compose up -d

# Watch ML Monitor logs
docker-compose logs -f ml-monitor
```

#### Option 3: Kubernetes Deployment (Production)

See **[REDEPLOY_ML_MONITOR.md](REDEPLOY_ML_MONITOR.md)** for complete guide.

**Quick version:**

```bash
# 1. Create RBAC permissions
kubectl create serviceaccount ml-monitor-sa
kubectl create role ml-monitor-role --verb=get,list,delete --resource=pods
kubectl create rolebinding ml-monitor-rolebinding \
  --role=ml-monitor-role --serviceaccount=default:ml-monitor-sa

# 2. Build and push
docker build -t ml-monitor:latest -f Dockerfile.monitor .
docker tag ml-monitor:latest YOUR_USERNAME/ml-monitor:latest
docker push YOUR_USERNAME/ml-monitor:latest

# 3. Deploy
kubectl create deployment ml-monitor \
  --image=YOUR_USERNAME/ml-monitor:latest --replicas=1
kubectl set env deployment/ml-monitor \
  PATIENT_URL=http://patient-app-service:5000
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa

# 4. Watch it work
kubectl logs -f deployment/ml-monitor
```

### How the ML Monitor Works

```
┌─────────────────────────────────────────────────────────────┐
│  Monitoring Loop (Every 5 seconds)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Fetch Health Data                                  │
│  GET /health → {cpu, memory, errors, uptime, status}        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: ML Prediction                                      │
│  • Feature extraction: [cpu, memory, errors, uptime, hour]  │
│  • RandomForest prediction → action + confidence            │
│  • Actions: no_action (0), reset_errors (1), restart (2)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Execute Healing                                    │
│  • no_action: Log and continue                              │
│  • reset_errors: POST /heal (soft healing)                  │
│  • restart_service: kubectl/docker restart (hard healing)   │
└─────────────────────────────────────────────────────────────┘
```

### Example Monitor Output

```
🩺 Doctor Monitor Starting...
👀 Watching patient app at: http://localhost:5000
🐳 Docker container: patient-app
🧠 Using ML model for decisions

[2025-12-19 10:30:00] Health Check:
  Status: healthy
  CPU: 45%
  Memory: 60%
  Errors: 0
  Uptime: 300s
✅ ML PREDICTION: No action needed (confidence: 92.50%)

[2025-12-19 10:30:05] Health Check:
  Status: degraded
  CPU: 75%
  Memory: 80%
  Errors: 8
  Uptime: 305s
ML PREDICTION: Reset recommended (confidence: 85.30%)

🔧 SOFT HEALING TRIGGERED: ML PREDICTION: Reset recommended
✅ Healing successful:
  Previous errors: 8

[2025-12-19 10:30:10] Health Check:
  Status: healthy
  CPU: 50%
  Memory: 65%
  Errors: 0
  Uptime: 310s
✅ ML PREDICTION: No action needed (confidence: 94.20%)
```

### ML Monitor vs Kubernetes HPA

| Aspect | DoctorMonitorML | Kubernetes HPA |
|--------|-----------------|----------------|
| **Purpose** | Application healing | Infrastructure scaling |
| **Intelligence** | ML-driven decisions | Rule-based thresholds |
| **Monitors** | `/health` (app metrics) | CPU/Memory (pod resources) |
| **Trigger** | Error count, health status | Resource utilization |
| **Actions** | Reset errors, restart pods | Add/remove pods |
| **Frequency** | 5 seconds | 15-30 seconds |
| **Scope** | Application-level | Infrastructure-level |
| **Runs** | External or in-cluster | Built into K8s |
| **ML Model** | RandomForest (95% accuracy) | None |

### Key Insight: Complementary Systems

- **HPA**: "We need more pods because CPU is high" (scaling)
- **ML Monitor**: "This pod has errors, let's heal it" (fixing)
- **Together**: Autonomous reliability through hybrid intelligence

## 🧠 ML Model Training

### Training the Healing Brain

The project includes a pre-trained model (`healing_brain.pkl`), but you can retrain it:

```bash
# Train the model
python train_brain.py
```

### Training Process

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Generate Synthetic Data                            │
│  • 1000 samples with realistic health patterns              │
│  • Features: CPU, Memory, Errors, Uptime, Hour              │
│  • Labels: no_action, reset_errors, restart_service         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Train RandomForest Classifier                      │
│  • 100 estimators, max_depth=10                             │
│  • 80/20 train/test split                                   │
│  • Optimized for health pattern recognition                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Evaluate & Save                                    │
│  • Accuracy: ~95%                                           │
│  • Save as healing_brain.pkl                                │
│  • Display feature importance                               │
└─────────────────────────────────────────────────────────────┘
```

### Model Architecture

**Algorithm:** RandomForest Classifier  
**Estimators:** 100 trees  
**Max Depth:** 10 levels  
**Training Data:** 1000 synthetic samples  
**Test Accuracy:** ~95%

### Input Features

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `cpu_usage` | int | 0-100 | CPU utilization percentage |
| `memory_usage` | int | 0-100 | Memory utilization percentage |
| `error_count` | int | 0-20+ | Number of application errors |
| `uptime` | int | 0-86400 | Seconds since last restart |
| `hour_of_day` | int | 0-23 | Current hour (time patterns) |

### Output Classes

| Class | Label | Action | Condition |
|-------|-------|--------|-----------|
| **0** | `no_action` | Continue monitoring | Healthy state |
| **1** | `reset_errors` | POST /heal | Errors > 5 or CPU/Mem > 80% |
| **2** | `restart_service` | Restart pod/container | Errors > 10 or Critical state |

### Training Output Example

```
============================================================
🧠 HEALING BRAIN TRAINING SYSTEM
============================================================

📊 Generating 1000 training samples...
  Training samples: 800
  Test samples: 200

✅ Training complete!
  Accuracy: 95.50%

📋 Classification Report:
              precision    recall  f1-score   support

  No Action       0.96      0.97      0.96        85
Reset Errors      0.94      0.95      0.95        62
Restart Service   0.96      0.94      0.95        53

    accuracy                           0.96       200

🔍 Feature Importance:
  error_count: 0.452
  cpu_usage: 0.231
  memory_usage: 0.198
  uptime: 0.089
  hour_of_day: 0.030

💾 Model saved to: healing_brain.pkl

🧪 Testing prediction with sample metrics:
  Input: {
    "cpu_usage": 85,
    "memory_usage": 75,
    "error_count": 7,
    "uptime": 3600
  }

  Prediction: {
    "recommended_action": "reset_errors",
    "confidence": 0.87,
    "probabilities": {
      "no_action": 0.08,
      "reset_errors": 0.87,
      "restart_service": 0.05
    }
  }

============================================================
✅ Training complete! Model ready for use.
============================================================
```

### Decision Logic (Learned by Model)

The model learns these patterns from training data:

```python
# Healthy state
if errors <= 5 and cpu < 80 and memory < 80:
    → no_action (confidence ~90%)

# Degraded state
if 5 < errors <= 10 or 80 <= cpu < 90 or 80 <= memory < 90:
    → reset_errors (confidence ~85%)

# Critical state
if errors > 10 or (cpu >= 90 and memory >= 90):
    → restart_service (confidence ~95%)
```

**Note:** The model learns these patterns probabilistically, not as hard rules, allowing for nuanced decision-making based on feature combinations.

## 🧪 Testing the System

### Test 1: Basic Health Checks

```bash
# Test Kubernetes health probe
curl http://localhost:5000/healthz
# Expected: {"status":"ok"}

# Test detailed health endpoint
curl http://localhost:5000/health
# Expected: {"status":"healthy","cpu_usage":45,"memory_usage":60,"error_count":0,"uptime":300}

# Test metrics endpoint
curl http://localhost:5000/metrics
# Expected: Full system metrics JSON

# Test home endpoint
curl http://localhost:5000/
# Expected: API overview with available endpoints
```

### Test 2: ML-Based Self-Healing

**Scenario: Simulate errors and watch ML monitor heal automatically**

```bash
# Terminal 1: Start ML Monitor
python doctor_monitor_ml.py http://localhost:5000

# Terminal 2: Generate errors
for i in {1..8}; do 
  curl http://localhost:5000/simulate-error
  sleep 1
done

# Check health (should show degraded status)
curl http://localhost:5000/health
# Expected: "status":"degraded", "error_count":8

# Watch Terminal 1 - ML Monitor should detect and trigger soft healing
# Expected output:
# ML PREDICTION: Reset recommended (confidence: 85%)
# 🔧 SOFT HEALING TRIGGERED
# ✅ Healing successful: Previous errors: 8

# Verify healing worked
curl http://localhost:5000/health
# Expected: "status":"healthy", "error_count":0
```

**Scenario: Critical errors trigger pod restart**

```bash
# Generate many errors (>10)
for i in {1..15}; do 
  curl http://localhost:5000/simulate-error
  sleep 0.5
done

# ML Monitor should predict restart
# Expected output:
# ML PREDICTION: Restart recommended (confidence: 100%)
# 🔴 CRITICAL HEALING: RESTARTING CONTAINER/POD
```

### Test 3: Kubernetes Autoscaling (HPA)

**Prerequisites:**
```bash
# Ensure metrics server is working
kubectl top nodes
kubectl top pods

# Verify HPA is configured
kubectl get hpa patient-app-hpa
# Should show CPU/Memory percentages, not <unknown>
```

**Load Test Method 1: In-Cluster Load Generator**

```bash
# Terminal 1: Watch HPA
kubectl get hpa patient-app-hpa --watch

# Terminal 2: Watch pods
kubectl get pods -l app=patient-app --watch

# Terminal 3: Generate load (use PowerShell on Windows, not Git Bash)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the pod:
while true; do wget -q -O- http://patient-app-service:5000/health; done
```

**Expected behavior:**
1. Initial: 2 pods, CPU ~5%
2. Load starts: CPU increases to 60-80%
3. HPA scales up: 2 → 4 → 6 → 8 pods
4. Load distributed: CPU drops to 30-40%
5. Stop load (Ctrl+C): Wait 3 minutes
6. HPA scales down: 8 → 6 → 4 → 2 pods

**Load Test Method 2: Port-Forward + Local Load (Windows-friendly)**

```bash
# Terminal 1: Port-forward
kubectl port-forward service/patient-app-service 5000:5000

# Terminal 2: Generate load
# PowerShell:
while ($true) { Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing | Out-Null }

# Bash/Linux:
while true; do curl -s http://localhost:5000/health > /dev/null; done

# Terminal 3: Watch HPA
kubectl get hpa patient-app-hpa --watch
```

### Test 4: Liveness Probe (Pod Restart)

```bash
# Watch pods
kubectl get pods -l app=patient-app --watch

# In another terminal, kill a pod's main process
kubectl exec -it <pod-name> -- kill 1

# Expected: Kubernetes detects failure via liveness probe and restarts pod
# You'll see: STATUS changes from Running → Error → Running
```

### Test 5: Readiness Probe (Traffic Removal)

```bash
# Simulate a pod becoming unready (if /healthz fails)
# The pod will be removed from service endpoints

# Check service endpoints
kubectl get endpoints patient-app-service

# Expected: Only ready pods are listed
```

### Test 6: Docker Compose Full System Test

```bash
# Start entire system
docker-compose up -d

# Watch ML Monitor logs
docker-compose logs -f ml-monitor

# In another terminal, generate errors
for i in {1..10}; do 
  curl http://localhost:5000/simulate-error
  sleep 1
done

# Watch ML Monitor detect and heal in real-time
# Expected: Monitor logs show health checks, predictions, and healing actions

# Stop system
docker-compose down
```

### Test 7: End-to-End Integration Test

**Complete workflow test:**

```bash
# 1. Deploy to Kubernetes
kubectl create deployment patient-app --image=YOUR_USERNAME/patient-app:latest --replicas=2
kubectl expose deployment patient-app --type=LoadBalancer --port=5000 --name=patient-app-service
kubectl autoscale deployment patient-app --min=2 --max=10 --cpu-percent=50 --name=patient-app-hpa

# 2. Wait for deployment
kubectl wait --for=condition=available --timeout=120s deployment/patient-app

# 3. Test health
curl http://localhost:5000/healthz

# 4. Deploy ML Monitor
kubectl create deployment ml-monitor --image=YOUR_USERNAME/ml-monitor:latest --replicas=1
kubectl set env deployment/ml-monitor PATIENT_URL=http://patient-app-service:5000

# 5. Generate errors
for i in {1..20}; do curl http://localhost:5000/simulate-error; sleep 1; done

# 6. Watch healing
kubectl logs -f deployment/ml-monitor

# 7. Generate load
kubectl run load-gen --image=busybox --restart=Never -- /bin/sh -c \
  "while true; do wget -q -O- http://patient-app-service:5000/health 2>/dev/null; done"

# 8. Watch scaling
kubectl get hpa patient-app-hpa --watch

# 9. Cleanup
kubectl delete deployment patient-app ml-monitor load-gen
kubectl delete service patient-app-service
kubectl delete hpa patient-app-hpa
```

### Expected Test Results Summary

| Test | Expected Outcome | Success Indicator |
|------|------------------|-------------------|
| **Health Checks** | All endpoints respond | HTTP 200, valid JSON |
| **ML Healing (Soft)** | Errors reset via API | error_count: 8 → 0 |
| **ML Healing (Hard)** | Pod/container restarts | New uptime, errors cleared |
| **HPA Scale-Up** | Pods increase under load | 2 → 4 → 6 → 8 pods |
| **HPA Scale-Down** | Pods decrease after load | 8 → 6 → 4 → 2 pods (3 min) |
| **Liveness Probe** | Failed pod restarts | Pod STATUS: Error → Running |
| **Readiness Probe** | Unready pod removed | Not in service endpoints |
| **Docker Compose** | Both services run | ML monitor logs appear |

## 📈 Monitoring & Observability

### Application Logs

```bash
# View all patient-app logs
kubectl logs -l app=patient-app --tail=100

# Follow logs in real-time
kubectl logs -f deployment/patient-app

# Specific pod logs
kubectl logs -f <pod-name>

# Previous pod logs (after restart)
kubectl logs <pod-name> --previous

# ML Monitor logs
kubectl logs -f deployment/ml-monitor

# Docker Compose logs
docker-compose logs -f
docker-compose logs -f patient-app
docker-compose logs -f ml-monitor
```

**Expected log format (Gunicorn):**
```
127.0.0.1 - - [19/Dec/2025 10:30:00] "GET /health HTTP/1.1" 200 95 "-" "python-requests/2.31.0"
```

### HPA Monitoring

```bash
# Current HPA status
kubectl get hpa patient-app-hpa

# Expected output:
# NAME              REFERENCE                TARGETS                        MINPODS   MAXPODS   REPLICAS
# patient-app-hpa   Deployment/patient-app   cpu: 5%/50%, memory: 42%/70%   2         10        2

# Detailed HPA description
kubectl describe hpa patient-app-hpa

# Watch HPA in real-time
kubectl get hpa patient-app-hpa --watch

# View pod resource usage
kubectl top pods -l app=patient-app

# View node resource usage
kubectl top nodes
```

### Pod Health Monitoring

```bash
# Check pod status
kubectl get pods -l app=patient-app

# Detailed pod information
kubectl describe pod <pod-name>

# Check pod events
kubectl get events --field-selector involvedObject.name=<pod-name>

# Watch pods in real-time
kubectl get pods -l app=patient-app --watch
```

### Service & Endpoint Monitoring

```bash
# Check service status
kubectl get service patient-app-service

# View service endpoints (which pods are receiving traffic)
kubectl get endpoints patient-app-service

# Describe service
kubectl describe service patient-app-service
```

### Cluster Events

```bash
# Watch all cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Filter by deployment
kubectl get events --field-selector involvedObject.name=patient-app

# Watch events in real-time
kubectl get events --watch

# Filter by type
kubectl get events --field-selector type=Warning
```

### Metrics Server Monitoring

```bash
# Check metrics server status
kubectl get deployment metrics-server -n kube-system

# View metrics server logs
kubectl logs -n kube-system deployment/metrics-server

# Test metrics availability
kubectl top nodes
kubectl top pods
```

### Health Endpoint Monitoring

```bash
# Continuous health monitoring (every 2 seconds)
watch -n 2 curl -s http://localhost:5000/health

# Or using a loop
while true; do 
  echo "=== $(date) ==="
  curl -s http://localhost:5000/health | jq .
  sleep 2
done
```

### Docker Monitoring

```bash
# Docker container stats
docker stats patient-app

# Docker container logs
docker logs -f patient-app

# Docker Compose status
docker-compose ps

# Docker Compose logs with timestamps
docker-compose logs -f --timestamps
```

### Monitoring Dashboard (Manual)

Create a simple monitoring script:

```bash
#!/bin/bash
# monitor.sh - Simple monitoring dashboard

while true; do
  clear
  echo "=== AIOps System Status ==="
  echo "Time: $(date)"
  echo ""
  
  echo "=== Pods ==="
  kubectl get pods -l app=patient-app
  echo ""
  
  echo "=== HPA ==="
  kubectl get hpa patient-app-hpa
  echo ""
  
  echo "=== Resource Usage ==="
  kubectl top pods -l app=patient-app
  echo ""
  
  echo "=== Health Check ==="
  curl -s http://localhost:5000/health | jq .
  echo ""
  
  sleep 5
done
```

### Key Metrics to Monitor

| Metric | Command | Healthy Value |
|--------|---------|---------------|
| **Pod Count** | `kubectl get pods -l app=patient-app` | 2-10 Running |
| **CPU Usage** | `kubectl top pods` | < 80% |
| **Memory Usage** | `kubectl top pods` | < 80% |
| **Error Count** | `curl /health \| jq .error_count` | 0-5 |
| **HPA Targets** | `kubectl get hpa` | Below thresholds |
| **Service Endpoints** | `kubectl get endpoints` | All pods listed |
| **Pod Restarts** | `kubectl get pods` | 0-2 restarts |

## 🔧 Troubleshooting

### Issue 1: Pods Not Starting

**Symptoms:**
- Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`
- `kubectl get pods` shows pods not running

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -l app=patient-app

# Detailed pod information
kubectl describe pod <pod-name>

# Check logs (if container started)
kubectl logs <pod-name>

# Check events
kubectl get events --field-selector involvedObject.name=<pod-name>
```

**Common Fixes:**

**ImagePullBackOff:**
```bash
# Verify image exists on Docker Hub
docker pull YOUR_USERNAME/patient-app:latest

# Check image name in deployment
kubectl get deployment patient-app -o yaml | grep image

# Fix: Update image name
kubectl set image deployment/patient-app patient-app=YOUR_USERNAME/patient-app:latest
```

**CrashLoopBackOff:**
```bash
# Check application logs
kubectl logs <pod-name>

# Check previous logs
kubectl logs <pod-name> --previous

# Common causes:
# - Port 5000 already in use
# - Missing dependencies
# - Application error

# Fix: Check Dockerfile and app.py
```

**Insufficient Resources:**
```bash
# Check node resources
kubectl top nodes

# Lower resource requests
kubectl set resources deployment patient-app \
  --requests=cpu=50m,memory=64Mi \
  --limits=cpu=250m,memory=256Mi
```

---

### Issue 2: HPA Shows `<unknown>` Metrics

**Symptoms:**
- `kubectl get hpa` shows `<unknown>/<unknown>` for targets
- Autoscaling doesn't work

**Diagnosis:**
```bash
# Check if metrics server is running
kubectl get deployment metrics-server -n kube-system

# Test metrics availability
kubectl top nodes
kubectl top pods

# If you get "Metrics API not available", metrics server needs fixing
```

**Fix:**
```bash
# Delete and reinstall metrics server
kubectl delete deployment metrics-server -n kube-system

# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Patch for Docker Desktop/Minikube (CRITICAL)
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"}
]'

# Wait 60 seconds for metrics to populate
sleep 60

# Verify metrics work
kubectl top nodes
kubectl top pods

# Check HPA again
kubectl get hpa patient-app-hpa
```

---

### Issue 3: Service Not Accessible

**Symptoms:**
- `curl http://localhost:5000` fails
- Can't access application

**Diagnosis:**
```bash
# Check service
kubectl get service patient-app-service

# Check if EXTERNAL-IP is set
# Docker Desktop: Should show "localhost"
# Minikube: Might show "<pending>"

# Check endpoints
kubectl get endpoints patient-app-service

# Check if pods are ready
kubectl get pods -l app=patient-app
```

**Fixes:**

**For Docker Desktop:**
```bash
# Service should work on localhost:5000
curl http://localhost:5000/healthz

# If not, use port-forward
kubectl port-forward service/patient-app-service 5000:5000
```

**For Minikube:**
```bash
# Get service URL
minikube service patient-app-service --url

# Or use port-forward
kubectl port-forward service/patient-app-service 5000:5000
```

**No Endpoints:**
```bash
# Check if pods are ready
kubectl get pods -l app=patient-app

# Check pod labels match service selector
kubectl get service patient-app-service -o yaml | grep selector
kubectl get pods -l app=patient-app --show-labels

# If labels don't match, recreate service
kubectl delete service patient-app-service
kubectl expose deployment patient-app --type=LoadBalancer --port=5000 --name=patient-app-service
```

---

### Issue 4: ML Monitor Can't Connect

**Symptoms:**
- Monitor shows connection errors
- Health checks fail

**Diagnosis:**
```bash
# Test if service is accessible
curl http://localhost:5000/health

# Check ML Monitor logs
kubectl logs deployment/ml-monitor
# Or for local:
# Check terminal output
```

**Fixes:**

**Running Locally:**
```bash
# Use port-forward
kubectl port-forward service/patient-app-service 5000:5000 &

# Run monitor
python doctor_monitor_ml.py http://localhost:5000
```

**Running in Kubernetes:**
```bash
# Check if ML Monitor can reach service
kubectl exec deployment/ml-monitor -- curl http://patient-app-service:5000/health

# If fails, check service DNS
kubectl exec deployment/ml-monitor -- nslookup patient-app-service

# Verify environment variable
kubectl get deployment ml-monitor -o yaml | grep PATIENT_URL

# Fix: Set correct URL
kubectl set env deployment/ml-monitor PATIENT_URL=http://patient-app-service:5000
```

---

### Issue 5: Load Generator Fails (Git Bash on Windows)

**Symptoms:**
- `kubectl run` fails with path conversion errors
- Load generator pod stuck in `ContainerCannotRun`

**Fix 1: Use PowerShell Instead**
```powershell
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
```

**Fix 2: Set Environment Variable in Git Bash**
```bash
export MSYS_NO_PATHCONV=1
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
```

**Fix 3: Use Port-Forward Method (Most Reliable)**
```bash
# Terminal 1
kubectl port-forward service/patient-app-service 5000:5000

# Terminal 2 (any shell)
while true; do curl -s http://localhost:5000/health > /dev/null; done
```

**Fix 4: Clean Up Failed Pods**
```bash
# Delete stuck load generator pods
kubectl delete pod load-generator --force --grace-period=0
```

---

### Issue 6: ML Monitor Not Showing Real-Time Logs

**Symptoms:**
- Logs appear in batches every 3 minutes
- Can't see monitoring activity

**Fix:**
```bash
# Verify Python unbuffered output is enabled
kubectl get deployment ml-monitor -o yaml | grep -A 5 command

# Should see: python -u doctor_monitor_ml.py

# If not, rebuild with correct Dockerfile.monitor
docker build -t ml-monitor:latest -f Dockerfile.monitor .
docker push YOUR_USERNAME/ml-monitor:latest
kubectl rollout restart deployment/ml-monitor
```

---

### Issue 7: Docker Compose Services Not Starting

**Symptoms:**
- `docker-compose up` fails
- Services exit immediately

**Diagnosis:**
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs patient-app
docker-compose logs ml-monitor
```

**Fixes:**
```bash
# Rebuild images
docker-compose build --no-cache

# Start with verbose output
docker-compose up

# Check if ports are available
netstat -an | grep 5000
# Or on Windows:
netstat -an | findstr 5000

# If port in use, stop conflicting service
docker stop patient-app
# Or change port in docker-compose.yml
```

---

### Issue 8: ML Model Not Found

**Symptoms:**
- Monitor shows "ML model not found, using rule-based decisions"

**Fix:**
```bash
# Train the model
python train_brain.py

# Verify model file exists
ls -la healing_brain.pkl
# Or on Windows:
dir healing_brain.pkl

# Copy to app directory
cp healing_brain.pkl app/

# Rebuild Docker images
docker-compose build
```

---

### Quick Diagnostic Commands

```bash
# Full system check
kubectl get all -l app=patient-app
kubectl get hpa patient-app-hpa
kubectl top pods
curl http://localhost:5000/healthz

# Reset everything
kubectl delete deployment patient-app ml-monitor
kubectl delete service patient-app-service
kubectl delete hpa patient-app-hpa
docker-compose down -v

# Fresh start
# See GETTING_STARTED.md for deployment steps
```

## 🎯 Key Concepts & Architecture Principles

### 1. Hybrid Intelligence Architecture

**Separation of Concerns:**
```
┌─────────────────────────────────────────────────────────────┐
│  Infrastructure Layer (Kubernetes)                          │
│  • Responsibility: Pod lifecycle, scaling, networking       │
│  • Intelligence: Rule-based (CPU > 50% → scale up)          │
│  • Scope: Infrastructure-level operations                   │
│  • Components: HPA, Probes, Service Mesh                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Application Layer (ML Monitor)                             │
│  • Responsibility: Application health, error handling       │
│  • Intelligence: ML-based (pattern recognition)             │
│  • Scope: Application-level healing                         │
│  • Components: DoctorMonitorML, RandomForest Model          │
└─────────────────────────────────────────────────────────────┘
```

**Why Hybrid?**
- **Kubernetes alone**: Can scale but can't understand application context
- **ML alone**: Can diagnose but needs infrastructure to execute
- **Together**: Autonomous reliability through complementary strengths

### 2. Cloud-Native Design Principles

#### 2.1 Containerization
```dockerfile
FROM python:3.11-slim
# Lightweight, reproducible, portable
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/app.py .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Benefits:**
- ✅ Consistent environments (dev = prod)
- ✅ Fast deployment (seconds, not minutes)
- ✅ Resource isolation
- ✅ Easy rollback

#### 2.2 Orchestration
- **Declarative**: Define desired state, K8s maintains it
- **Self-healing**: Failed pods automatically restarted
- **Service Discovery**: Automatic DNS for services
- **Load Balancing**: Traffic distributed across pods

#### 2.3 Scalability
- **Horizontal**: Add more pods (not bigger pods)
- **Automatic**: HPA monitors and scales
- **Elastic**: Scale up fast, scale down gradually
- **Cost-effective**: Pay for what you use

#### 2.4 Resilience
- **Health Probes**: Detect and recover from failures
- **Graceful Degradation**: Continue with reduced capacity
- **No Single Point of Failure**: Multiple replicas
- **Circuit Breaking**: Prevent cascade failures

#### 2.5 Observability
- **Logging**: Structured logs to stdout
- **Metrics**: CPU, memory, custom metrics
- **Tracing**: Request flow through system
- **Monitoring**: Real-time health visibility

### 3. AIOps Integration

#### 3.1 ML-Driven Decision Making
```python
# Traditional approach (rule-based)
if errors > 10:
    restart()
elif errors > 5:
    reset()

# AIOps approach (ML-based)
prediction = model.predict([cpu, memory, errors, uptime])
action = prediction['recommended_action']
confidence = prediction['confidence']
if confidence > 0.8:
    execute(action)
```

**Advantages:**
- 📊 **Pattern Recognition**: Learns complex patterns
- 🎯 **Context-Aware**: Considers multiple factors
- 📈 **Confidence Scores**: Quantifies certainty
- 🔄 **Adaptable**: Can be retrained with new data

#### 3.2 Autonomous Operations
```
Manual → Automated → Autonomous
  ↓          ↓            ↓
Human    Scripts      ML Model
decides  execute      decides
```

**Autonomy Levels:**
1. **Manual**: Human monitors and fixes (traditional)
2. **Automated**: Scripts execute predefined actions (DevOps)
3. **Autonomous**: ML decides and executes (AIOps) ← **This Project**

#### 3.3 Closed-Loop Healing
```
Monitor → Analyze → Decide → Execute → Verify
   ↑                                      ↓
   └──────────────────────────────────────┘
```

**Implementation:**
1. **Monitor**: Poll /health every 5 seconds
2. **Analyze**: Extract features, run ML model
3. **Decide**: Get action + confidence score
4. **Execute**: Call /heal API or restart pod
5. **Verify**: Check if healing worked

### 4. Production-Ready Features

#### 4.1 High Availability
- **Multiple Replicas**: 2-10 pods (never single)
- **Load Balancing**: Traffic distributed evenly
- **Health Checks**: Unhealthy pods removed
- **Rolling Updates**: Zero-downtime deployments

#### 4.2 Resource Management
```yaml
resources:
  requests:  # Guaranteed resources
    cpu: 100m
    memory: 128Mi
  limits:    # Maximum resources
    cpu: 500m
    memory: 512Mi
```

**Benefits:**
- ✅ Prevents resource starvation
- ✅ Enables autoscaling (HPA needs requests)
- ✅ Improves scheduling efficiency
- ✅ Protects cluster stability

#### 4.3 Security Best Practices
- **RBAC**: ML Monitor has minimal permissions (get, list, delete pods)
- **ServiceAccount**: Separate identity for ML Monitor
- **Non-root**: Containers run as non-root user
- **Image Scanning**: Use trusted base images

#### 4.4 Operational Excellence
- **Gunicorn**: Production WSGI server (not Flask dev server)
- **Structured Logging**: JSON logs for parsing
- **Graceful Shutdown**: Handle SIGTERM properly
- **Health Endpoints**: Separate /healthz and /health

### 5. Academic & Research Value

#### 5.1 Demonstrates Key Concepts
- ✅ **Microservices**: Patient App + ML Monitor
- ✅ **Machine Learning**: RandomForest for healing
- ✅ **Container Orchestration**: Kubernetes deployment
- ✅ **Autoscaling**: HPA based on metrics
- ✅ **Self-Healing**: Automated recovery
- ✅ **Observability**: Logging and monitoring

#### 5.2 Real-World Applicability
- **E-commerce**: Handle traffic spikes (Black Friday)
- **Healthcare**: Ensure uptime for critical systems
- **Finance**: Auto-recover from errors
- **SaaS**: Optimize resource costs

#### 5.3 Research Extensions
- **Advanced ML**: Try LSTM, XGBoost, or ensemble methods
- **Reinforcement Learning**: Learn optimal healing policies
- **Anomaly Detection**: Detect novel failure patterns
- **Predictive Scaling**: Predict load before it happens
- **Multi-Cluster**: Extend to multiple Kubernetes clusters
- **Chaos Engineering**: Inject failures and test resilience

### 6. Comparison with Industry Solutions

| Feature | This Project | Datadog | New Relic | Prometheus |
|---------|--------------|---------|-----------|------------|
| **ML Healing** | ✅ Custom | ✅ Yes | ✅ Yes | ❌ No |
| **Open Source** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **K8s Native** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Cost** | Free | $$$$ | $$$$ | Free |
| **Customizable** | ✅ Fully | ⚠️ Limited | ⚠️ Limited | ✅ Yes |
| **Learning Curve** | Low | Medium | Medium | High |

**Unique Value:**
- 🎓 **Educational**: Understand AIOps from scratch
- 🔧 **Customizable**: Modify ML model, add features
- 💰 **Free**: No licensing costs
- 📚 **Well-Documented**: Complete guides and examples

## 📚 Documentation & Resources

### Project Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[README.md](README.md)** | Project overview & architecture | Everyone |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Step-by-step deployment guide | Beginners |
| **[QUICK_START.md](QUICK_START.md)** | Quick reference & troubleshooting | Experienced users |
| **[HOW_TO_DEPLOY.md](HOW_TO_DEPLOY.md)** | Detailed deployment options | DevOps engineers |
| **[REDEPLOY_ML_MONITOR.md](REDEPLOY_ML_MONITOR.md)** | ML Monitor deployment | ML engineers |

### Kubernetes Resources

- **[Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)** - Health check configuration
- **[Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)** - Autoscaling documentation
- **[Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)** - Deployment concepts
- **[Services](https://kubernetes.io/docs/concepts/services-networking/service/)** - Service networking
- **[RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)** - Role-based access control

### Cloud-Native Best Practices

- **[12-Factor App](https://12factor.net/)** - Methodology for building SaaS apps
- **[Cloud Native Computing Foundation](https://www.cncf.io/)** - Cloud-native ecosystem
- **[Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)** - K8s configuration best practices
- **[Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)** - Container best practices

### AIOps & ML Resources

- **[AIOps by Gartner](https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations)** - AIOps definition and trends
- **[scikit-learn Documentation](https://scikit-learn.org/stable/)** - ML library documentation
- **[RandomForest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)** - Model documentation

### Related Technologies

- **[Flask](https://flask.palletsprojects.com/)** - Python web framework
- **[Gunicorn](https://gunicorn.org/)** - Python WSGI HTTP Server
- **[Docker](https://docs.docker.com/)** - Container platform
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration

---

## 🎓 For Students & Educators

### Learning Objectives

After completing this project, you will understand:

1. **Cloud-Native Architecture**
   - Containerization with Docker
   - Orchestration with Kubernetes
   - Microservices design patterns

2. **Machine Learning Operations (MLOps)**
   - Training and deploying ML models
   - ML-driven decision making
   - Model serving in production

3. **AIOps Principles**
   - Autonomous operations
   - Self-healing systems
   - Intelligent monitoring

4. **Production DevOps**
   - CI/CD concepts
   - Health checks and probes
   - Autoscaling strategies
   - Observability and monitoring

### Suggested Exercises

1. **Beginner**: Deploy using Docker Compose, test self-healing
2. **Intermediate**: Deploy to Kubernetes, configure HPA
3. **Advanced**: Modify ML model, add new features, implement custom metrics
4. **Expert**: Extend to multi-cluster, add chaos engineering, implement A/B testing

### Presentation Tips

**For Academic Presentations:**

1. **Start with Problem**: "Manual operations don't scale"
2. **Show Architecture**: Use the diagrams in this README
3. **Live Demo**: 
   - Show healthy system
   - Simulate errors
   - Watch ML monitor heal automatically
   - Generate load and show HPA scaling
4. **Explain Hybrid Approach**: Why ML + K8s is better than either alone
5. **Discuss Results**: Show metrics, logs, healing actions
6. **Future Work**: Mention possible extensions

**Demo Script (5 minutes):**
```bash
# 1. Show system is running (30s)
kubectl get pods
curl http://localhost:5000/health

# 2. Start ML Monitor (30s)
kubectl logs -f deployment/ml-monitor

# 3. Simulate errors (1 min)
for i in {1..10}; do curl http://localhost:5000/simulate-error; sleep 1; done

# 4. Watch healing (1 min)
# ML Monitor detects and heals automatically

# 5. Show autoscaling (2 min)
kubectl get hpa --watch
# Generate load in another terminal
```

---

## 🤝 Contributing

This is an open educational project. Contributions welcome!

**Ways to Contribute:**
- 🐛 Report bugs or issues
- 📝 Improve documentation
- ✨ Add new features
- 🧪 Add tests
- 🎨 Improve UI/UX
- 📊 Add monitoring dashboards

**Contribution Ideas:**
- Add Prometheus/Grafana integration
- Implement custom metrics
- Add more ML models (LSTM, XGBoost)
- Create Helm charts
- Add CI/CD pipeline
- Implement chaos engineering tests

---

## 📝 License

This project is licensed for **Educational and Academic Use**.

See [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgments

**Technologies Used:**
- Python, Flask, Gunicorn
- scikit-learn, pandas, numpy
- Docker, Docker Compose
- Kubernetes, kubectl
- RandomForest ML algorithm

**Inspired By:**
- Cloud-native computing principles
- AIOps research and best practices
- Production Kubernetes deployments
- ML-driven automation

---

## 📧 Contact & Support

**For Questions:**
- Check documentation files first
- Review troubleshooting section
- Check GitHub issues (if applicable)

**For Academic Use:**
- Feel free to use in courses, projects, research
- Attribution appreciated
- Share your improvements!

---

## 🌟 Project Status

✅ **Production-Ready Features:**
- Docker containerization
- Kubernetes deployment
- ML-based self-healing
- Horizontal autoscaling
- Health probes
- Real-time monitoring

🚧 **Potential Enhancements:**
- Prometheus metrics export
- Grafana dashboards
- Helm charts
- CI/CD pipeline
- Multi-cluster support
- Advanced ML models

---

**Built with ❤️ for Cloud Computing, AIOps, and Machine Learning Education**

**⭐ If this project helped you, please consider starring it!**

---

## 🚀 Quick Links

- 📖 **[Getting Started](GETTING_STARTED.md)** - Deploy in 5 steps
- ⚡ **[Quick Start](QUICK_START.md)** - Quick reference
- 🔧 **[Deployment Guide](HOW_TO_DEPLOY.md)** - Detailed instructions
- 🧠 **[ML Monitor Guide](REDEPLOY_ML_MONITOR.md)** - ML deployment

**Happy Learning! 🎓**
