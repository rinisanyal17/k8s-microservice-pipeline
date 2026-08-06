<div align="center">

# k8s-microservice-pipeline
### Production-Ready End-to-End Kubernetes Microservice CI/CD Deployment Pipeline

<p>
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Nginx_Ingress-009639?style=for-the-badge&logo=nginx&logoColor=white" />
  <img src="https://img.shields.io/badge/Minikube-2088FF?style=for-the-badge&logo=minikube&logoColor=white" />
</p>

</div>

---

## 📌 Overview

This repository contains a cloud-native, automated end-to-end Kubernetes microservice pipeline. It demonstrates industry best practices for continuous integration, local container image delivery, declarative Kubernetes deployment, ingress traffic management, zero-downtime rolling updates, and health monitoring.

Whenever a commit is pushed to the `main` branch, an automated **GitHub Actions Self-Hosted Runner** triggers a full CI/CD workflow: building the Docker image, transferring it to Minikube, deploying Kubernetes manifests, and verifying health checks.

---

## 🏗️ End-to-End CI/CD Architecture

The architecture below illustrates the path from developer code commit to automated execution and live cluster routing:

```mermaid
flowchart TD
    subgraph Developer_Workspace["1. Source Code Management"]
        Dev["Developer"] -->|git push origin main| GitHub["GitHub Repository"]
    end

    subgraph CI_Pipeline["2. Continuous Integration (GitHub Actions)"]
        GitHub -->|Webhook Trigger| Runner["WSL Self-Hosted Runner"]
        
        subgraph Workflow_Steps["Pipeline Stages"]
            Checkout["1. Checkout Code"] --> BuildDocker["2. Docker Build"]
            BuildDocker --> LoadMinikube["3. Load Image to Minikube"]
        end

        Runner --> Workflow_Steps
    end

    subgraph CD_Deployment["3. Continuous Deployment"]
        LoadMinikube --> ApplyManifests["4. kubectl apply -f k8s/"]
        ApplyManifests --> RolloutCheck["5. Verify Rollout Status"]
        RolloutCheck --> HealthCheck["6. Smoke Test (/healthz)"]
    end

    subgraph K8s_Cluster["4. Kubernetes Runtime (Minikube)"]
        HealthCheck --> Ingress["Nginx Ingress Router<br/><code>[http://myapp.local](http://myapp.local)</code>"]
        Ingress --> Service["ClusterIP Service (Port 5000)"]
        Service --> Pod1["Pod 1 (1/1 Ready)"]
        Service --> Pod2["Pod 2 (1/1 Ready)"]
    end

    classDef dev fill:#1e293b,stroke:#38bdf8,color:#f8fafc;
    classDef ci fill:#0284c7,stroke:#38bdf8,color:#fff;
    classDef cd fill:#0f172a,stroke:#22c55e,color:#4ade80;
    
    class Dev,GitHub dev;
    class Runner,Checkout,BuildDocker,LoadMinikube ci;
    class ApplyManifests,RolloutCheck,HealthCheck,Ingress,Service,Pod1,Pod2 cd;
```

---

## 📁 Repository Structure

```text
k8s-microservice-pipeline/
├── .github/
│   └── workflows/
│       └── ci-cd.yml    # GitHub Actions automated pipeline definition
├── app.py               # Python/Flask microservice with / & /healthz endpoints
├── requirements.txt     # Dependency definitions (Flask, gunicorn)
├── Dockerfile           # Optimized single-stage runtime image build
├── .dockerignore        # Excludes virtual environments, pycache, and git assets
└── k8s/
    ├── configMap.yml    # Application environment variables configuration
    ├── deployment.yml   # Workload definition (2 Replicas, Probes, Resource Limits)
    ├── service.yml      # Internal ClusterIP network exposure on Port 5000
    └── ingress.yml      # Path-based routing rules for host myapp.local
```

---

## 🚀 Getting Started Guide

### 1. Register GitHub Self-Hosted Runner (WSL)
```bash
# Register runner daemon under repo Settings -> Actions -> Runners
mkdir actions-runner && cd actions-runner
tar xzf ./actions-runner-linux-x64-*.tar.gz
./config.sh --url [https://github.com/](https://github.com/)<USER>/k8s-microservice-pipeline --token <TOKEN>

# Start background daemon service
sudo ./svc.sh install
sudo ./svc.sh start
```

### 2. Enable Local Networking & Ingress
```bash
# Enable Ingress controller
minikube addons enable ingress

# Start Minikube Tunnel (Keep open in a separate terminal tab)
minikube tunnel

# Map host entry in /etc/hosts or C:\Windows\System32\drivers\etc\hosts
127.0.0.1   myapp.local
```

### 3. Trigger Automated CI/CD
Simply commit and push any changes to trigger the full automated build and deployment:
```bash
git add .
git commit -m "feat: trigger automated pipeline build"
git push origin main
```

---

## 🛠️ Core Engineering Highlights

| Feature | Implementation Details |
| :--- | :--- |
| **Full Pipeline Automation** | End-to-end CI/CD powered by GitHub Actions targeting local Minikube via WSL self-hosted agent. |
| **Zero-Downtime Rolling Updates** | K8s rolling deployment strategy with readiness/liveness health checks ensures uninterrupted traffic. |
| **Resilient Traffic Management** | Nginx Ingress host routing (`myapp.local`) with ClusterIP service load balancing across multiple active pods. |
| **Automated Testing & Validation** | Post-deployment smoke testing (`/healthz` endpoint query) integrated directly into the CI pipeline. |

---

<div align="center">

<sub><b>k8s-microservice-pipeline</b> — Maintained by <b>Rini Sanyal</b> | Senior Embedded & Platform Engineer</sub>

</div>
# Pipeline Verified
