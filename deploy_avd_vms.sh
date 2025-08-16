#!/bin/bash
# AVD Session Host Deployment Script
# Optimized for Azure Free Tier

set -e

# Configuration
RESOURCE_GROUP="avd-rg"
LOCATION="eastus"
VM_SIZE="Standard_B1s"  # Free tier friendly
VM_COUNT=1
ADMIN_USERNAME="${AVD_ADMIN_USERNAME:-avdadmin}"
ADMIN_PASSWORD="${AVD_ADMIN_PASSWORD:-CHANGE_THIS_PASSWORD}"  # Set via environment variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AVD Session Host Deployment${NC}"
echo -e "${BLUE}Resource Group: ${RESOURCE_GROUP}${NC}"
echo -e "${BLUE}Location: ${LOCATION}${NC}"
echo -e "${BLUE}VM Size: ${VM_SIZE}${NC}"
echo -e "${BLUE}VM Count: ${VM_COUNT}${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged into Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Create resource group if it doesn't exist
echo -e "${BLUE}📦 Creating resource group...${NC}"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create virtual network if it doesn't exist
echo -e "${BLUE}🌐 Creating virtual network...${NC}"
az network vnet create \
    --resource-group $RESOURCE_GROUP \
    --name avd-vnet \
    --address-prefix 10.0.0.0/16 \
    --subnet-name avd-subnet \
    --subnet-prefix 10.0.1.0/24

# Create network security group
echo -e "${BLUE}🔒 Creating network security group...${NC}"
az network nsg create \
    --resource-group $RESOURCE_GROUP \
    --name avd-nsg

# Add RDP rule
az network nsg rule create \
    --resource-group $RESOURCE_GROUP \
    --nsg-name avd-nsg \
    --name AllowRDP \
    --protocol tcp \
    --priority 1000 \
    --destination-port-range 3389 \
    --access allow

# Deploy session hosts
for i in $(seq 1 $VM_COUNT); do
    VM_NAME="avd-session-host-$(printf "%02d" $i)"
    NIC_NAME="${VM_NAME}-nic"
    
    echo -e "${BLUE}🖥️  Creating VM: ${VM_NAME}${NC}"
    
    # Create network interface
    echo -e "${YELLOW}  Creating network interface...${NC}"
    az network nic create \
        --resource-group $RESOURCE_GROUP \
        --name $NIC_NAME \
        --vnet-name avd-vnet \
        --subnet avd-subnet \
        --network-security-group avd-nsg
    
    # Create VM
    echo -e "${YELLOW}  Creating virtual machine...${NC}"
    az vm create \
        --resource-group $RESOURCE_GROUP \
        --name $VM_NAME \
        --location $LOCATION \
        --size $VM_SIZE \
        --nics $NIC_NAME \
        --image "MicrosoftWindowsDesktop:windows-11:win11-22h2-pro:latest" \
        --admin-username $ADMIN_USERNAME \
        --admin-password $ADMIN_PASSWORD \
        --no-wait
    
    echo -e "${GREEN}✅ VM ${VM_NAME} creation initiated${NC}"
done

# Wait for all VMs to be created
echo -e "${BLUE}⏳ Waiting for VMs to be created...${NC}"
az vm wait --created --resource-group $RESOURCE_GROUP --timeout 1800

echo -e "${GREEN}🎉 AVD Session Host deployment completed!${NC}"
echo -e "${YELLOW}⚠️  Next steps:${NC}"
echo -e "${YELLOW}1. Install AVD agent on session hosts${NC}"
echo -e "${YELLOW}2. Configure host pool registration${NC}"
echo -e "${YELLOW}3. Test connectivity${NC}"
echo -e "${YELLOW}4. Monitor costs in Azure portal${NC}"

# List created VMs
echo -e "${BLUE}📋 Created VMs:${NC}"
az vm list --resource-group $RESOURCE_GROUP --output table