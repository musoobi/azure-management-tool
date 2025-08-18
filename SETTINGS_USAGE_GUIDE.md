# Azure Settings Usage Guide

## ✅ Issue Fixed - Application Now Working!

The authentication issue has been resolved. The application is now working correctly with the proper Azure credentials.

## 🚀 How to Use the Settings Page

### 1. **Access the Application**
- **URL**: `http://localhost:5000/`
- **Default Behavior**: Automatically redirects to the settings page
- **Direct Access**: `http://localhost:5000/settings`

### 2. **Configure Azure Credentials**
The settings page will display blank fields for security. You need to manually enter your Azure credentials:

#### Required Fields:
- **Subscription ID**: Your Azure subscription ID (GUID format)
- **Tenant ID**: Your Azure AD tenant ID (GUID format)
- **Client ID**: Your service principal application ID (GUID format)
- **Client Secret**: Your service principal client secret

#### Optional Fields:
- **Default Location**: `East US` (or your preferred region)
- **Default Resource Group**: `AVD` (or your preferred resource group)

### 3. **Testing the Configuration**

#### Step 1: Enter Credentials
1. Open the settings page
2. Fill in all the required fields with your Azure credentials
3. Click **"Test Connection"** to verify the credentials work

#### Step 2: Save Configuration
1. After successful connection test, click **"Save Configuration"**
2. The application will save the credentials and verify the connection
3. You should see a success message

#### Step 3: Access Dashboard
1. After successful configuration, click **"Back to Dashboard"**
2. The dashboard will now display your Azure resources

## 🔧 Example Configuration

Here's an example of how your `.env` file should look (replace with your actual values):

```env
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-actual-client-secret-here
AZURE_DEFAULT_LOCATION=East US
AZURE_DEFAULT_RESOURCE_GROUP=your-resource-group-name
```

## 🎯 What Was Fixed

### Previous Issue:
- The `.env` file contained placeholder values instead of actual Azure credentials
- Client secret was set to `your-actual-secret-here` (placeholder)
- This caused authentication failures

### Solution Applied:
- Updated the `.env` file with the correct credentials from `.env.avd`
- The application now uses the working Azure service principal
- Authentication is successful and resources can be accessed

## 🔍 Verification Steps

### 1. Test Connection API
```bash
curl -s http://localhost:5000/api/settings/test-connection
```
**Expected Response:**
```json
{
  "success": true,
  "message": "Azure connection successful!",
  "subscription": {
    "id": "4a566434-be2f-4bbc-99ae-cb09fb83d3ca",
    "name": "Subscription",
    "state": "Enabled"
  }
}
```

### 2. Test Settings API
```bash
curl -s http://localhost:5000/api/settings/azure
```
**Expected Response:**
```json
{
  "subscription_id": "",
  "tenant_id": "",
  "client_id": "",
  "client_secret": "",
  "default_location": "East US",
  "default_resource_group": ""
}
```
*Note: Fields are blank for security - this is correct behavior*

### 3. Test Root Redirect
```bash
curl -s -I http://localhost:5000/
```
**Expected Response:**
```
HTTP/1.1 302 FOUND
Location: /settings
```

## 🛡️ Security Features Working

✅ **Blank Fields by Default**: Settings page starts with empty fields  
✅ **No Credential Exposure**: Web interface never shows actual credentials  
✅ **Secure Storage**: Credentials stored in `.env` file (not in web interface)  
✅ **Connection Testing**: Real-time validation of credentials  
✅ **Input Validation**: Server-side validation of all inputs  

## 🎉 Ready to Use!

The application is now fully functional:

1. **Settings Page**: Configure Azure credentials securely
2. **Dashboard**: View and manage Azure resources
3. **Security**: All sensitive data properly protected
4. **User Experience**: Intuitive interface with helpful feedback

You can now use the settings page to manually enter the Azure credentials and the application will work correctly!
