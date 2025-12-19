# 🔄 Redeploy ML Monitor (Fixed Version)

## 🐛 Issues Fixed:

1. ✅ **Real-time logs** - Added unbuffered output (`python -u` and `sys.stdout.flush()`)
2. ✅ **Pod restart in Kubernetes** - Added kubectl support and RBAC permissions
3. ✅ **Environment detection** - Automatically detects Docker vs Kubernetes
4. ✅ **Better error handling** - Added exception handling and error messages

---

## 🚀 Redeploy Steps:

### **Step 1: Create RBAC Permissions Using kubectl Commands**

The ML Monitor needs permission to delete pods for healing. Create RBAC resources using kubectl:

```bash
# Create ServiceAccount
kubectl create serviceaccount ml-monitor-sa

# Create Role (allows pod deletion)
kubectl create role ml-monitor-role \
  --verb=get,list,delete \
  --resource=pods

# Create RoleBinding (bind role to service account)
kubectl create rolebinding ml-monitor-rolebinding \
  --role=ml-monitor-role \
  --serviceaccount=default:ml-monitor-sa
```

**Windows PowerShell:**

```powershell
# Create ServiceAccount
kubectl create serviceaccount ml-monitor-sa

# Create Role
kubectl create role ml-monitor-role `
  --verb=get,list,delete `
  --resource=pods

# Create RoleBinding
kubectl create rolebinding ml-monitor-rolebinding `
  --role=ml-monitor-role `
  --serviceaccount=default:ml-monitor-sa
```

This creates:

-   `ml-monitor-sa` ServiceAccount
-   `ml-monitor-role` Role (can get, list, delete pods)
-   `ml-monitor-rolebinding` RoleBinding

### **Step 2: Rebuild and Push ML Monitor Image**

```bash
# Rebuild with fixes
docker build -t ml-monitor:latest -f Dockerfile.monitor .

# Tag for Docker Hub
docker tag ml-monitor:latest 3morii74/ml-monitor:latest

# Push to Docker Hub
docker push 3morii74/ml-monitor:latest
```

### **Step 3: Update ML Monitor Deployment**

Delete and recreate the deployment with the new ServiceAccount:

```bash
# Delete old deployment
kubectl delete deployment ml-monitor

# Create new deployment with ServiceAccount
kubectl create deployment ml-monitor \
  --image=3morii74/ml-monitor:latest \
  --replicas=1

# Set Patient App URL
kubectl set env deployment/ml-monitor \
  PATIENT_URL=http://patient-app-service:5000

# IMPORTANT: Set the ServiceAccount
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa
```

**Windows PowerShell:**

```powershell
# Delete old deployment
kubectl delete deployment ml-monitor

# Create new deployment
kubectl create deployment ml-monitor `
  --image=3morii74/ml-monitor:latest `
  --replicas=1

# Set environment variable
kubectl set env deployment/ml-monitor `
  PATIENT_URL=http://patient-app-service:5000

# Set ServiceAccount
kubectl set serviceaccount deployment ml-monitor ml-monitor-sa
```

### **Step 4: Verify Real-Time Logs**

```bash
# Watch logs (should appear every 5 seconds now!)
kubectl logs -f deployment/ml-monitor
```

**Expected output (every 5 seconds):**

```
[2025-12-18 14:30:00] Health Check:
  Status: healthy
  CPU: 45%
  Memory: 60%
  Errors: 0
  Uptime: 300s
✅ ML PREDICTION: No action needed (confidence: 88.95%)

[2025-12-18 14:30:05] Health Check:
  Status: healthy
  CPU: 50%
  ...
```

---

## 🧪 Test Pod Restart:

### **Step 1: Simulate Errors**

```bash
# Generate errors to trigger pod restart
for i in {1..30}; do
  curl http://localhost:5000/simulate-error
  sleep 1
done
```

**Windows PowerShell:**

```powershell
for ($i=0; $i -lt 30; $i++) {
    Invoke-WebRequest -Uri "http://localhost:5000/simulate-error" -UseBasicParsing | Out-Null
    Start-Sleep -Seconds 1
}
```

### **Step 2: Watch ML Monitor Detect and Heal**

```bash
# Terminal 1: Watch ML Monitor logs
kubectl logs -f deployment/ml-monitor

