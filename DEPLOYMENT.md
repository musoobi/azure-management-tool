# Azure Management Tool - Deployment Guide

## 🐳 Containerized Web Application

This guide shows how to deploy the Azure Management Tool as a containerized web application.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Azure service principal credentials
- Python 3.11+ (for local development)

## 🚀 Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Azure credentials

# Run the web app
python app.py
```

### 2. Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t azure-management-web .
docker run -p 5000:5000 --env-file .env azure-management-web
```

### 3. Production Deployment

#### Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry your-registry --image azure-management-web .

# Deploy to Container Instances
az container create \
  --resource-group your-rg \
  --name azure-management-web \
  --image your-registry.azurecr.io/azure-management-web:latest \
  --dns-name-label azure-management-web \
  --ports 5000 \
  --environment-variables \
    AZURE_TENANT_ID=your-tenant-id \
    AZURE_CLIENT_ID=your-client-id \
    AZURE_CLIENT_SECRET=your-client-secret \
    AZURE_SUBSCRIPTION_ID=your-subscription-id \
    FLASK_SECRET_KEY=your-secret-key
```

#### Azure App Service

```bash
# Deploy to App Service
az webapp config container set \
  --name your-webapp \
  --resource-group your-rg \
  --docker-custom-image-name your-registry.azurecr.io/azure-management-web:latest
```

#### Kubernetes

```bash
# Create Kubernetes deployment
kubectl apply -f k8s-deployment.yaml

# Create service
kubectl apply -f k8s-service.yaml
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_TENANT_ID` | Azure AD tenant ID | Yes |
| `AZURE_CLIENT_ID` | Service principal client ID | Yes |
| `AZURE_CLIENT_SECRET` | Service principal secret | Yes |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | Yes |
| `FLASK_SECRET_KEY` | Flask secret key | Yes |
| `FLASK_DEBUG` | Enable debug mode | No |
| `PORT` | Web server port | No |

### Security Best Practices

1. **Use Azure Key Vault** for production secrets
2. **Enable HTTPS** in production
3. **Add authentication layer** for user access
4. **Use managed identities** when possible
5. **Monitor with Application Insights**

## 📊 Features

- ✅ **Real-time Dashboard**: View all Azure resources
- ✅ **Resource Management**: List and monitor resources
- ✅ **API Endpoints**: RESTful API for integration
- ✅ **Health Monitoring**: Built-in health checks
- ✅ **Container Ready**: Docker and Kubernetes compatible
- ✅ **Scalable**: Can be deployed to any cloud platform

## 🔍 API Endpoints

- `GET /` - Main dashboard
- `GET /api/auth/status` - Authentication status
- `GET /api/dashboard` - Dashboard data
- `GET /api/resources/vms` - Virtual machines
- `GET /api/resources/storage` - Storage accounts
- `GET /api/resources/webapps` - Web apps
- `GET /api/resources/resourcegroups` - Resource groups
- `GET /health` - Health check

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check Azure credentials in .env
   - Verify service principal permissions
   - Check subscription access

2. **Container Won't Start**
   - Check Docker logs: `docker logs container-name`
   - Verify environment variables
   - Check port conflicts

3. **Web App Not Loading**
   - Check if port 5000 is accessible
   - Verify health endpoint: `curl http://localhost:5000/health`
   - Check browser console for errors

### Logs

```bash
# Docker logs
docker-compose logs azure-web-app

# Application logs
docker exec container-name tail -f /app/logs/app.log
```

## 📈 Monitoring

### Health Checks

The application includes built-in health checks:

```bash
curl http://localhost:5000/health
```

### Metrics

Consider adding:
- Azure Application Insights
- Prometheus metrics
- Custom logging

## 🔄 Updates

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Rolling Updates

For production deployments, use rolling updates to minimize downtime.
