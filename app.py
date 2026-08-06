import os
from flask import Flask, jsonify

app = Flask(__name__)

# Retrieve environment variables passed by OS / Kubernetes ConfigMap
PORT = int(os.environ.get("PORT", 5000))
APP_ENV = os.environ.get("APP_ENV", "local")

# Route 1: Main Application Endpoint (/)
@app.route("/")
def home():
    pod_name = os.environ.get("HOSTNAME", "localhost")
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
        <h1 style="color: #2c3e50;">🚀 Hello from Automated CI/CD Pipeline!!!!</h1>
        <p>Environment: <strong>{APP_ENV}</strong></p>
        <p>Pod Hostname: <strong>{pod_name}</strong></p>
      </body>
    </html>
    """

# Route 2: Health Check Endpoint for Kubernetes Liveness/Readiness Probes (/healthz)
@app.route("/healthz")
def healthz():
    return jsonify({
        "status": "UP",
        "environment": APP_ENV,
        "service": "k8s-microservice-pipeline"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
# Trigger test
