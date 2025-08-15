# 🚀 Azure Virtual Desktop (AVD) Deployment Guide
## Optimized for Azure Free Tier

### 📋 Prerequisites
- Azure subscription (Free tier works)
- Azure CLI installed
- Python 3.8+ with required packages

### �� Deployment Options

#### Option 1: Python Script Deployment (Recommended)
```bash
# Install AVD dependency
pip install azure-mgmt-desktopvirtualization>=1.0.0

# Run deployment
python deploy_avd.py --session-hosts 1 --location eastus
```

#### Option 2: ARM Template Deployment
```bash
# Deploy using ARM template
az deployment group create \
    --resource-group avd-rg \
    --template-file avd_arm_template.json \
    --parameters location=eastus
```

#### Option 3: Bash Script Deployment
```bash
# Make script executable
chmod +x deploy_avd_vms.sh

# Run deployment
./deploy_avd_vms.sh
```

### 💰 Cost Optimization for Free Tier

#### VM Sizes (Free Tier Friendly)
- **Standard_B1s**: 1 vCPU, 1 GB RAM - $0.0104/hour
- **Standard_B1ms**: 1 vCPU, 2 GB RAM - $0.0208/hour
- **Standard_B2s**: 2 vCPU, 4 GB RAM - $0.0416/hour

#### Recommended Configuration
- **Session Hosts**: 1-2 VMs
- **VM Size**: Standard_B1s or Standard_B1ms
- **Location**: eastus (good free tier support)
- **Storage**: Standard HDD (cheaper)

### 🔧 Post-Deployment Steps

#### 1. Install AVD Agent
```powershell
# On session host VM
# Download and install AVD agent
# Configure host pool registration
```

#### 2. Configure User Access
- Add users to AVD application group
- Configure workspace access
- Test client connectivity

#### 3. Monitor Costs
- Set up cost alerts
- Monitor usage in Azure portal
- Optimize based on usage patterns

### 🚨 Important Notes

#### Free Tier Limitations
- **VM Hours**: Limited per month
- **Storage**: Limited GB per month
- **Network**: Limited egress per month
- **Monitor**: Basic monitoring only

#### Security Considerations
- Change default passwords
- Configure network security groups
- Enable Azure Security Center
- Regular security updates

### 📊 Cost Estimation

#### Monthly Costs (Approximate)
- **1x Standard_B1s VM**: ~$7.50/month
- **Storage**: ~$2-5/month
- **Network**: ~$1-3/month
- **Total**: ~$10-15/month

#### Cost Optimization Tips
- Use auto-shutdown for VMs
- Monitor usage patterns
- Scale down during off-hours
- Use reserved instances for production

### 🔍 Troubleshooting

#### Common Issues
1. **VM Creation Fails**
   - Check subscription limits
   - Verify VM size availability
   - Check resource provider registration

2. **Network Connectivity**
   - Verify NSG rules
   - Check VNet configuration
   - Test RDP connectivity

3. **AVD Agent Issues**
   - Verify host pool registration
   - Check agent installation
   - Review event logs

### 📞 Support
- Azure Documentation: https://docs.microsoft.com/azure/virtual-desktop/
- Azure Support: Available with paid subscriptions
- Community: Azure Virtual Desktop Tech Community