# 🏥 AIOps Self-Healing System with Kubernetes

A cloud-native self-healing application that combines **ML-based self-healing** with **Kubernetes autoscaling** to create a robust, production-ready system.

---

## 🚀 **New to This Project? Start Here!**

👉 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete guide to deploy on your machine in 5 steps!

---

## 🏗️ Architecture Overview

This project demonstrates the **separation of concerns** between two critical cloud operations:

### 1️⃣ ML-Based Self-Healing (Application-Level)

-   **Component**: `DoctorMonitorML` (runs outside Kubernetes)
-   **Purpose**: Monitors application health and makes intelligent healing decisions
-   **Actions**:
    -   Soft healing: Reset errors via `/heal` API
    -   Hard healing: Restart containers when critical
-   **Uses**: Trained RandomForest ML model (`healing_brain.pkl`)
-   **Monitors**: `/health` endpoint for detailed metrics

### 2️⃣ Kubernetes Autoscaling (Infrastructure-Level)

-   **Component**: Kubernetes HPA (Horizontal Pod Autoscaler)
-   **Purpose**: Scale pods based on resource utilization
-   **Actions**: Add/remove pods based on CPU/memory thresholds
-   **Uses**: Kubernetes metrics server
-   **Monitors**: `/healthz` endpoint for liveness/readiness probes

```
┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  HPA (Horizontal Pod Autoscaler)                     │   │
│  │  - Monitors CPU/Memory                               │   │
│  │  - Scales pods up/down                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │  Deployment: patient-app                              │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │  │
│  │  │  Pod 1  │  │  Pod 2  │  │  Pod 3  │               │  │
│  │  │ /healthz│  │ /healthz│  │ /healthz│ ◄─ Probes     │  │
│  │  │ /health │  │ /health │  │ /health │               │  │
│  │  └─────────┘  └─────────┘  └─────────┘               │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │  Service: patient-app-service                         │  │
│  │  Type: LoadBalancer / NodePort                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Monitors /health
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  EXTERNAL MONITORING (Outside Kubernetes)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DoctorMonitorML                                     │   │
│  │  - Uses ML model (healing_brain.pkl)                 │   │
│  │  - Monitors /health endpoint                         │   │
│  │  - Triggers self-healing actions                     │   │
│  │  - Does NOT scale pods (HPA's job)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
self-healing-project/
├── app/
│   ├── app.py                    # Flask application
│   ├── requirements.txt          # Python dependencies
│   └── healing_brain.pkl         # Trained ML model
├── Dockerfile                    # Production-ready container image
├── kubernetes-deployment.yaml    # Kubernetes Deployment config
├── kubernetes-service.yaml       # Kubernetes Service config
├── kubernetes-hpa.yaml           # Horizontal Pod Autoscaler config
├── doctor_monitor_ml.py          # External ML-based monitor
├── train_brain.py                # ML model training script
└── README.md                     # This file
```

## 🚀 API Endpoints

### Patient App (Port 5000)

| Endpoint          | Method | Purpose                 | Used By                |
| ----------------- | ------ | ----------------------- | ---------------------- |
| `/healthz`        | GET    | Kubernetes health probe | K8s Liveness/Readiness |
| `/health`         | GET    | Detailed health metrics | DoctorMonitorML        |
| `/metrics`        | GET    | System metrics          | Monitoring             |
| `/heal`           | POST   | Trigger self-healing    | DoctorMonitorML        |
| `/simulate-error` | GET    | Simulate errors         | Testing                |
| `/data`           | GET    | Data retrieval endpoint | Application            |

### Key Differences:

-   **`/healthz`**: Lightweight, returns `{"status": "ok"}`, used by Kubernetes
-   **`/health`**: Detailed metrics (CPU, memory, errors), used by ML monitor

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t patient-app:latest .
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name patient-app patient-app:latest
```

### Test the Application

```bash
# Check health
curl http://localhost:5000/healthz

# Get detailed health
curl http://localhost:5000/health

# Simulate an error
curl http://localhost:5000/simulate-error
```

### Docker Commands Reference

```bash
# View logs
docker logs patient-app

# Stop container
docker stop patient-app

# Remove container
docker rm patient-app

# Run interactively (see output)
docker run -p 5000:5000 patient-app:latest
```

## ☸️ Kubernetes Deployment

### Prerequisites

1. **Kubernetes cluster** (Minikube, Docker Desktop, or cloud provider)
2. **kubectl** installed and configured
3. **Metrics Server** installed (required for HPA)

```bash
# Install metrics server (if not already installed)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Step 1: Build and Push Image

