# Azure Settings Management Feature

## Overview

The Azure Management Tool now includes a comprehensive web-based settings interface that allows end users to view and update Azure configuration settings directly from the browser, without needing to manually edit configuration files.

## Features

### 🔧 **Web-Based Configuration Management**
- **View Current Settings**: Display current Azure credentials and configuration
- **Update Credentials**: Modify Azure tenant ID, client ID, client secret, and subscription ID
- **Test Connection**: Verify Azure connectivity with current settings
- **Real-time Validation**: Immediate feedback on configuration changes

### 🛡️ **Security Features**
- **Secure Storage**: Credentials are stored in the `.env` file (not exposed in web interface)
- **Password Masking**: Client secrets are masked with `***` when displayed
- **Input Validation**: Required field validation and format checking
- **Connection Testing**: Automatic verification of credentials before saving

### 🎨 **User Experience**
- **Modern Interface**: Clean, responsive design with dark/light theme support
- **Intuitive Navigation**: Easy access via settings icon in the header
- **Help Documentation**: Built-in guide for obtaining Azure credentials
- **Status Feedback**: Real-time connection status and error messages

## How to Access

### From the Dashboard
1. Look for the **settings icon** (⚙️) in the top-right corner of the dashboard
2. Click the settings icon to navigate to the configuration page
3. Or directly visit: `http://localhost:5000/settings`

### Direct URL Access
- **Settings Page**: `http://localhost:5000/settings`
- **API Endpoints**: 
  - `GET /api/settings/azure` - Get current settings
  - `POST /api/settings/azure` - Update settings
  - `GET /api/settings/test-connection` - Test Azure connection

## Configuration Options

### Required Fields
- **Subscription ID**: Your Azure subscription ID (GUID format)
- **Tenant ID**: Your Azure AD tenant ID (GUID format)
- **Client ID**: Application (client) ID from your service principal
- **Client Secret**: Client secret from your service principal

### Optional Fields
- **Default Location**: Preferred Azure region for new resources
- **Default Resource Group**: Default resource group name

## API Endpoints

### Get Current Settings
```http
GET /api/settings/azure
```

**Response:**
```json
{
  "subscription_id": "your-subscription-id",
  "tenant_id": "your-tenant-id",
  "client_id": "your-client-id",
  "client_secret": "***",
  "default_location": "East US",
  "default_resource_group": "your-rg"
}
```

### Update Settings
```http
POST /api/settings/azure
Content-Type: application/json

{
  "subscription_id": "new-subscription-id",
  "tenant_id": "new-tenant-id",
  "client_id": "new-client-id",
  "client_secret": "new-client-secret",
  "default_location": "West US",
  "default_resource_group": "new-rg"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Azure configuration updated successfully and connection verified!"
}
```

### Test Connection
```http
GET /api/settings/test-connection
```

**Response:**
```json
{
  "success": true,
  "message": "Azure connection successful!",
  "subscription": {
    "id": "subscription-id",
    "name": "Subscription Name",
    "state": "Enabled"
  }
}
```

## How to Get Azure Credentials

### 1. Create a Service Principal
1. Go to Azure Portal → Azure Active Directory → App registrations
2. Click "New registration" and create a new app
3. Note down the **Application (client) ID** and **Directory (tenant) ID**

### 2. Create a Client Secret
1. In your app registration, go to "Certificates & secrets"
2. Click "New client secret" and create a new secret
3. **Copy the secret value immediately** (you won't see it again)

### 3. Assign Permissions
1. Go to "API permissions" and add the required permissions
2. For resource management, add "Contributor" role to your subscription

### 4. Get Subscription ID
1. Go to Azure Portal → Subscriptions
2. Copy your subscription ID (GUID format)

## Security Considerations

### ✅ **Best Practices**
- Store production secrets in Azure Key Vault
- Rotate credentials regularly
- Use least-privilege access for service principals
- Monitor access logs and audit trails

### ⚠️ **Important Notes**
- The `.env` file contains sensitive information
- Ensure proper file permissions (readable only by the application)
- Never commit credentials to version control
- Consider using environment variables in production

## Troubleshooting

### Common Issues

**"Configuration updated but authentication failed"**
- Verify your Azure credentials are correct
- Check that the service principal has proper permissions
- Ensure the subscription is active and accessible

**"Failed to load current settings"**
- Check that the `.env` file exists and is readable
- Verify the application has proper file permissions

**"Connection test failed"**
- Check your internet connectivity
- Verify Azure services are available
- Ensure your service principal hasn't expired

### Debug Steps
1. Test connection using the "Test Connection" button
2. Check application logs for detailed error messages
3. Verify Azure portal access with the same credentials
4. Ensure all required environment variables are set

## Technical Implementation

### Backend Changes
- **New Routes**: Added settings management endpoints
- **File Management**: Secure `.env` file reading and writing
- **Authentication**: Automatic credential validation and testing
- **Error Handling**: Comprehensive error handling and user feedback

### Frontend Changes
- **Settings Page**: New responsive settings interface
- **Dashboard Integration**: Added settings link to main dashboard
- **Real-time Updates**: Dynamic status updates and validation
- **User Experience**: Intuitive form design with help text

### Security Implementation
- **Credential Masking**: Client secrets are never exposed in the UI
- **Input Validation**: Server-side validation of all inputs
- **File Security**: Proper file handling and permissions
- **Session Management**: Secure session handling for settings updates

## Future Enhancements

### Planned Features
- **Credential Encryption**: Encrypt sensitive data at rest
- **Audit Logging**: Track configuration changes
- **Multi-tenant Support**: Manage multiple Azure subscriptions
- **Role-based Access**: Control who can modify settings
- **Backup/Restore**: Configuration backup and restore functionality

### Integration Opportunities
- **Azure Key Vault**: Store secrets in Azure Key Vault
- **Azure AD Integration**: Use managed identities
- **Configuration Management**: Integration with Azure App Configuration
- **Monitoring**: Azure Monitor integration for settings changes
