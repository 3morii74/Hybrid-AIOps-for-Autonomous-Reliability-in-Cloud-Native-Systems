# 🚀 Getting Started - Deploy This Project on Your Machine

This guide helps you deploy the **AIOps Self-Healing Project** on your own environment, step by step.

---

## 📋 Prerequisites

Before you start, make sure you have:

### **Required Software:**

1. ✅ **Docker Desktop** (with Kubernetes enabled)

    - Download: https://www.docker.com/products/docker-desktop
    - After installation: Settings → Kubernetes → Enable Kubernetes
    - Wait for Kubernetes to start (green icon)

2. ✅ **Git**

    - Download: https://git-scm.com/downloads
    - Needed to clone the repository

3. ✅ **kubectl** (usually comes with Docker Desktop)

    - Verify: `kubectl version --client`

4. ✅ **Docker Hub Account** (Free)
    - Sign up: https://hub.docker.com/signup
    - You'll need this to push your Docker images

### **Optional (for development):**

-   Python 3.11+ (if you want to run the monitor locally)
-   Code editor (VS Code, PyCharm, etc.)

---

## 🎯 Quick Start (5 Steps)

### **Step 1: Clone the Repository**

```bash
# Clone the project
git clone https://github.com/YOUR_FRIEND_USERNAME/self-healing-project.git
cd self-healing-project
```

**Or download ZIP:**

-   Download the project as ZIP
-   Extract it
-   Open terminal in the extracted folder

---

### **Step 2: Login to Docker Hub**

```bash
# Login with your Docker Hub credentials
docker login -u YOUR_DOCKERHUB_USERNAME

# Enter your password when prompted
```

**Windows Users:** Use PowerShell or CMD, not Git Bash for this.

---

### **Step 3: Build and Push Patient App Image**

```bash
# Build the Patient App image
docker build -t patient-app:latest .

# Tag with YOUR Docker Hub username
docker tag patient-app:latest YOUR_DOCKERHUB_USERNAME/patient-app:latest

# Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/patient-app:latest
```

**Expected time:** 2-5 minutes

**Note:** Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username!

---

### **Step 4: Deploy to Kubernetes**

```bash
# Create deployment (use YOUR username!)
kubectl create deployment patient-app \
  --image=YOUR_DOCKERHUB_USERNAME/patient-app:latest \
  --replicas=2

# Set resource limits
kubectl set resources deployment patient-app \
  --limits=cpu=500m,memory=512Mi \
  --requests=cpu=100m,memory=128Mi

# Expose as service
kubectl expose deployment patient-app \
  --type=LoadBalancer \
  --port=5000 \
  --name=patient-app-service

# Wait for service to be ready (30-60 seconds)
kubectl get service patient-app-service --watch
# Press Ctrl+C when EXTERNAL-IP shows "localhost"
```

**Windows PowerShell:**

```powershell
# Create deployment
kubectl create deployment patient-app `
  --image=YOUR_DOCKERHUB_USERNAME/patient-app:latest `
  --replicas=2

# Set resources
kubectl set resources deployment patient-app `
  --limits=cpu=500m,memory=512Mi `
  --requests=cpu=100m,memory=128Mi

# Expose service
kubectl expose deployment patient-app `
  --type=LoadBalancer `
  --port=5000 `
  --name=patient-app-service
```

---

### **Step 5: Test It Works!**

```bash
# Test health endpoint
curl http://localhost:5000/healthz

# Expected output:
# {"status":"ok"}

# Test full health
curl http://localhost:5000/health

# View in browser
# Open: http://localhost:5000
```

**Windows PowerShell:**

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "http://localhost:5000/healthz" -UseBasicParsing

# View in browser
Start-Process "http://localhost:5000"
```

---

## ✅ Verify Deployment

```bash
# Check pods are running
kubectl get pods

# Expected output:
# NAME                           READY   STATUS    RESTARTS   AGE
# patient-app-xxxxxxxxx-xxxxx    1/1     Running   0          2m
# patient-app-xxxxxxxxx-xxxxx    1/1     Running   0          2m

# Check service
kubectl get service patient-app-service

# View logs
kubectl logs -l app=patient-app --tail=50
```

**If you see 2 pods running and can access http://localhost:5000, you're good!** ✅

---

## 🔧 Add Health Probes (Optional but Recommended)