```bash
# Build the image
docker build -t patient-app:latest .

# Tag for your registry (if using remote cluster)
docker tag patient-app:latest <your-registry>/patient-app:latest

# Push to registry (if needed)
docker push <your-registry>/patient-app:latest
```

### Step 2: Deploy to Kubernetes

```bash
# Create deployment
kubectl apply -f kubernetes-deployment.yaml

# Create service
kubectl apply -f kubernetes-service.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services
```

### Step 3: Configure Autoscaling

```bash
# Apply HPA configuration
kubectl apply -f kubernetes-hpa.yaml

# Verify HPA
kubectl get hpa

# Watch HPA in action
kubectl get hpa patient-app-hpa --watch
```

### Step 4: Access the Application

```bash
# Get service URL (for Minikube)
minikube service patient-app-service --url

# Or use port-forward
kubectl port-forward service/patient-app-service 5000:5000

# Test the application
curl http://localhost:5000/healthz
```

### Alternative: Using kubectl Commands (Without YAML)

```bash
# Create deployment
kubectl create deployment patient-app --image=patient-app:latest --replicas=2

# Expose as service
kubectl expose deployment patient-app --type=LoadBalancer --port=5000 --target-port=5000 --name=patient-app-service

# Configure autoscaling
kubectl autoscale deployment patient-app --cpu-percent=50 --min=2 --max=10

# Export YAML for documentation
kubectl get deployment patient-app -o yaml > kubernetes-deployment.yaml
kubectl get service patient-app-service -o yaml > kubernetes-service.yaml
kubectl get hpa patient-app -o yaml > kubernetes-hpa.yaml
```

## 🔍 Health Checks & Probes

### Kubernetes Health Probes Configuration

The deployment uses `/healthz` for both liveness and readiness probes:

**Liveness Probe:**

-   Checks if the pod is alive
-   Kubernetes restarts the pod if it fails
-   Endpoint: `GET /healthz`
-   Expected: HTTP 200

**Readiness Probe:**

-   Checks if the pod is ready to receive traffic
-   Kubernetes removes pod from service if it fails
-   Endpoint: `GET /healthz`
-   Expected: HTTP 200

### Why `/healthz`?

1. **Lightweight**: Returns immediately without heavy computation
2. **Standard**: Follows Kubernetes conventions
3. **Separate from monitoring**: Doesn't interfere with ML-based health checks
4. **Simple**: Binary alive/not-alive check

## 📊 Monitoring with DoctorMonitorML

### Running the ML Monitor (Outside Kubernetes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the monitor
python doctor_monitor_ml.py http://<service-url>:5000
```

### What the Monitor Does

1. **Polls `/health`** every 5 seconds
2. **Analyzes metrics** using trained ML model
3. **Predicts healing action**:
    - `no_action`: System is healthy
    - `reset_errors`: Soft healing via `/heal` API
    - `restart_service`: Hard healing (container restart)
4. **Executes healing** based on prediction

### Monitor vs HPA

| Feature      | DoctorMonitorML       | Kubernetes HPA       |
| ------------ | --------------------- | -------------------- |
| **Purpose**  | Self-healing          | Scaling              |
| **Trigger**  | Application errors    | Resource utilization |
| **Action**   | Reset errors, restart | Add/remove pods      |
| **Uses ML**  | Yes                   | No                   |
| **Monitors** | `/health`             | CPU/Memory metrics   |
| **Runs**     | External              | Inside K8s           |

## 🧠 ML Model Training

### Train the Healing Brain

```bash
python train_brain.py
```

This will:

1. Generate 1000 synthetic training samples
2. Train a RandomForest classifier
3. Save model as `healing_brain.pkl`
4. Display accuracy and feature importance

### Model Features

-   `cpu_usage`: CPU utilization percentage
-   `memory_usage`: Memory utilization percentage
-   `error_count`: Number of errors
-   `uptime`: Application uptime in seconds
-   `hour_of_day`: Time-based patterns

### Predicted Actions

-   `0`: No action needed
-   `1`: Reset errors (soft healing)
-   `2`: Restart service (hard healing)

## 🧪 Testing the System

### Test 1: Basic Health Check

```bash
# Check Kubernetes health probe
curl http://localhost:5000/healthz
# Expected: {"status": "ok"}

