from flask import Flask, jsonify, request
import random
import time
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log all requests
@app.before_request
def log_request():
    logger.info(f'{request.method} {request.path} - {request.remote_addr}')

@app.after_request
def log_response(response):
    logger.info(f'{request.method} {request.path} - {response.status_code}')
    return response

# Simulated health metrics
health_status = {
    "status": "healthy",
    "cpu_usage": 0,
    "memory_usage": 0,
    "error_count": 0,
    "uptime": 0
}

start_time = time.time()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Patient App - Self Healing System",
        "status": "running",
        "endpoints": [
            "/healthz - Kubernetes health probe (liveness/readiness)",
            "/health - Detailed health status for ML monitoring",
            "/metrics - Get system metrics",
            "/simulate-error - Trigger an error",
            "/heal - Trigger self-healing"
        ]
    })

@app.route('/healthz')
def healthz():
    """
    Kubernetes health probe endpoint (liveness & readiness)
    Lightweight check - returns 200 if app is alive
    Used by Kubernetes to determine pod health and restart if needed
    """
    return jsonify({"status": "ok"}), 200

@app.route('/health')
def health():
    """
    Detailed health check endpoint for ML-based monitoring
    Used by DoctorMonitorML for self-healing decisions
    Note: Kubernetes handles pod scaling via HPA based on CPU/memory
          This endpoint is for ML-driven healing decisions only
    """
    health_status["uptime"] = int(time.time() - start_time)
    health_status["cpu_usage"] = random.randint(10, 90)
    health_status["memory_usage"] = random.randint(20, 80)
    
    # Simulate degraded health if error count is high
    if health_status["error_count"] > 5:
        health_status["status"] = "degraded"
    elif health_status["error_count"] > 10:
        health_status["status"] = "critical"
    else:
        health_status["status"] = "healthy"
    
    return jsonify(health_status)

@app.route('/metrics')
def metrics():
    """Get detailed metrics"""
    return jsonify({
        "cpu_usage": random.randint(10, 90),
        "memory_usage": random.randint(20, 80),
        "disk_usage": random.randint(30, 70),
        "network_latency": random.randint(10, 100),
        "active_connections": random.randint(1, 50),
        "error_count": health_status["error_count"],
        "uptime_seconds": int(time.time() - start_time)
    })

@app.route('/simulate-error')
def simulate_error():
    """Simulate an error to test self-healing"""
    health_status["error_count"] += 1
    
    error_types = [
        "Database connection timeout",
        "Memory leak detected",
        "High CPU usage",
        "Network connectivity issue",
        "Service dependency failure"
    ]
    
    error = random.choice(error_types)
    
    return jsonify({
        "error": error,
        "error_count": health_status["error_count"],
        "status": "error_logged",
        "message": "Error simulated. Monitor will detect and attempt healing."
    }), 500

@app.route('/heal', methods=['POST'])
def heal():
    """Trigger self-healing mechanism"""
    healing_action = request.json.get('action', 'reset_errors') if request.json else 'reset_errors'
    
    if healing_action == 'reset_errors':
        old_count = health_status["error_count"]
        health_status["error_count"] = 0
        health_status["status"] = "healthy"
        
        return jsonify({
            "message": "Self-healing completed",
            "action": "Errors reset",
            "previous_error_count": old_count,
            "current_status": "healthy"
        })
    
    elif healing_action == 'restart_service':
        return jsonify({
            "message": "Service restart initiated",
            "action": "restart_service",
            "status": "healing"
        })
    
    else:
        return jsonify({
            "message": "Unknown healing action",
            "action": healing_action
        }), 400

@app.route('/data')
def get_data():
    """Simulate data retrieval"""
    # Randomly fail to simulate issues
    if random.random() < 0.2:  # 20% chance of failure
        health_status["error_count"] += 1
        return jsonify({"error": "Data retrieval failed"}), 500
    
    return jsonify({
        "data": [
            {"id": i, "value": random.randint(1, 100)}
            for i in range(10)
        ],
        "timestamp": time.time()
    })

if __name__ == '__main__':
    print("🏥 Patient App Starting...")
    print("🔧 Self-Healing System Active")
    print("📊 Monitoring endpoints available")
    app.run(host='0.0.0.0', port=5000, debug=False)
