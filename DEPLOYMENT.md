# Deployment Guide

## Table of Contents
1. [Docker Compose Deployment](#docker-compose-deployment)
2. [AWS Deployment](#aws-deployment)
3. [Google Cloud Deployment](#google-cloud-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Performance Tuning](#performance-tuning)

---

## Docker Compose Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd LangTrans
```

2. **Create Environment Files**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. **Start Services**
```bash
docker-compose up --build
```

4. **Verify Services**
```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f

# Test API
curl http://localhost:8000/api/health
```

### Configuration
Edit `backend/.env` for production:
```env
CORS_ORIGINS=https://yourdomain.com
DEBUG=false
```

### Stop Services
```bash
docker-compose down

# Remove volumes (models cache)
docker-compose down -v
```

---

## AWS Deployment

### Option 1: Elastic Container Service (ECS) Fargate

1. **Create ECR Repositories**
```bash
aws ecr create-repository --repository-name langtrans-backend --region us-east-1
aws ecr create-repository --repository-name langtrans-frontend --region us-east-1
```

2. **Build and Push Images**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Backend
docker build -t langtrans-backend:latest backend/
docker tag langtrans-backend:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/langtrans-backend:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/langtrans-backend:latest

# Frontend
docker build -t langtrans-frontend:latest frontend/
docker tag langtrans-frontend:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/langtrans-frontend:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/langtrans-frontend:latest
```

3. **Create ECS Cluster**
```bash
aws ecs create-cluster --cluster-name langtrans-cluster --region us-east-1
```

4. **Create Task Definitions**
See `aws-task-definition.json` file

5. **Deploy Services**
```bash
aws ecs create-service --cluster langtrans-cluster --service-name langtrans-backend --task-definition langtrans-backend:1 --desired-count 2 --launch-type FARGATE --region us-east-1
```

### Option 2: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init langtrans --platform "Docker" --region us-east-1

# Create environment
eb create langtrans-env

# Deploy
eb deploy

# View logs
eb logs

# Open in browser
eb open
```

### Option 3: AWS Lightsail

1. Create container service
2. Push Docker images to ECR
3. Configure deployment

---

## Google Cloud Deployment

### Option 1: Cloud Run

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build Backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/langtrans-backend backend/

# Deploy Backend
gcloud run deploy langtrans-backend \
  --image gcr.io/YOUR_PROJECT_ID/langtrans-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars CORS_ORIGINS=https://YOUR_FRONTEND_URL \
  --memory 4Gb \
  --cpu 2

# Build Frontend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/langtrans-frontend frontend/

# Deploy Frontend
gcloud run deploy langtrans-frontend \
  --image gcr.io/YOUR_PROJECT_ID/langtrans-frontend \
  --platform managed \
  --region us-central1 \
  --set-env-vars VITE_API_URL=https://YOUR_BACKEND_URL/api
```

### Option 2: Google Kubernetes Engine (GKE)

```bash
# Create cluster
gcloud container clusters create langtrans-cluster

# Create deployments
kubectl apply -f gke-deployment.yaml

# Check status
kubectl get pods
kubectl get services
```

---

## Kubernetes Deployment

### Prerequisites
- kubectl configured
- Kubernetes cluster (local, GKE, AKS, EKS)

### Steps

1. **Create Namespace**
```bash
kubectl create namespace langtrans
```

2. **Create Secrets**
```bash
kubectl create secret generic langtrans-config \
  --from-literal=cors-origins="https://yourdomain.com" \
  -n langtrans
```

3. **Deploy Backend**
```bash
kubectl apply -f k8s/backend-deployment.yaml -n langtrans
kubectl apply -f k8s/backend-service.yaml -n langtrans
```

4. **Deploy Frontend**
```bash
kubectl apply -f k8s/frontend-deployment.yaml -n langtrans
kubectl apply -f k8s/frontend-service.yaml -n langtrans
```

5. **Check Status**
```bash
kubectl get deployments -n langtrans
kubectl get pods -n langtrans
kubectl get services -n langtrans
```

6. **Scale Services**
```bash
kubectl scale deployment langtrans-backend --replicas=3 -n langtrans
```

---

## Azure Deployment

### Option 1: Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name langtrans-rg --location eastus

# Create container registry
az acr create --resource-group langtrans-rg --name langtransacr --sku Basic

# Build and push
az acr build --registry langtransacr --image langtrans-backend:latest ./backend
az acr build --registry langtransacr --image langtrans-frontend:latest ./frontend

# Deploy
az container create \
  --resource-group langtrans-rg \
  --name langtrans-backend \
  --image langtransacr.azurecr.io/langtrans-backend:latest \
  --cpu 2 --memory 4 \
  --ports 8000 \
  --registry-login-server langtransacr.azurecr.io
```

### Option 2: Azure App Service

```bash
# Create App Service Plan
az appservice plan create --name langtrans-plan --resource-group langtrans-rg --sku B2 --is-linux

# Create Container Web App
az webapp create --resource-group langtrans-rg --plan langtrans-plan --name langtrans-backend

# Configure deployment
az webapp config container set --name langtrans-backend --resource-group langtrans-rg \
  --docker-custom-image-name langtransacr.azurecr.io/langtrans-backend:latest
```

---

## Performance Tuning

### Backend Optimization

**1. Use GPU**
- Ensure CUDA 11.8+ and cuDNN installed
- Set `CUDA_VISIBLE_DEVICES=0` to use specific GPU

**2. Model Memory Optimization**
```python
import torch
# Use mixed precision
model.half()  # FP16
```

**3. Enable Async Workers**
```bash
uvicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**4. Caching**
- Implement response caching for common translations
- Use Redis for distributed caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

cache = RedisBackend("{redis_url}")
```

### Frontend Optimization

**1. Build for Production**
```bash
npm run build
```

**2. Enable Compression**
```nginx
gzip on;
gzip_types application/json text/css;
```

**3. CDN Integration**
```bash
# Serve from CloudFront, Cloudflare, etc.
```

### Infrastructure Scaling

**Horizontal Scaling:**
```bash
# Docker Compose
docker-compose up --scale backend=3
```

**Vertical Scaling:**
- Increase CPU/Memory in container configuration
- Use larger machine types

**Load Balancing:**
```nginx
upstream backend {
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}
```

---

## Monitoring & Logging

### Cloud Monitoring

**Google Cloud Monitoring:**
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Create alerts
gcloud alpha monitoring alerts create
```

**AWS CloudWatch:**
```bash
# View logs
aws logs tail /ecs/langtrans-backend --follow

# Create alarms
aws cloudwatch put-metric-alarm --alarm-name HighCPU ...
```

### Application Logging

Enable comprehensive logging:
```env
DEBUG=true
LOG_LEVEL=INFO
```

View logs:
```bash
docker-compose logs -f backend
kubectl logs deployment/langtrans-backend -f
```

---

## Backup & Recovery

### Model Cache Backup
```bash
# Backup cache volumes
docker-compose exec backend tar -czf /tmp/models.tar.gz ~/.cache/huggingface

# Restore
docker-compose exec backend tar -xzf /tmp/models.tar.gz -C ~/.cache/
```

---

## Security

1. **HTTPS/TLS**
   - Use Let's Encrypt with Certbot
   - Configure reverse proxy (Nginx, Traefik)

2. **API Authentication**
   - Add API Key validation
   - Implement rate limiting

3. **Environment Variables**
   - Use AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager

4. **Docker Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Run as non-root user

---

## Cost Optimization

- Use spot instances for non-critical workloads
- Auto-scale based on demand
- Cache model downloads
- Use CDN for static assets
- Implement request rate limiting

---

## Troubleshooting Deployment Issues

| Issue | Solution |
|-------|----------|
| Models not downloading | Pre-download and cache models |
| OOM errors | Use smaller model or more memory |
| Slow cold start | Pre-load models in init container |
| CORS errors | Update CORS_ORIGINS in config |
| Port conflicts | Use different port in config |

---

For more details, see main README.md
