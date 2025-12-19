# ML-Based Self-Healing Monitor
# 
# IMPORTANT ARCHITECTURE NOTES:
# ==============================
# 1. This monitor runs OUTSIDE Kubernetes (or as a separate utility container)
# 2. It uses ML to make SELF-HEALING decisions (reset errors, restart containers)
# 3. It does NOT handle pod scaling - that's Kubernetes HPA's responsibility
# 4. Kubernetes HPA scales pods based on CPU/memory metrics
# 5. This ML model focuses on application-level healing actions
#
# SEPARATION OF CONCERNS:
# - Kubernetes HPA: Horizontal scaling (add/remove pods based on load)
# - ML Monitor: Self-healing decisions (fix errors, restart unhealthy instances)

import requests
import time
import json
import subprocess
import sys
import os
from datetime import datetime
from train_brain import HealingBrain  # Import the ML model

# Force unbuffered output for real-time logging in Kubernetes
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

class DoctorMonitorML:
    """
    Enhanced Doctor Monitor that uses ML for healing decisions
    
    Responsibilities:
    - Monitor application health via /health endpoint
    - Use ML model to predict optimal healing actions
    - Trigger soft healing (API-based) or hard healing (container restart)
    
    NOT responsible for:
    - Pod scaling (handled by Kubernetes HPA)
    - Infrastructure-level autoscaling
    """
    
    def __init__(self, patient_url="http://localhost:5000", container_name="patient-app"):
        self.patient_url = patient_url
        self.container_name = container_name
        self.check_interval = 5
        
        # Load the trained ML model
        self.brain = HealingBrain()
        try:
            self.brain.load_model('healing_brain.pkl')
            print("✅ ML model loaded successfully!")
            self.use_ml = True
        except:
            print("⚠️  ML model not found, using rule-based decisions")
            self.use_ml = False
            self.error_threshold = 5
            self.critical_threshold = 10
        
        self.health_history = []
    
    def check_health(self):
        """Same as before - check patient health"""
        try:
            response = requests.get(f"{self.patient_url}/health", timeout=5)
            health_data = response.json()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Health Check:")
            print(f"  Status: {health_data['status']}")
            print(f"  CPU: {health_data['cpu_usage']}%")
            print(f"  Memory: {health_data['memory_usage']}%")
            print(f"  Errors: {health_data['error_count']}")
            print(f"  Uptime: {health_data['uptime']}s")
            sys.stdout.flush()  # Force flush after each health check
            
            return health_data
        except Exception as e:
            print(f"   ❌ Health check failed: {str(e)}")
            sys.stdout.flush()
            return None
    
    def analyze_health_ml(self, health_data):
        """
        Use ML model to decide healing action
        
        Note: This ML prediction is for self-healing decisions only.
        Kubernetes HPA handles pod scaling based on resource utilization.
        """
        if not health_data:
            return None, "No health data available"
        
        # Get ML prediction
        prediction = self.brain.predict_action({
            'cpu_usage': health_data.get('cpu_usage', 0),
            'memory_usage': health_data.get('memory_usage', 0),
            'error_count': health_data.get('error_count', 0),
            'uptime': health_data.get('uptime', 0)
        })
        
        action = prediction['recommended_action']
        confidence = prediction['confidence']
        
        # Map ML actions to our actions
        if action == 'restart_service':
            msg = f"ML PREDICTION: Restart recommended (confidence: {confidence:.2%})"
            print(msg)
            sys.stdout.flush()
            return 'restart_container', msg
        elif action == 'reset_errors':
            msg = f"ML PREDICTION: Reset recommended (confidence: {confidence:.2%})"
            print(msg)
            sys.stdout.flush()
            return 'reset_errors', msg
        else:
            msg = f"ML PREDICTION: No action needed (confidence: {confidence:.2%})"
            print(f"✅ {msg}")
            sys.stdout.flush()
            return None, msg
    
    def analyze_health_rules(self, health_data):
        """
        FALLBACK: Use rule-based decisions if ML not available
        """
        if not health_data:
            return None, "No health data available"
        
        error_count = health_data.get('error_count', 0)
        
        if error_count >= self.critical_threshold:
            return 'restart_container', f"RULE: Error count ({error_count}) >= {self.critical_threshold}"
        elif error_count >= self.error_threshold:
            return 'reset_errors', f"RULE: Error count ({error_count}) >= {self.error_threshold}"
        else:
            return None, "System is healthy"
    
    def analyze_health(self, health_data):
        """
        Decide which analysis method to use
        """
        if self.use_ml:
            return self.analyze_health_ml(health_data)
        else:
            return self.analyze_health_rules(health_data)
    
    # Rest of the methods (trigger_healing, restart_container, monitor)
    # are the same as the original doctor_monitor.py
    
    def trigger_healing(self, reason):
        """Soft healing via API"""
        print(f"\n🔧 SOFT HEALING TRIGGERED: {reason}")
        sys.stdout.flush()
        
        try:
            response = requests.post(
                f"{self.patient_url}/heal",
                json={"action": "reset_errors"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Healing successful:")
                print(f"  Previous errors: {result['previous_error_count']}")
                sys.stdout.flush()
                return True
            else:
                print(f"   ⚠️ Healing failed with status: {response.status_code}")
                sys.stdout.flush()
                return False
        except Exception as e:
            print(f"   ❌ Healing request failed: {str(e)}")
            sys.stdout.flush()
            return False
    
    def restart_container(self, reason):
        """
        Hard healing - restart container/pod
        
        Detects environment and uses appropriate restart method:
        - Kubernetes: Deletes pod (deployment recreates it)
        - Docker: Restarts container
        """
        print(f"\n🔴 CRITICAL HEALING: RESTARTING CONTAINER/POD")
        print(f"   Reason: {reason}")
        sys.stdout.flush()  # Force flush
        
        # Check if running in Kubernetes
        if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount'):
            print(f"   📦 Detected Kubernetes environment")
            sys.stdout.flush()
            
            try:
                # Get current pod name from hostname
                pod_name = os.environ.get('HOSTNAME', 'unknown')
                namespace = os.environ.get('NAMESPACE', 'default')
                
                # Use kubectl to delete a patient-app pod (deployment will recreate it)
                result = subprocess.run(
                    ['kubectl', 'delete', 'pod', '-l', 'app=patient-app', '--field-selector=status.phase=Running', '--timeout=10s', '-n', namespace],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Patient app pod deleted - Deployment will recreate it")
                    sys.stdout.flush()
                    time.sleep(3)
                    return True
                else:
                    print(f"   ⚠️ kubectl failed: {result.stderr}")
                    sys.stdout.flush()
                    return False
                    
            except Exception as e:
                print(f"   ❌ Kubernetes restart failed: {str(e)}")
                sys.stdout.flush()
                return False
        else:
            # Running in Docker (non-Kubernetes)
            print(f"   🐳 Detected Docker environment")
            sys.stdout.flush()
            
            try:
                result = subprocess.run(
                    ['docker', 'restart', self.container_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Container restarted successfully")
                    sys.stdout.flush()
                    time.sleep(3)
                    return True
                else:
                    print(f"   ⚠️ Docker restart failed: {result.stderr}")
                    sys.stdout.flush()
                    return False
            except Exception as e:
                print(f"   ❌ Docker restart failed: {str(e)}")
                sys.stdout.flush()
                return False
    
    def monitor(self):
        """Main monitoring loop"""
        print("🩺 Doctor Monitor Starting...")
        print(f"👀 Watching patient app at: {self.patient_url}")
        print(f"🐳 Docker container: {self.container_name}")
        
        if self.use_ml:
            print(f"🧠 Using ML model for decisions")
        else:
            print(f"📏 Using rule-based decisions")
            print(f"⚠️  Error threshold (soft): {self.error_threshold}")
            print(f"🔴 Critical threshold (restart): {self.critical_threshold}")
        
        print("\n" + "="*50)
        
        while True:
            try:
                health_data = self.check_health()
                healing_action, reason = self.analyze_health(health_data)
                
                if healing_action == 'restart_container':
                    self.restart_container(reason)
                elif healing_action == 'reset_errors':
                    self.trigger_healing(reason)
                else:
                    print(f"✅ {reason}")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n\n👋 Doctor Monitor shutting down...")
                break

if __name__ == '__main__':
    import sys
    
    patient_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    container_name = sys.argv[2] if len(sys.argv) > 2 else "patient-app"
    
    monitor = DoctorMonitorML(patient_url, container_name)
    monitor.monitor()