```bash
# Add Liveness Probe
kubectl patch deployment patient-app --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/livenessProbe",
    "value": {
      "httpGet": {
        "path": "/healthz",
        "port": 5000
      },
      "initialDelaySeconds": 10,
      "periodSeconds": 10
    }
  }
]'

# Add Readiness Probe
kubectl patch deployment patient-app --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/readinessProbe",
    "value": {
      "httpGet": {
        "path": "/healthz",
        "port": 5000
      },
      "initialDelaySeconds": 5,
      "periodSeconds": 5
    }
  }
]'
```

**Windows PowerShell:** See `HOW_TO_DEPLOY.md` for PowerShell commands.

---

## 📊 Add Autoscaling (Optional)

### **Step 1: Install Metrics Server**

```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for it to start
kubectl wait --for=condition=available --timeout=60s deployment/metrics-server -n kube-system

# Patch for Docker Desktop (REQUIRED)
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--kubelet-insecure-tls"
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--kubelet-preferred-address-types=InternalIP"
  }
]'

# Wait 60 seconds for metrics to populate
echo "Waiting 60 seconds..."
sleep 60

# Verify metrics work
kubectl top nodes
kubectl top pods
```

### **Step 2: Create HPA**

```bash
# Create autoscaler
kubectl autoscale deployment patient-app \
  --min=2 \
  --max=10 \
  --cpu-percent=50 \
  --name=patient-app-hpa

# Check HPA status
kubectl get hpa patient-app-hpa

# Should show:
# NAME              REFERENCE                 TARGETS   MINPODS   MAXPODS   REPLICAS
# patient-app-hpa   Deployment/patient-app    1%/50%    2         10        2
```

---

## 🧠 Deploy ML Monitor (Optional)

### **Option 1: Run Locally (Easiest)**

```bash
# Install Python dependencies
pip install -r requirements-monitor.txt

# Port-forward to access the service
kubectl port-forward service/patient-app-service 5000:5000 &

# Run monitor
python doctor_monitor_ml.py http://localhost:5000

# You'll see health checks every 5 seconds!
# Press Ctrl+C to stop
```

### **Option 2: Deploy to Kubernetes (Advanced)**

See `REDEPLOY_ML_MONITOR.md` for full instructions.

Quick version:

```bash
# Create RBAC
kubectl create serviceaccount ml-monitor-sa
kubectl create role ml-monitor-role --verb=get,list,delete --resource=pods
kubectl create rolebinding ml-monitor-rolebinding --role=ml-monitor-role --serviceaccount=default:ml-monitor-sa

# Build and push
docker build -t ml-monitor:latest -f Dockerfile.monitor .
docker tag ml-monitor:latest YOUR_DOCKERHUB_USERNAME/ml-monitor:latest
docker push YOUR_DOCKERHUB_USERNAME/ml-monitor:latest

# Deploy
kubectl create deployment ml-monitor --image=YOUR_DOCKERHUB_USERNAME/ml-monitor:latest --replicas=1
kubectl set env deployment/ml-monitor PATIENT_URL=http://patient-app-service:5000
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa

# Watch it work
kubectl logs -f deployment/ml-monitor
```

---

## 🧪 Test the System

### **Test 1: Basic Health Check**

```bash
# Test healthz
curl http://localhost:5000/healthz

# Test health
curl http://localhost:5000/health

# Test metrics
curl http://localhost:5000/metrics
```

### **Test 2: Simulate Errors**

```bash
# Generate some errors
for i in {1..10}; do
  curl http://localhost:5000/simulate-error
  sleep 1
done

# Check health again
curl http://localhost:5000/health
# Error count should be > 0

# Heal the errors
curl -X POST http://localhost:5000/heal

# Check health again
curl http://localhost:5000/health
# Error count should be 0
```

**Windows PowerShell:**

```powershell
# Generate errors
for ($i=0; $i -lt 10; $i++) {
    Invoke-WebRequest -Uri "http://localhost:5000/simulate-error" -UseBasicParsing
    Start-Sleep -Seconds 1
}
```

### **Test 3: Autoscaling (if HPA installed)**

```bash
# Terminal 1: Watch HPA
kubectl get hpa patient-app-hpa --watch

# Terminal 2: Generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
# Inside the pod:
while true; do wget -q -O- http://patient-app-service:5000/health; done
```

Watch as HPA scales pods from 2 → 4 → 6 → 8!

Press Ctrl+C to stop load, wait 3 minutes, and watch it scale back down.

---

## 📁 Project Structure

