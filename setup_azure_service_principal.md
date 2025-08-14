# Azure Service Principal Setup Guide

This guide will walk you through creating a service principal in Azure for secure API access to your Azure resources.

## Prerequisites

- Azure subscription with admin access
- Azure Active Directory (AAD) tenant
- Global Administrator or Application Administrator role

## Step-by-Step Setup

### Step 1: Create App Registration

1. **Navigate to Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Sign in with your Azure account

2. **Access Azure Active Directory**
   - Search for "Azure Active Directory" in the search bar
   - Click on "Azure Active Directory" from the results

3. **Go to App Registrations**
   - In the left sidebar, click on "App registrations"
   - Click "New registration"

4. **Fill in Registration Details**
   - **Name**: `Azure Management Tool` (or any descriptive name)
   - **Supported account types**: Select "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank for now
   - Click "Register"

### Step 2: Note Important Information

After registration, you'll be taken to the app overview page. Note down:

- **Application (client) ID**: This is your `AZURE_CLIENT_ID`
- **Directory (tenant) ID**: This is your `AZURE_TENANT_ID`

### Step 3: Create Client Secret

1. **Navigate to Certificates & Secrets**
   - In the left sidebar, click "Certificates & secrets"
   - Click "New client secret"

2. **Configure Secret**
   - **Description**: `Azure Management Tool Secret`
   - **Expires**: Choose an appropriate expiration (recommend 12 months)
   - Click "Add"

3. **Copy the Secret Value**
   - **IMPORTANT**: Copy the secret value immediately - you won't be able to see it again!
   - This is your `AZURE_CLIENT_SECRET`

### Step 4: Configure API Permissions

1. **Go to API Permissions**
   - In the left sidebar, click "API permissions"
   - Click "Add a permission"

2. **Select Azure Service Management**
   - Choose "Azure Service Management"
   - Select "Application permissions"
   - Check "user_impersonation"
   - Click "Add permissions"

3. **Grant Admin Consent**
   - Click "Grant admin consent for [your organization]"
   - Confirm the action

### Step 5: Assign Subscription Permissions

1. **Navigate to Your Subscription**
   - Go to "Subscriptions" in the Azure portal
   - Click on your subscription

2. **Access Control (IAM)**
   - In the left sidebar, click "Access control (IAM)"
   - Click "Add" → "Add role assignment"

3. **Assign Contributor Role**
   - **Role**: Select "Contributor"
   - **Members**: Click "Select members"
   - Search for your app registration name
   - Select it and click "Select"
   - Click "Review + assign"

### Step 6: Configure Environment Variables

Create a `.env` file in your project directory:

```env
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_subscription_id_here
AZURE_TENANT_ID=your_tenant_id_here
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_DEFAULT_LOCATION=East US
```

### Step 7: Test the Configuration

```bash
# Install dependencies
pip install -r requirements.txt

# Test authentication
python azure_cli.py auth

# View dashboard
python azure_cli.py dashboard
```

## Security Best Practices

### 1. Secret Management
- **Never commit secrets to version control**
- Use Azure Key Vault for production environments
- Rotate secrets regularly (every 6-12 months)

### 2. Principle of Least Privilege
- Only grant necessary permissions
- Consider using Reader role instead of Contributor for read-only operations
- Use custom roles for specific permissions

### 3. Monitoring
- Enable audit logs for the service principal
- Monitor sign-in activity
- Set up alerts for unusual activity

### 4. Network Security
- Use IP restrictions if possible
- Consider using private endpoints for Azure services
- Implement network security groups

## Troubleshooting

### Common Issues

1. **"AADSTS700016: Application with identifier was not found"**
   - Verify the client ID is correct
   - Ensure the app registration exists in the correct tenant

2. **"AADSTS7000215: Invalid client secret is provided"**
   - Check if the client secret has expired
   - Verify the secret value is correct
   - Create a new secret if needed

3. **"AADSTS50013: Assertion failed"**
   - Check if the tenant ID is correct
   - Verify the app registration is in the correct tenant

4. **"AuthorizationFailed: The client does not have authorization"**
   - Verify the service principal has the correct role assignment
   - Check if admin consent was granted for API permissions
   - Ensure the subscription ID is correct

### Verification Steps

1. **Check App Registration**
   ```bash
   # Verify app registration exists
   az ad app show --id YOUR_CLIENT_ID
   ```

2. **Verify Role Assignment**
   ```bash
   # Check role assignments
   az role assignment list --assignee YOUR_CLIENT_ID
   ```

3. **Test API Access**
   ```bash
   # Test with Azure CLI
   az login --service-principal -u YOUR_CLIENT_ID -p YOUR_CLIENT_SECRET --tenant YOUR_TENANT_ID
   az account show
   ```

## Alternative: Using Azure CLI

You can also create a service principal using Azure CLI:

```bash
# Login to Azure
az login

# Create service principal
az ad sp create-for-rbac --name "Azure Management Tool" --role contributor

# The output will contain all the necessary information
```

## Next Steps

After setting up the service principal:

1. **Test the connection** using the provided tools
2. **Explore your resources** with the dashboard
3. **Set up monitoring** for the service principal
4. **Document the setup** for your team
5. **Plan secret rotation** schedule

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Azure AD documentation
3. Verify all permissions are correctly assigned
4. Test with Azure CLI first
5. Check Azure AD audit logs for errors

## Additional Resources

- [Azure AD App Registration Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Service Principal Best Practices](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)
- [Azure RBAC Documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/)
- [Azure Key Vault for Secret Management](https://docs.microsoft.com/en-us/azure/key-vault/)