# Terminal 2: Watch pods being restarted
kubectl get pods -l app=patient-app --watch
```

**Expected sequence:**

```
[timestamp] Health Check:
  Status: degraded
  CPU: 76%
  Memory: 76%
  Errors: 20
  Uptime: 2761s

🔴 CRITICAL HEALING: RESTARTING CONTAINER/POD
   Reason: ML PREDICTION: Restart recommended (confidence: 100.00%)
   📦 Detected Kubernetes environment
   ✅ Patient app pod deleted - Deployment will recreate it

[timestamp] Health Check:
  Status: healthy
  CPU: 10%
  Memory: 20%
  Errors: 0
  Uptime: 5s
✅ ML PREDICTION: No action needed (confidence: 95%)
```

---

## 🔍 What Changed:

### **1. Real-Time Logging**

**Before:**

```python
# Logs buffered - appeared every 3 minutes
print("Health Check...")
```

**After:**

```python
# Unbuffered - logs appear immediately
print("Health Check...")
sys.stdout.flush()  # Force immediate output
```

Plus added `-u` flag in Dockerfile:

```dockerfile
CMD python -u doctor_monitor_ml.py $PATIENT_URL
```

### **2. Kubernetes Pod Restart**

**Before:**

```python
# Only worked with Docker
subprocess.run(['docker', 'restart', self.container_name])
```

**After:**

```python
# Detects environment automatically
if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount'):
    # Kubernetes: Delete pod (deployment recreates it)
    subprocess.run(['kubectl', 'delete', 'pod', '-l', 'app=patient-app', ...])
else:
    # Docker: Restart container
    subprocess.run(['docker', 'restart', self.container_name])
```

### **3. RBAC Permissions**

ML Monitor now has a ServiceAccount with permissions to:

-   ✅ List pods
-   ✅ Get pod details
-   ✅ Delete pods (for healing)

---

## ✅ Verification Checklist:

```bash
# 1. Check RBAC is applied
kubectl get serviceaccount ml-monitor-sa
kubectl get role ml-monitor-role
kubectl get rolebinding ml-monitor-rolebinding

# 2. Check ML Monitor is using ServiceAccount
kubectl get deployment ml-monitor -o yaml | grep serviceAccount

# 3. Check logs appear every 5 seconds
kubectl logs -f deployment/ml-monitor

# 4. Check ML Monitor can access kubectl
kubectl exec deployment/ml-monitor -- kubectl version --client

# 5. Generate errors and watch healing
curl http://localhost:5000/simulate-error
kubectl logs -f deployment/ml-monitor
```

---

## 📊 Complete System Test:

### **Test Scenario: High Error Count → Pod Restart**

```bash
# Terminal 1: Watch ML Monitor
kubectl logs -f deployment/ml-monitor

# Terminal 2: Watch Patient App pods
kubectl get pods -l app=patient-app --watch

# Terminal 3: Generate 30 errors
for i in {1..30}; do curl http://localhost:5000/simulate-error; sleep 1; done
```

**What should happen:**

1. Errors accumulate (0 → 5 → 10 → 15 → 20)
2. ML Monitor detects critical state (20+ errors)
3. ML predicts restart needed (100% confidence)
4. ML Monitor deletes one patient-app pod
5. Kubernetes Deployment recreates the pod automatically
6. New pod starts with 0 errors
7. System returns to healthy state

---

## 🎯 Summary:

| Issue              | Before      | After             |
| ------------------ | ----------- | ----------------- |
| **Log Delay**      | 3 minutes   | Real-time (5 sec) |
| **Pod Restart**    | ❌ Fails    | ✅ Works          |
| **Environment**    | Docker only | Docker + K8s      |
| **Permissions**    | None        | RBAC configured   |
| **Error Handling** | Silent      | Clear messages    |

---

## 📤 Export YAML Files (Optional - for GitHub)

After creating resources with kubectl commands, you can export them:

```bash
# Export ServiceAccount
kubectl get serviceaccount ml-monitor-sa -o yaml > kubernetes-ml-monitor-sa.yaml

# Export Role
kubectl get role ml-monitor-role -o yaml > kubernetes-ml-monitor-role.yaml

# Export RoleBinding
kubectl get rolebinding ml-monitor-rolebinding -o yaml > kubernetes-ml-monitor-rolebinding.yaml

# Export ML Monitor Deployment
kubectl get deployment ml-monitor -o yaml > kubernetes-ml-monitor-deployment.yaml
```

---

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
