# 🚀 Complete Deployment Guide

## 📋 Overview

This guide provides **battle-tested** deployment instructions based on real troubleshooting and fixes. All commands have been verified to work on Windows with Docker Desktop.

---

## 🎯 Three Deployment Options

### **Option 1: Docker Compose** ⭐ EASIEST (Development)

-   Runs both Patient App + ML Monitor
-   Single command deployment
-   Best for testing and demos

### **Option 2: Kubernetes** ⭐ REQUIRED (Academic/Production)

-   Production-grade orchestration
-   Auto-scaling with HPA
-   Satisfies all academic requirements

### **Option 3: Plain Docker**

-   Single container (Patient App only)
-   Manual ML Monitor execution

---

## 🐳 Option 1: Docker Compose (Quickest Setup)

### **Step 1: Start Everything**

**Bash/Linux/Mac:**

```bash
# Build and start both services
docker-compose up -d

# View logs
docker-compose logs -f
```

**Windows PowerShell:**

```powershell
# Build and start both services
docker-compose up -d

# View logs
docker-compose logs -f
```

### **Step 2: Test**

```bash
# Test health endpoint
curl http://localhost:5000/healthz

# View ML Monitor logs (watch it work!)
docker-compose logs -f ml-monitor
```

### **Step 3: Stop**

```bash
docker-compose down
```

**See `DOCKER_COMPOSE_GUIDE.md` for more details**

---

## ☸️ Option 2: Kubernetes (Full Academic Compliance)

### **Prerequisites**

✅ Docker Desktop with Kubernetes enabled
✅ Docker Hub account
✅ kubectl installed

---

## 🐳 Part 1: Build and Push Docker Image

### **Step 1: Build Patient App Image**

```bash
# Build the image
docker build -t patient-app:latest .

# Test locally (optional)
docker run -d -p 5000:5000 --name patient-app-test patient-app:latest
curl http://localhost:5000/healthz
docker stop patient-app-test
docker rm patient-app-test
```

### **Step 2: Login to Docker Hub**

```bash
# Login (you'll be prompted for password)
docker login -u YOUR_USERNAME
```

### **Step 3: Tag and Push**

```bash
# Tag the image
docker tag patient-app:latest YOUR_USERNAME/patient-app:latest

# Push to Docker Hub
docker push YOUR_USERNAME/patient-app:latest
```

**✅ Academic Requirement 2: Containerization - COMPLETE**

---

## ☸️ Part 2: Kubernetes Deployment

### **IMPORTANT: Clean Up Old Resources First**

If you've deployed before, clean up first:

```bash
# Delete old resources
kubectl delete deployment patient-app 2>/dev/null || true
kubectl delete service patient-app-service 2>/dev/null || true
kubectl delete hpa patient-app-hpa 2>/dev/null || true
kubectl delete hpa patient-app 2>/dev/null || true

# Verify clean slate
kubectl get deployments
kubectl get services
kubectl get hpa
```

### **Step 1: Create Deployment**

```bash
# Create deployment with 2 replicas
kubectl create deployment patient-app \
  --image=3morii74/patient-app:latest \
  --replicas=2
```

**Windows PowerShell:**

```powershell
kubectl create deployment patient-app `
  --image=YOUR_USERNAME/patient-app:latest `
  --replicas=2
```

### **Step 2: Set Resource Limits**

```bash
# Set CPU and memory limits/requests
kubectl set resources deployment patient-app \
  --limits=cpu=500m,memory=512Mi \
  --requests=cpu=100m,memory=128Mi
```

**Windows PowerShell:**

```powershell
kubectl set resources deployment patient-app `
  --limits=cpu=500m,memory=512Mi `
  --requests=cpu=100m,memory=128Mi
```

### **Step 3: Expose as Service**

```bash
# Create LoadBalancer service
kubectl expose deployment patient-app \
  --type=LoadBalancer \
  --port=5000 \
  --name=patient-app-service
```

### **Step 4: Wait for Service to be Ready**

```bash
# Wait for service (may take 30-60 seconds)
kubectl get service patient-app-service --watch

# Stop watching with Ctrl+C when EXTERNAL-IP appears
```

**Windows PowerShell:**

```powershell
# Check service status
kubectl get service patient-app-service

# Wait until EXTERNAL-IP shows (localhost on Docker Desktop)
```

### **Step 5: Test the Deployment**

