# 🚀 Quick Start Guide

## ⚠️ Important Notes

**Before you start:**

1. **Metrics Server Patch Required**: Docker Desktop and Minikube need the metrics-server patched with `--kubelet-insecure-tls` flag (see Step 2 below)
2. **Wait for Metrics**: After installing metrics-server, wait 30-60 seconds for metrics to populate
3. **Load Testing**: Use the busybox load generator inside the cluster or port-forward for local testing

## Prerequisites

-   Docker installed
-   Kubernetes cluster (Minikube/Docker Desktop/Cloud)
-   kubectl configured
-   Python 3.11+ (for monitor)

## 1️⃣ Docker Deployment (5 minutes)

```bash
# Build image
docker build -t patient-app:latest .

# Run container
docker run -d -p 5000:5000 --name patient-app patient-app:latest

# Test
curl http://localhost:5000/healthz
```

## 2️⃣ Kubernetes Deployment (10 minutes)

```bash
# Step 1: Install and configure metrics server (REQUIRED for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Step 2: Patch metrics server for Docker Desktop/Minikube (IMPORTANT!)
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"}
]'

# Step 3: Wait for metrics-server to be ready
kubectl wait --for=condition=available --timeout=120s deployment/metrics-server -n kube-system

# Step 4: Deploy application
kubectl apply -f kubernetes-deployment.yaml
kubectl apply -f kubernetes-service.yaml
kubectl apply -f kubernetes-hpa.yaml

# Step 5: Verify deployment
kubectl get pods
kubectl get svc
kubectl get hpa

# Step 6: Wait for metrics to populate (30-60 seconds)
echo "Waiting for metrics to populate..."
sleep 30

# Step 7: Verify metrics are working
kubectl top nodes
kubectl top pods

# Step 8: Access application
# For Minikube:
minikube service patient-app-service --url

# For Docker Desktop or port-forward:
kubectl port-forward service/patient-app-service 5000:5000

# Test
curl http://localhost:5000/healthz
```

## 3️⃣ Run ML Monitor (External)

```bash
# Install dependencies
pip install flask pandas scikit-learn joblib requests numpy

# Run monitor (adjust URL to your service)
python doctor_monitor_ml.py http://localhost:5000
```

## 4️⃣ Test Self-Healing

```bash
# Terminal 1: Watch monitor logs
python doctor_monitor_ml.py http://localhost:5000

# Terminal 2: Simulate errors
for i in {1..30}; do curl http://localhost:5000/simulate-error; done

# Terminal 3: Watch Kubernetes
kubectl get pods --watch

# Observe: Monitor will detect errors and trigger healing
```

## 5️⃣ Test Autoscaling

### ⚠️ Before Testing: Clean Up Old Load Generators

If you've tested before or after Docker restart, clean up any failed pods:

```bash
# Check for failed load generator pods
kubectl get pods | grep load

# Delete all load generator pods (if any exist)
kubectl delete pod load-generator load-gen-1 load-gen-2 load-gen-3 --force --grace-period=0 2>/dev/null || true
```

### Method 1: Using Load Generator Pod (Recommended)

**⚠️ Windows Users:** Use **PowerShell** or **CMD** for this method, NOT Git Bash (Git Bash has path conversion issues).

```bash
# Terminal 1: Watch HPA
kubectl get hpa patient-app-hpa --watch

# Terminal 2: Generate load inside cluster (use PowerShell not bash or CMD on Windows)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the pod, run:
while true; do wget -q -O- http://patient-app-service:5000/health; done

# Observe: HPA will scale up pods based on CPU usage

# Note: Press Ctrl+C to stop, pod will auto-delete due to --rm flag
```

**Git Bash Users:** If you must use Git Bash, set this first:

```bash
export MSYS_NO_PATHCONV=1
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
```

### Method 2: Using Port-Forward + Local Load (Recommended for Windows)

**This method works reliably on all platforms, including Windows with Git Bash.**

```bash
# Terminal 1: Port-forward (works in any shell)
kubectl port-forward service/patient-app-service 5000:5000

# Terminal 2: Generate load locally
# For PowerShell:
while ($true) {
    Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing | Out-Null
}

# For Git Bash / Linux / macOS:
while true; do curl -s http://localhost:5000/health > /dev/null; sleep 0.01; done

# Terminal 3: Watch HPA
kubectl get hpa patient-app-hpa --watch


## 📊 Key Endpoints

-   `/healthz` - Kubernetes health probe
-   `/health` - ML monitor endpoint
-   `/metrics` - System metrics
-   `/simulate-error` - Trigger errors
-   `/heal` - Self-healing API

## 🔍 Troubleshooting

### Pods not starting?

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### HPA not working? (Shows `<unknown>` for metrics)

**This is the most common issue!** The metrics-server needs to be patched for Docker Desktop/Minikube.

```bash
# Check if metrics are available
kubectl top pods

