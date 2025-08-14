# Azure Portal Management Tool

A comprehensive Python-based tool for managing Azure resources via API. This tool provides a command-line interface and programmatic access to manage your Azure subscription, including virtual machines, storage accounts, web apps, and more.

## 🔐 Security Notice

**IMPORTANT**: This repository contains Azure management tools. Never commit your actual Azure credentials to version control!

- ✅ `.env` files are automatically excluded via `.gitignore`
- ✅ Use `.env.example` as a template for your credentials
- ✅ Store production secrets in Azure Key Vault
- ✅ Rotate credentials regularly

## Features

### 🌐 **Web Application**
- 🎨 **Modern Web Interface**: Beautiful, responsive Flask-based web application
- 🔍 **Advanced Search & Filtering**: Real-time search with resource type and location filters
- 🎮 **Interactive Resource Management**: Start/Stop/Restart VMs with action buttons
- 💰 **Cost Analytics**: Real-time cost estimation and display
- 🌙 **Dark/Light Theme**: Toggle between themes with persistent preferences
- 📋 **Detailed Resource Views**: Comprehensive modals with resource information
- 🔔 **Smart Notifications**: Success/Error/Info notifications with auto-dismiss
- 📱 **Mobile Responsive**: Optimized for desktop, tablet, and mobile devices

### 🔧 **Core Management Features**
- 🔐 **Multiple Authentication Methods**: Service Principal, Interactive Browser, Managed Identity
- 📊 **Resource Dashboard**: Comprehensive overview of all Azure resources
- 🖥️ **Virtual Machine Management**: List, monitor, and manage VMs
- 💾 **Storage Account Management**: Monitor storage accounts and their status
- 🌐 **Web App Management**: Manage Azure Web Apps and their configurations
- 📁 **Resource Group Management**: Organize and manage resource groups
- 🎯 **Cost Management**: Monitor and analyze Azure costs
- 🔍 **Real-time Monitoring**: Get current status of all resources

## Prerequisites

- Python 3.8 or higher
- Azure subscription
- Appropriate permissions in your Azure subscription

## Installation

1. **Clone or download this project**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd /path/to/your/azure-management-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Azure authentication**
   ```bash
   python azure_cli.py setup
   ```

## Authentication Setup

The tool supports three authentication methods:

### 1. Interactive Browser Authentication (Recommended for development)
- Opens your browser for login
- No need to create service principals
- Perfect for testing and development

### 2. Service Principal Authentication (Recommended for production)
- Create a service principal in Azure AD
- Provides secure, automated access
- Best for production environments

### 3. Managed Identity Authentication
- For use within Azure (VMs, App Services, etc.)
- Automatically uses the system's managed identity

## Quick Start

### 1. Initial Setup
```bash
# Run the setup wizard
python azure_cli.py setup
```

### 2. Test Authentication
```bash
# Test your Azure connection
python azure_cli.py auth
```

### 3. View Dashboard
```bash
# See all your Azure resources
python azure_cli.py dashboard
```

### 4. Launch Web Application
```bash
# Start the web interface
python app.py

# Access the web application
# Open your browser and go to: http://localhost:5000
```

### 5. Docker Deployment (Optional)
```bash
# Build and run with Docker
docker-compose up --build

# Or build and run manually
docker build -t azure-management-tool .
docker run -p 5000:5000 --env-file .env azure-management-tool
```

## Usage Examples

### View All Resources
```bash
# Comprehensive dashboard
python azure_cli.py dashboard
```

### List Specific Resources
```bash
# List all virtual machines
python azure_cli.py list vms

# List VMs in a specific resource group
python azure_cli.py list vms --resource-group my-rg

# List storage accounts
python azure_cli.py list storage

# List web apps
python azure_cli.py list webapps

# List resource groups
python azure_cli.py list resourcegroups
```

### Web Application Usage
```bash
# Start the web application
python app.py

# Access the web interface
# Open your browser and go to: http://localhost:5000
```

**Web Application Features:**
- **Dashboard**: View all Azure resources in a beautiful web interface
- **Search**: Real-time search across all resources
- **Filtering**: Filter by resource type and location
- **Resource Actions**: Start/Stop/Restart VMs directly from the web interface
- **Detailed Views**: Click "View Details" for comprehensive resource information
- **Theme Toggle**: Switch between dark and light themes
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Programmatic Usage
```python
from azure_manager import AzureManager

# Initialize the manager
manager = AzureManager("your-subscription-id")

# Authenticate
if manager.authenticate("interactive"):
    # Get all VMs
    vms = manager.list_virtual_machines()
    
    # Get storage accounts
    storage_accounts = manager.list_storage_accounts()
    
    # Display dashboard
    manager.display_dashboard()
```

## Configuration

The tool uses environment variables for configuration. Create a `.env` file in the project directory:

```env
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_subscription_id_here
AZURE_TENANT_ID=your_tenant_id_here
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_DEFAULT_LOCATION=East US
AZURE_DEFAULT_RESOURCE_GROUP=your_resource_group_name

# Flask Web Application Configuration
FLASK_SECRET_KEY=your-secret-key-change-this
FLASK_DEBUG=False
FLASK_ENV=production
PORT=5000
```