```bash
# Test healthz endpoint
curl http://localhost:5000/healthz

# Test health endpoint
curl http://localhost:5000/health

# Test metrics endpoint
curl http://localhost:5000/metrics
```

**✅ Academic Requirement 3: Kubernetes Deployment - COMPLETE**

---

## 🏥 Part 3: Health Probes (CRITICAL FIX)

### **⚠️ IMPORTANT: kubectl set probe is DEPRECATED**

Use `kubectl patch` instead to add health probes.

### **Step 1: Add Liveness Probe**

**Bash/Linux/Mac:**

```bash
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
      "periodSeconds": 10,
      "timeoutSeconds": 3,
      "failureThreshold": 3
    }
  }
]'
```

**Windows PowerShell:**

```powershell
kubectl patch deployment patient-app --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/livenessProbe","value":{"httpGet":{"path":"/healthz","port":5000},"initialDelaySeconds":10,"periodSeconds":10,"timeoutSeconds":3,"failureThreshold":3}}]'
```

### **Step 2: Add Readiness Probe**

**Bash/Linux/Mac:**

```bash
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
      "periodSeconds": 5,
      "timeoutSeconds": 3,
      "failureThreshold": 3
    }
  }
]'
```

**Windows PowerShell:**

```powershell
kubectl patch deployment patient-app --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/readinessProbe","value":{"httpGet":{"path":"/healthz","port":5000},"initialDelaySeconds":5,"periodSeconds":5,"timeoutSeconds":3,"failureThreshold":3}}]'
```

### **Step 3: Verify Probes**

```bash
# Check deployment configuration
kubectl describe deployment patient-app | grep -A 10 "Liveness"
kubectl describe deployment patient-app | grep -A 10 "Readiness"

# Wait for pods to restart with new probes
kubectl get pods --watch
```

**✅ Academic Requirement 4: Health Checks - COMPLETE**

---

## 📊 Part 4: Horizontal Pod Autoscaler (HPA)

### **Step 1: Install/Fix Metrics Server**

**⚠️ CRITICAL: Metrics Server Must Work for HPA**

```bash
# Delete old metrics-server
kubectl delete deployment metrics-server -n kube-system 2>/dev/null || true

# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for deployment
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

# Wait for metrics-server to restart
echo "Waiting 60 seconds for metrics-server to stabilize..."
sleep 60
```

**Windows PowerShell:**

```powershell
# Delete old metrics-server
kubectl delete deployment metrics-server -n kube-system 2>$null

# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=60s deployment/metrics-server -n kube-system

# Patch for Docker Desktop (REQUIRED)
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"}]'

# Wait for metrics-server to stabilize
Start-Sleep -Seconds 60
```

### **Step 2: Verify Metrics Server**

```bash
# Check metrics-server logs
kubectl logs -n kube-system deployment/metrics-server

# Test metrics (should show CPU/Memory, not errors)
kubectl top nodes
kubectl top pods

# If you see "error: Metrics API not available", wait another 30 seconds and try again
```

### **Step 3: Create HPA**

```bash
# Create autoscaler (min 2, max 10 pods, 50% CPU target)
kubectl autoscale deployment patient-app \
  --min=2 \
  --max=10 \
  --cpu-percent=50 \
  --name=patient-app-hpa
```

**Windows PowerShell:**

```powershell
kubectl autoscale deployment patient-app `
  --min=2 `
  --max=10 `
  --cpu-percent=50 `
  --name=patient-app-hpa
```

**Note:** You may see "Flag --cpu-percent has been deprecated" - this is just a warning, it still works.

### **Step 4: Apply Advanced HPA Configuration**

**Bash/Linux/Mac:**

```bash
kubectl patch hpa patient-app-hpa --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/metrics",
    "value": [
      {
        "type": "Resource",
        "resource": {
          "name": "cpu",
          "target": {
            "type": "Utilization",
            "averageUtilization": 50
          }
        }
      },
      {
        "type": "Resource",
        "resource": {
          "name": "memory",
          "target": {
            "type": "Utilization",
            "averageUtilization": 70
          }
        }
      }
    ]
  },
  {
    "op": "add",
    "path": "/spec/behavior",
    "value": {
      "scaleDown": {
        "stabilizationWindowSeconds": 180,
        "policies": [
          {
            "type": "Percent",
            "value": 50,
            "periodSeconds": 60
          },
          {
            "type": "Pods",
            "value": 1,
            "periodSeconds": 60
          }
        ],
        "selectPolicy": "Min"
      },
      "scaleUp": {
        "stabilizationWindowSeconds": 0,
        "policies": [
          {
            "type": "Percent",
            "value": 100,
            "periodSeconds": 30
          },
          {
            "type": "Pods",
            "value": 2,
            "periodSeconds": 30
          }
        ],
        "selectPolicy": "Max"
      }
    }
  }
]'
```

