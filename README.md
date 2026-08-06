<div align="center">

# k8s-microservice-pipeline
### Production-Ready End-to-End Kubernetes Microservice Deployment Pipeline

<p>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Nginx_Ingress-009639?style=for-the-badge&logo=nginx&logoColor=white" />
  <img src="https://img.shields.io/badge/Minikube-2088FF?style=for-the-badge&logo=minikube&logoColor=white" />
</p>

</div>

---

## 📌 Overview

This repository contains a cloud-native, end-to-end Kubernetes microservice pipeline demonstrating best practices for containerization, declarative Kubernetes configuration, ingress routing, zero-downtime rolling updates, and health monitoring.

The core workload is a high-performance Python/Flask application encapsulated in a lightweight Docker image (`python:3.10-slim`) and orchestrated on a local Kubernetes cluster using Minikube and Nginx Ingress.

---

## 🏗️ Architecture & Traffic Flow

The architecture below illustrates the path of an external client request passing through local network tunnels, host resolution, Nginx Ingress routing, ClusterIP service abstraction, and load balancing across active replica pods.

```mermaid
flowchart LR
    Client["Client / Browser<br/><code>[http://myapp.local](http://myapp.local)</code>"] 
    
    subgraph Cluster["Kubernetes Cluster (Minikube)"]
        direction LR
        Ingress["Nginx Ingress<br/><i>Ingress Controller</i><br/>(Host Routing)"]
        Service["K8s Service<br/><i>ClusterIP: 5000</i><br/>Load Balancer"]
        
        subgraph Pods["Replica Pods"]
            Pod1["Pod 1 (1/1 Ready)<br/>Flask App (Port 5000)<br/><code>Env: APP_ENV</code>"]
            Pod2["Pod 2 (1/1 Ready)<br/>Flask App (Port 5000)<br/><code>Env: APP_ENV</code>"]
        end
        
        ConfigMap["ConfigMap<br/><code>APP_ENV: development</code>"]
    end

    Client -->|Host/Port 80| Ingress
    Ingress -->|ClusterIP| Service
    Service -->|Load Balance| Pod1
    Service -->|Load Balance| Pod2
    ConfigMap -.-|Environment Injection| Pod1
    ConfigMap -.-|Environment Injection| Pod2

    classDef default fill:#1e293b,stroke:#334155,color:#e2e8f0;
    classDef ingress fill:#0284c7,stroke:#38bdf8,color:#fff;
    classDef pod fill:#0f172a,stroke:#22c55e,color:#4ade80;
    classDef config fill:#1e293b,stroke:#a855f7,color:#c084fc;
    
    class Ingress ingress;
    class Pod1,Pod2 pod;
    class ConfigMap config;
`` ``` ``
📁 Repository Structure
Plaintext
k8s-microservice-pipeline/
├── app.py               # Python/Flask microservice with / & /healthz endpoints
├── requirements.txt     # Dependency definitions (Flask, gunicorn)
├── Dockerfile           # Optimized single-stage runtime image build
├── .dockerignore        # Excludes virtual environments, pycache, and git assets
└── k8s/
    ├── configMap.yml    # Application environment variables configuration
    ├── deployment.yml   # Workload definition (2 Replicas, Probes, Resource Limits)
    ├── service.yml      # Internal ClusterIP network exposure on Port 5000
    └── ingress.yml      # Path-based routing rules for host myapp.local

🚀 Getting Started & Execution Guide1. Local Container Build & Cache InjectionBash# Build application image locally
docker build -t k8s-microservice-pipeline:v1 .

# Transfer image directly into Minikube node storage
minikube image load k8s-microservice-pipeline:v1
2. Declarative DeploymentBash# Apply all Kubernetes manifests simultaneously
kubectl apply -f k8s/

# Monitor rollout status
kubectl get pods -w
3. Ingress Tunneling & Local RoutingBash# Enable Nginx Ingress Controller
minikube addons enable ingress

# Start Minikube Tunnel (Keep active in separate terminal)
minikube tunnel

# Map host entry in /etc/hosts or C:\Windows\System32\drivers\etc\hosts
127.0.0.1   myapp.local
4. End-to-End VerificationBash# Test main web endpoint
curl [http://myapp.local](http://myapp.local)

# Test Liveness/Readiness health probes
curl [http://myapp.local/healthz](http://myapp.local/healthz)
🛠️ Core Engineering HighlightsFeatureImplementation DetailsZero-Downtime DeploymentRolling update strategy configured via Deployment spec with readiness/liveness health checks.  Isolated BuildCompliant with PEP 668 environment handling; isolated host builds via virtualenv and clean Docker layer caching.  Resilient NetworkingPath-based HTTP routing using Nginx Ingress and ClusterIP service decouples backend pods from external endpoints[cite: 1, 2].Health & ObservabilityAutomated pod lifecycle checks (HTTP GET /healthz) running periodically to ensure traffic is only served to healthy containers[cite: 1, 2].k8s-microservice-pipeline — Maintained by Rini Sanyal | Senior Embedded & Platform Engineer