```
self-healing-project/
├── app/
│   ├── app.py                  # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   └── healing_brain.pkl       # Trained ML model
├── Dockerfile                  # Patient App container
├── Dockerfile.monitor          # ML Monitor container
├── doctor_monitor_ml.py        # ML Monitor script
├── train_brain.py              # ML training logic
├── requirements-monitor.txt    # Monitor dependencies
├── GETTING_STARTED.md          # This file!
├── HOW_TO_DEPLOY.md           # Detailed deployment guide
├── REDEPLOY_ML_MONITOR.md     # ML Monitor guide
└── README.md                   # Project overview
```

---

## 🚨 Troubleshooting

### **Problem: Can't access http://localhost:5000**

**Solution:**

```bash
# Check if service is running
kubectl get service patient-app-service

# Check if pods are running
kubectl get pods

# Check pod logs
kubectl logs -l app=patient-app --tail=50

# Port-forward manually
kubectl port-forward service/patient-app-service 5000:5000
```

### **Problem: HPA shows `<unknown>` metrics**

**Solution:**

```bash
# Re-patch metrics-server
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--kubelet-insecure-tls"
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--kubelet-preferred-address-types=InternalIP"
  }
]'

# Wait 60 seconds
sleep 60

# Check again
kubectl top pods
kubectl get hpa
```

### **Problem: Pods not starting**

**Solution:**

```bash
# Check pod status
kubectl describe pod -l app=patient-app

# Common issues:
# - Image pull error: Check Docker Hub username in image name
# - Resource limits: Lower CPU/memory limits
# - Port conflict: Make sure port 5000 is not used by another app
```

### **Problem: Git Bash issues on Windows**

**Solution:** Use PowerShell or CMD instead of Git Bash for kubectl commands.

---

## 🧹 Clean Up Everything

When you're done testing:

```bash
# Delete all resources
kubectl delete deployment patient-app
kubectl delete service patient-app-service
kubectl delete hpa patient-app-hpa
kubectl delete deployment ml-monitor
kubectl delete serviceaccount ml-monitor-sa
kubectl delete role ml-monitor-role
kubectl delete rolebinding ml-monitor-rolebinding

# Delete metrics-server (optional)
kubectl delete deployment metrics-server -n kube-system

# Verify everything is deleted
kubectl get all
```

---

## 📚 Next Steps

1. ✅ **Completed basic deployment?** → Try adding health probes
2. ✅ **Health probes working?** → Add autoscaling (HPA)
3. ✅ **HPA working?** → Deploy ML Monitor
4. ✅ **Everything working?** → Read `HOW_TO_DEPLOY.md` for advanced features

---

## 🎓 For Presentation / Demo

### **Quick Demo Script:**

1. Show pods running: `kubectl get pods`
2. Access app in browser: http://localhost:5000
3. Show health: `curl http://localhost:5000/health`
4. Simulate errors: `curl http://localhost:5000/simulate-error` (x10)
5. Show degraded health: `curl http://localhost:5000/health`
6. Heal: `curl -X POST http://localhost:5000/heal`
7. Show healthy again: `curl http://localhost:5000/health`
8. Show ML Monitor logs: `kubectl logs -f deployment/ml-monitor`
9. Generate load and watch HPA scale: `kubectl get hpa --watch`

---

## 💡 Tips

-   **Docker images take time:** First build can take 5-10 minutes
-   **Metrics need time:** Wait 2-3 minutes after installing metrics-server
-   **HPA scales slowly:** Scale-up is fast, scale-down takes 3 minutes
-   **Windows users:** Use PowerShell for best experience
-   **Save commands:** Keep a note of your Docker Hub username

---

## ❓ Need Help?

1. Check `TROUBLESHOOTING.md` for common issues
2. Read `HOW_TO_DEPLOY.md` for detailed steps
3. Check `QUICK_START.md` for quick reference
4. View logs: `kubectl logs -l app=patient-app`

---

## 🎉 Success Checklist

-   [ ] Docker Desktop installed and Kubernetes enabled
-   [ ] Cloned/downloaded the project
-   [ ] Logged into Docker Hub
-   [ ] Built and pushed Patient App image
-   [ ] Deployed to Kubernetes (2 pods running)
-   [ ] Can access http://localhost:5000
-   [ ] Health checks working
-   [ ] (Optional) Health probes configured
-   [ ] (Optional) HPA autoscaling working
-   [ ] (Optional) ML Monitor deployed

---

**Once you complete the checklist, your project is fully deployed and ready to demo!** 🚀

**Questions?** Check the other documentation files in this repository.