**Windows PowerShell:**

```powershell
kubectl patch hpa patient-app-hpa --type='json' -p='[{"op":"add","path":"/spec/metrics","value":[{"type":"Resource","resource":{"name":"cpu","target":{"type":"Utilization","averageUtilization":50}}},{"type":"Resource","resource":{"name":"memory","target":{"type":"Utilization","averageUtilization":70}}}]},{"op":"add","path":"/spec/behavior","value":{"scaleDown":{"stabilizationWindowSeconds":300,"policies":[{"type":"Percent","value":50,"periodSeconds":60},{"type":"Pods","value":1,"periodSeconds":60}],"selectPolicy":"Min"},"scaleUp":{"stabilizationWindowSeconds":0,"policies":[{"type":"Percent","value":100,"periodSeconds":30},{"type":"Pods","value":2,"periodSeconds":30}],"selectPolicy":"Max"}}}]'
```

### **Step 5: Verify HPA**

```bash
# Check HPA status (should show actual percentages, not <unknown>)
kubectl get hpa patient-app-hpa

# Detailed view
kubectl describe hpa patient-app-hpa

# Watch in real-time
kubectl get hpa patient-app-hpa --watch
```

**Expected output:**

```
NAME              REFERENCE                 TARGETS          MINPODS   MAXPODS   REPLICAS
patient-app-hpa   Deployment/patient-app    1%/50%, 41%/70%  2         10        2
```

**If you see `<unknown>`:** Wait 2-3 minutes for metrics to populate, or re-patch the metrics-server.

---

## 🧪 Part 5: Test Autoscaling

### **Step 1: Generate Load**

If you've tested before or after Docker restart, clean up any failed pods:

```bash
# Check for failed load generator pods
kubectl get pods | grep load

# Delete all load generator pods (if any exist)
kubectl delete pod load-generator load-gen-1 load-gen-2 load-gen-3 --force --grace-period=0 2>/dev/null || true
```

**⚠️ Windows Users:** Use **PowerShell** or **CMD** for this method, NOT Git Bash (Git Bash has path conversion issues).

````bash
# Terminal 1: Watch HPA
kubectl get hpa patient-app-hpa --watch

# Terminal 2: Generate load inside cluster (use PowerShell not bash or CMD on Windows)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the pod, run:
while true; do wget -q -O- http://patient-app-service:5000/health; done



### **Step 2: Watch Scaling**

**Open a second terminal:**

```bash
# Watch HPA scale up
kubectl get hpa patient-app-hpa --watch

# Watch pods being created
kubectl get pods --watch
````

**Expected behavior:**

-   CPU usage increases to 50%+
-   HPA creates new pods (up to 10)
-   After you stop load, HPA waits 5 minutes
-   Then scales down gradually

**Scale-down timing:** 180 seconds (3 minutes) - defined in HPA behavior

---

## 🧠 Part 6: Deploy ML Monitor (Optional)

### **Option A: Run Locally (Easiest for Demo)**

```bash
# Install dependencies
pip install -r requirements-monitor.txt

# Run monitor (point to Kubernetes service)
kubectl port-forward service/patient-app-service 5000:5000 &
python doctor_monitor_ml.py http://localhost:5000

# Press Ctrl+C to stop
```

### **Option B: Deploy to Kubernetes (Production)**

#### **Step 1: Create RBAC Permissions (Required)**

ML Monitor needs permission to delete pods for self-healing:

```bash
# Create ServiceAccount
kubectl create serviceaccount ml-monitor-sa

# Create Role (allows pod management)
kubectl create role ml-monitor-role \
  --verb=get,list,delete \
  --resource=pods

# Create RoleBinding
kubectl create rolebinding ml-monitor-rolebinding \
  --role=ml-monitor-role \
  --serviceaccount=default:ml-monitor-sa
```

**Windows PowerShell:**

```powershell
kubectl create serviceaccount ml-monitor-sa
kubectl create role ml-monitor-role --verb=get,list,delete --resource=pods
kubectl create rolebinding ml-monitor-rolebinding --role=ml-monitor-role --serviceaccount=default:ml-monitor-sa
```

#### **Step 2: Build and Push ML Monitor**

```bash
# Build ML Monitor image
docker build -t ml-monitor:latest -f Dockerfile.monitor .