# If you get "Metrics API not available", fix it:
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"}
]'

# Wait for metrics-server to restart
kubectl wait --for=condition=available --timeout=120s deployment/metrics-server -n kube-system

# Wait 30-60 seconds for metrics to populate
sleep 60

# Verify metrics are working
kubectl top nodes
kubectl top pods

# Check HPA status
kubectl describe hpa patient-app-hpa
```

### Can't access service?

```bash
kubectl get svc
kubectl port-forward service/patient-app-service 5000:5000
```

### Load generator pods in Error or ContainerCannotRun state?

**This happens after Docker restarts or if pods weren't cleaned up properly.**

```bash
# Check for failed pods
kubectl get pods | grep load

# Delete ALL load generator pods (force cleanup)
kubectl delete pod load-generator load-gen-1 load-gen-2 load-gen-3 --force --grace-period=0 2>/dev/null || true

# Wait for deletion to complete
sleep 3

# Verify they're gone
kubectl get pods | grep load

# Now you can create new load generators
```

### Load generator pod stuck or timing out?

```bash
# Delete stuck pod
kubectl delete pod load-generator --force --grace-period=0

# Use background load generators instead (no interactive session)
kubectl run load-gen-1 --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://patient-app-service:5000/health 2>/dev/null; done"

# Or use port-forward + local load (simplest and most reliable)
kubectl port-forward service/patient-app-service 5000:5000
# Then in another terminal:
while true; do curl -s http://localhost:5000/health > /dev/null; done
```

## ✅ Success Indicators

Your deployment is successful when you see:

```bash
# Metrics working
$ kubectl top nodes
NAME             CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
docker-desktop   209m         1%       1717Mi          22%

$ kubectl top pods
NAME                           CPU(cores)   MEMORY(bytes)
patient-app-76d57dd494-vmqs2   1m           52Mi
patient-app-76d57dd494-xbpck   1m           53Mi

# HPA showing metrics (not <unknown>)
$ kubectl get hpa patient-app-hpa
NAME              REFERENCE                TARGETS                        MINPODS   MAXPODS   REPLICAS
patient-app-hpa   Deployment/patient-app   cpu: 1%/50%, memory: 41%/70%   2         10        2

# All pods running
$ kubectl get pods -l app=patient-app
NAME                           READY   STATUS    RESTARTS   AGE
patient-app-76d57dd494-vmqs2   1/1     Running   0          5m
patient-app-76d57dd494-xbpck   1/1     Running   0          5m
```

## 🎯 Expected Behavior

### During Load Test:

1. **Initial**: 2 pods, CPU ~1%, Memory ~40%
2. **Load Applied**: CPU increases to 60-80%
3. **HPA Triggers**: Scales up to 4-6 pods
4. **Load Distributed**: CPU drops back to 30-40%
5. **Stabilization**: Maintains higher pod count for 5 minutes
6. **Scale Down**: After 5 minutes of low load, scales back to 2 pods

### During Self-Healing Test:

1. **Errors Simulated**: Error count increases
2. **Monitor Detects**: ML model predicts healing action
3. **Healing Triggered**: POST to /heal endpoint
4. **System Recovers**: Error count resets to 0
5. **Status Returns**: System returns to healthy state

## 🧹 Cleanup (When Done Testing)

### Clean Up Load Generators

```bash
# Delete all load generator pods
kubectl delete pod load-generator load-gen-1 load-gen-2 load-gen-3 --force --grace-period=0 2>/dev/null || true

# Verify cleanup
kubectl get pods | grep load
```

### Clean Up Entire Deployment (Optional)

```bash
# Delete Kubernetes resources
kubectl delete -f kubernetes-hpa.yaml
kubectl delete -f kubernetes-service.yaml
kubectl delete -f kubernetes-deployment.yaml

# Verify deletion
kubectl get all -l app=patient-app

# Delete Docker container (if running locally)
docker stop patient-app
docker rm patient-app
docker rmi patient-app:latest
```

### After Docker Desktop Restart

If you restart Docker Desktop, you may need to:

```bash
# 1. Clean up failed pods
kubectl delete pod --all --force --grace-period=0 2>/dev/null || true

# 2. Redeploy application
kubectl apply -f kubernetes-deployment.yaml
kubectl apply -f kubernetes-service.yaml
kubectl apply -f kubernetes-hpa.yaml

# 3. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=patient-app --timeout=120s

# 4. Verify everything is running
kubectl get pods
kubectl get hpa patient-app-hpa
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
