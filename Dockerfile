# Production-ready Dockerfile for Patient App
# This Dockerfile satisfies Academic Requirement 2: Containerization

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/app.py .

# Copy ML model (used by external monitoring service, not exposed via API)
COPY app/healing_brain.pkl .

# Expose port 5000
EXPOSE 5000

# Health check for Docker
# Note: Kubernetes will use /healthz endpoint for liveness/readiness probes
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/healthz || exit 1

# Run with gunicorn for production
# Logs are sent to stdout for kubectl logs visibility
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", \
  "--access-logfile", "-", \
  "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"", \
  "app:app"]