# Tag and push to Docker Hub
docker tag ml-monitor:latest YOUR_USERNAME/ml-monitor:latest
docker push YOUR_USERNAME/ml-monitor:latest
```

#### **Step 3: Deploy ML Monitor**

```bash
# Create Deployment
kubectl create deployment ml-monitor \
  --image=YOUR_USERNAME/ml-monitor:latest \
  --replicas=1

# Set Patient App URL
kubectl set env deployment/ml-monitor \
  PATIENT_URL=http://patient-app-service:5000

# Set ServiceAccount (IMPORTANT - enables pod restart)
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa

# View logs (real-time health checks)
kubectl logs -f deployment/ml-monitor
```

**Windows PowerShell:**

```powershell
# Create Deployment
kubectl create deployment ml-monitor `
  --image=YOUR_USERNAME/ml-monitor:latest `
  --replicas=1

# Set environment variable
kubectl set env deployment/ml-monitor `
  PATIENT_URL=http://patient-app-service:5000

# Set ServiceAccount
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa

# View logs
kubectl logs -f deployment/ml-monitor
```



## 🚀 Quick Redeploy Command:

```bash
# All in one:
kubectl create serviceaccount ml-monitor-sa && \
kubectl create role ml-monitor-role --verb=get,list,delete --resource=pods && \
kubectl create rolebinding ml-monitor-rolebinding --role=ml-monitor-role --serviceaccount=default:ml-monitor-sa && \
docker build -t ml-monitor:latest -f Dockerfile.monitor . && \
docker tag ml-monitor:latest 3morii74/ml-monitor:latest && \
docker push 3morii74/ml-monitor:latest && \
kubectl delete deployment ml-monitor && \
kubectl create deployment ml-monitor --image=3morii74/ml-monitor:latest --replicas=1 && \
kubectl set env deployment/ml-monitor PATIENT_URL=http://patient-app-service:5000 && \
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa && \
echo "✅ ML Monitor redeployed! Watch logs with: kubectl logs -f deployment/ml-monitor"
```

---

**Your ML Monitor is now fully functional with real-time logging and Kubernetes pod restart capability!** 🎉




#### **Step 4: Export YAML (for GitHub)**

```bash
kubectl get serviceaccount ml-monitor-sa -o yaml > kubernetes-ml-monitor-sa.yaml
kubectl get role ml-monitor-role -o yaml > kubernetes-ml-monitor-role.yaml
kubectl get rolebinding ml-monitor-rolebinding -o yaml > kubernetes-ml-monitor-rolebinding.yaml
kubectl get deployment ml-monitor -o yaml > kubernetes-ml-monitor-deployment.yaml
```

---

## 📤 Part 7: Export YAML Files (for GitHub)

### **Export All Resources**

```bash
# Export Deployment
kubectl get deployment patient-app -o yaml > kubernetes-deployment.yaml

# Export Service
kubectl get service patient-app-service -o yaml > kubernetes-service.yaml

# Export HPA (use correct name!)
kubectl get hpa patient-app-hpa -o yaml > kubernetes-hpa.yaml
```

### **Clean Up YAML Files (Optional)**

Remove auto-generated fields to make YAML cleaner:

**Manual cleanup:** Remove these sections:

-   `metadata.uid`
-   `metadata.resourceVersion`
-   `metadata.creationTimestamp`
-   `metadata.generation`
-   `metadata.selfLink`
-   `status` (entire section)
-   `metadata.annotations.kubectl.kubernetes.io/last-applied-configuration`

**Or use kubectl neat plugin:**

```bash
# Install kubectl-neat
kubectl krew install neat

# Export clean YAML
kubectl get deployment patient-app -o yaml | kubectl neat > kubernetes-deployment.yaml
kubectl get service patient-app-service -o yaml | kubectl neat > kubernetes-service.yaml
kubectl get hpa patient-app-hpa -o yaml | kubectl neat > kubernetes-hpa.yaml
```

---

## ✅ Verification Checklist

### **1. Docker Image**

```bash
# Should see your image on Docker Hub
docker pull YOUR_USERNAME/patient-app:latest
```

### **2. Kubernetes Deployment**

```bash
# Should show 2+ pods running
kubectl get pods -l app=patient-app

# Should show all pods ready
kubectl get deployment patient-app
```