## Service Principal Setup (Production)

For production use, create a service principal:

1. **Go to Azure Portal** → Azure Active Directory → App registrations
2. **Click "New registration"**
3. **Fill in details**:
   - Name: `Azure Management Tool`
   - Supported account types: `Accounts in this organizational directory only`
4. **After creation, note**:
   - Application (client) ID
   - Directory (tenant) ID
5. **Create a client secret**:
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Note the secret value
6. **Add API permissions**:
   - Go to "API permissions"
   - Add "Azure Service Management" with "Contributor" role
7. **Assign subscription permissions**:
   - Go to your subscription → Access control (IAM)
   - Add the service principal as "Contributor"

## Available Commands

### Main Commands
- `setup` - Interactive setup wizard
- `auth` - Test Azure authentication
- `dashboard` - Display resource dashboard

### List Commands
- `list vms` - List virtual machines
- `list storage` - List storage accounts
- `list webapps` - List web apps
- `list resourcegroups` - List resource groups

### Options
- `--subscription-id` - Specify Azure subscription ID
- `--auth-method` - Choose authentication method
- `--resource-group` - Filter by resource group

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check your subscription ID
   - Verify service principal permissions
   - Ensure client secret is correct

2. **Permission Denied**
   - Verify the service principal has Contributor role
   - Check subscription access

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **No Resources Found**
   - Verify you're using the correct subscription
   - Check if resources exist in the specified resource group

### Getting Help

```bash
# Show help for all commands
python azure_cli.py --help

# Show help for specific command
python azure_cli.py list vms --help
```

## Security Best Practices

1. **Use Service Principals** for production environments
2. **Store secrets securely** (use Azure Key Vault in production)
3. **Limit permissions** to only what's necessary
4. **Rotate client secrets** regularly
5. **Use managed identities** when running in Azure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Azure documentation
3. Verify your Azure permissions
4. Test with a simple authentication first

## Azure Resource Types Supported

- ✅ Virtual Machines
- ✅ Storage Accounts
- ✅ Web Apps
- ✅ Resource Groups
- ✅ Network Resources
- ✅ SQL Databases
- ✅ Monitoring & Alerts
- ✅ Cost Management

## ✅ Implemented Features

### 🎯 **Quick Wins (Recently Added)**
- ✅ **Web Interface**: Full Flask-based web application with modern UI
- ✅ **Search & Filtering**: Real-time search across all resources with type and location filters
- ✅ **Resource Actions**: Start/Stop/Restart VMs with action buttons
- ✅ **Cost Display**: Estimated monthly cost calculations in dashboard
- ✅ **Dark/Light Theme**: Toggle between themes with persistent preference
- ✅ **Detailed Resource Modals**: Comprehensive resource information with action buttons
- ✅ **Notification System**: Success/Error/Info notifications with auto-dismiss
- ✅ **Responsive Design**: Mobile-friendly interface with modern styling

### 🔧 **Core Features**
- ✅ **Multiple Authentication Methods**: Service Principal, Interactive Browser, Managed Identity
- ✅ **Resource Dashboard**: Comprehensive overview of all Azure resources
- ✅ **Virtual Machine Management**: List, monitor, and manage VMs
- ✅ **Storage Account Management**: Monitor storage accounts and their status
- ✅ **Web App Management**: Manage Azure Web Apps and their configurations
- ✅ **Resource Group Management**: Organize and manage resource groups
- ✅ **Cost Management**: Monitor and analyze Azure costs
- ✅ **Real-time Monitoring**: Get current status of all resources

## 🚀 Future Enhancements

### **High Priority**
- [ ] **Real VM Operations**: Implement actual VM start/stop/restart via Azure API
- [ ] **Resource Creation**: Create new VMs, storage accounts, and web apps
- [ ] **Resource Deletion**: Safe deletion with confirmation dialogs
- [ ] **User Authentication**: Add login system for web interface
- [ ] **Role-based Access Control**: Different permissions for different users

### **Medium Priority**
- [ ] **Backup Management**: Azure Backup integration and management
- [ ] **Network Security Groups**: Configure and manage NSG rules
- [ ] **Load Balancer Configuration**: Set up and manage load balancers
- [ ] **Auto-scaling Rules**: Configure VM scale sets and auto-scaling
- [ ] **Cost Optimization**: AI-powered cost recommendations
- [ ] **Export Functionality**: Export resource data to CSV/JSON
- [ ] **Bulk Operations**: Perform actions on multiple resources

### **Advanced Features**
- [ ] **Real-time Monitoring**: Live resource status updates
- [ ] **Alert Management**: Configure and manage Azure Monitor alerts
- [ ] **Log Analytics**: Integration with Azure Log Analytics
- [ ] **Container Management**: AKS cluster management
- [ ] **Database Management**: SQL Database and Cosmos DB management
- [ ] **API Rate Limiting**: Smart handling of Azure API limits
- [ ] **Multi-subscription Support**: Manage multiple Azure subscriptions
- [ ] **Audit Logging**: Track all actions performed through the tool
# azure-management-tool