# Check detailed health
curl http://localhost:5000/health
# Expected: Full health metrics
```

### Test 2: Simulate Errors and Healing

```bash
# Simulate multiple errors
for i in {1..6}; do curl http://localhost:5000/simulate-error; done

# Check health (should show degraded status)
curl http://localhost:5000/health

# Watch monitor logs - it should trigger healing automatically
```

### Test 3: Kubernetes Autoscaling

```bash
# Generate load to trigger HPA
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the pod, generate requests
while true; do wget -q -O- http://patient-app-service:5000/health; done

# In another terminal, watch HPA scale up
kubectl get hpa patient-app-hpa --watch
```

### Test 4: Pod Restart (Liveness Probe)

```bash
# Simulate pod crash (if implemented)
kubectl exec -it <pod-name> -- kill 1

# Kubernetes will automatically restart the pod
kubectl get pods --watch
```

## 📈 Monitoring & Observability

### View Logs

```bash
# Application logs
kubectl logs -f deployment/patient-app

# Specific pod logs
kubectl logs -f <pod-name>

# Previous pod logs (after restart)
kubectl logs <pod-name> --previous
```

### Check HPA Status

```bash
# Current HPA status
kubectl get hpa

# Detailed HPA description
kubectl describe hpa patient-app-hpa

# Watch HPA metrics
kubectl top pods
```

### Monitor Events

```bash
# Watch cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Filter by deployment
kubectl get events --field-selector involvedObject.name=patient-app
```

## 🔧 Troubleshooting

### Issue: Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Common fixes:
# - Verify image exists: docker images | grep patient-app
# - Check resource limits in deployment
# - Ensure port 5000 is not blocked
```

### Issue: HPA not scaling

```bash
# Verify metrics server is running
kubectl get deployment metrics-server -n kube-system

# Check if metrics are available
kubectl top pods

# Verify HPA configuration
kubectl describe hpa patient-app-hpa

# Common fixes:
# - Install metrics server
# - Set resource requests in deployment
# - Wait 1-2 minutes for metrics to populate
```

### Issue: Service not accessible

```bash
# Check service
kubectl get svc patient-app-service

# Check endpoints
kubectl get endpoints patient-app-service

# Test from inside cluster
kubectl run test-pod --image=busybox -it --rm -- wget -O- http://patient-app-service:5000/healthz

# Common fixes:
# - Verify selector labels match deployment
# - Check if pods are ready
# - Use port-forward for local testing
```

### Issue: Monitor can't connect

```bash
# Get service URL
kubectl get svc patient-app-service

# For Minikube
minikube service patient-app-service --url

# Use port-forward
kubectl port-forward service/patient-app-service 5000:5000

# Then run monitor
python doctor_monitor_ml.py http://localhost:5000
```

## 🎯 Key Concepts for Academic Projects

### 1. Separation of Concerns

-   **Kubernetes**: Infrastructure-level operations (scaling, health checks, restarts)
-   **ML Monitor**: Application-level intelligence (error analysis, healing decisions)

### 2. Cloud-Native Principles

-   **Containerization**: Application runs in Docker
-   **Orchestration**: Kubernetes manages lifecycle
-   **Scalability**: HPA handles load
-   **Resilience**: Probes ensure availability
-   **Observability**: Logs and metrics

### 3. AIOps Integration

-   **ML-Driven**: Decisions based on trained model
-   **Automated**: No manual intervention
-   **Predictive**: Anticipates issues
-   **Adaptive**: Learns from patterns

### 4. Production Readiness

-   **Health Probes**: Liveness and readiness checks
-   **Autoscaling**: Handles variable load
-   **Resource Limits**: Prevents resource exhaustion
-   **Graceful Degradation**: Continues operating under stress

## 📚 Additional Resources

### Kubernetes Documentation

-   [Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
-   [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
-   [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

### Best Practices

-   [12-Factor App](https://12factor.net/)
-   [Cloud Native Computing Foundation](https://www.cncf.io/)
-   [AIOps Best Practices](https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations)

## 🤝 Contributing

This is an academic project demonstrating:

-   Cloud-native application design
-   ML-based self-healing
-   Kubernetes orchestration
-   Production deployment practices

## 📝 License

Educational/Academic Use

---

**Built with ❤️ for Cloud Computing & AIOps Education**