### **3. Service**

```bash
# Should show LoadBalancer with localhost external IP
kubectl get service patient-app-service

# Should respond with 200
curl http://localhost:5000/healthz
```

### **4. Health Probes**

```bash
# Should show liveness and readiness probes configured
kubectl describe deployment patient-app | grep -A 10 "Liveness"
```

### **5. HPA**

```bash
# Should show actual CPU/Memory percentages (not <unknown>)
kubectl get hpa patient-app-hpa

# Should show metrics
kubectl top pods
```

### **6. Application Logs**

```bash
# Should see Gunicorn access logs
kubectl logs -l app=patient-app --tail=50

# Expected format:
# 127.0.0.1 - - [timestamp] "GET /healthz HTTP/1.1" 200 18 "-" "curl/..."
```

---

## 🚨 Common Issues & Fixes

### **Issue 1: HPA shows `<unknown>` for metrics**

**Fix:**

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

# Verify
kubectl top pods
```

### **Issue 2: Load generator pod fails with Git Bash**

**Fix:** Use PowerShell instead for load generation, or set:

```bash
export MSYS_NO_PATHCONV=1
```

### **Issue 3: Duplicate HPA resources**

**Fix:**

```bash
# Delete duplicate HPA
kubectl delete hpa patient-app

# Keep only patient-app-hpa
kubectl get hpa
```

### **Issue 4: "deployment already exists" error**

**Fix:**

```bash
# Clean up first
kubectl delete deployment patient-app
kubectl delete service patient-app-service
kubectl delete hpa patient-app-hpa

# Then recreate
```

### **Issue 5: Can't export HPA YAML**

**Fix:** Use correct HPA name:

```bash
# Wrong
kubectl get hpa patient-app -o yaml

# Correct
kubectl get hpa patient-app-hpa -o yaml
```

### **Issue 6: Application logs not showing**

**Solution:** Logs ARE being generated by Gunicorn. Check with:

```bash
kubectl logs -l app=patient-app --tail=100
```

---

## 🎓 For Academic Presentation

### **What to Say:**

**1. Containerization:**

> "I created a production-ready Dockerfile with Gunicorn WSGI server, health checks, and the trained ML model. The image is pushed to Docker Hub and can be deployed anywhere."

**2. Kubernetes Deployment:**

> "I deployed using kubectl commands rather than manual YAML writing. The deployment includes 2 replicas for high availability, with LoadBalancer service for external access."

**3. Health Checks:**

> "I implemented both liveness and readiness probes using the `/healthz` endpoint. Liveness probe restarts unhealthy containers, while readiness probe ensures traffic only goes to ready pods."

**4. Autoscaling:**

> "The HPA monitors CPU and memory metrics and automatically scales from 2 to 10 pods based on load. It includes a 5-minute stabilization window to prevent flapping. This demonstrates Kubernetes handling infrastructure scaling, while the ML model handles application-level self-healing."

---

## 📚 Additional Documentation

-   **`DOCKER_COMPOSE_GUIDE.md`** - Docker Compose deployment
-   **`ML_MONITOR_DEPLOYMENT.md`** - ML Monitor deployment options
-   **`ACADEMIC_REQUIREMENTS.md`** - How each requirement is satisfied
-   **`QUICK_START.md`** - Quick reference and troubleshooting
-   **`DEPLOYMENT_COMMANDS.sh`** - Automated Bash script
-   **`DEPLOYMENT_COMMANDS.ps1`** - Automated PowerShell script

---

## 🎯 Quick Command Reference

### **Deploy Everything:**

```bash
# 1. Build and push
docker build -t patient-app:latest .
docker tag patient-app:latest USER/patient-app:latest
docker push USER/patient-app:latest

# 2. Create deployment
kubectl create deployment patient-app --image=USER/patient-app:latest --replicas=2
kubectl set resources deployment patient-app --limits=cpu=500m,memory=512Mi --requests=cpu=100m,memory=128Mi
kubectl expose deployment patient-app --type=LoadBalancer --port=5000 --name=patient-app-service

# 3. Add health probes (use commands from Part 3)

# 4. Setup HPA (use commands from Part 4)
```

### **Clean Up Everything:**

```bash
kubectl delete deployment patient-app
kubectl delete service patient-app-service
kubectl delete hpa patient-app-hpa
docker rmi YOUR_USERNAME/patient-app:latest
```

---

**✅ Your deployment is now complete and production-ready!** 🎉
