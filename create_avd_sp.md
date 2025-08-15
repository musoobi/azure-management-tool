# 🚀 Creating AVD-Specific Service Principal

## 📋 Step-by-Step Guide

### **Step 1: Create App Registration**

1. **Go to Azure Portal:**
   - Navigate to: https://portal.azure.com
   - Go to **Azure Active Directory** → **App registrations**

2. **Create New Registration:**
   - Click **"New registration"**
   - **Name:** `AVD-Management-SP`
   - **Supported account types:** "Accounts in this organizational directory only"
   - **Redirect URI:** Leave blank
   - Click **"Register"**

3. **Note the Details:**
   - **Application (client) ID:** Copy this
   - **Directory (tenant) ID:** Copy this (should be same as current)

### **Step 2: Create Client Secret**

1. **In the new app registration:**
   - Go to **"Certificates & secrets"**
   - Click **"New client secret"**
   - **Description:** `AVD-Management-Secret`
   - **Expires:** Choose appropriate duration (e.g., 12 months)
   - Click **"Add"**

2. **Copy the Secret Value:**
   - **IMPORTANT:** Copy the secret value immediately (you won't see it again)
   - Save it securely

### **Step 3: Add API Permissions**

1. **Go to "API permissions":**
   - Click **"Add a permission"**
   - Select **"Microsoft Graph"**
   - Choose **"Application permissions"**

2. **Add These Permissions:**
   - `User.ReadWrite.All` - Manage users
   - `Group.ReadWrite.All` - Manage groups
   - `Directory.ReadWrite.All` - Full directory access
   - `Application.ReadWrite.All` - Manage applications

3. **Grant Admin Consent:**
   - Click **"Grant admin consent for [Your Tenant]"**

### **Step 4: Assign Azure Roles**

1. **Go to Subscriptions:**
   - Navigate to **Subscriptions** → **Your Subscription**
   - Go to **"Access control (IAM)"**

2. **Add Role Assignments:**
   - Click **"Add"** → **"Add role assignment"**
   - Add these roles to the new Service Principal:

   **Roles to Add:**
   - `Desktop Virtualization Administrator`
   - `Virtual Machine Administrator Login`
   - `User Administrator`
   - `Contributor` (for resource management)

### **Step 5: Update Environment Variables**

1. **Create new .env file or update existing:**
   ```bash
   # AVD Management Service Principal
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=new-client-id
   AZURE_CLIENT_SECRET=new-client-secret
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   ```

2. **Test the new Service Principal:**
   ```bash
   python test_permissions.py
   ```

## 🔧 What This Service Principal Can Do:

### **AVD Management:**
- ✅ Create and manage AVD host pools
- ✅ Manage AVD workspaces and application groups
- ✅ Add/remove users from AVD groups
- ✅ Generate registration tokens

### **VM Management:**
- ✅ Create and manage VMs
- ✅ Access VMs via RDP
- ✅ Install software on VMs
- ✅ Manage VM configurations

### **User Management:**
- ✅ Create and manage users
- ✅ Add users to groups
- ✅ Manage directory permissions

## ⚠️ Security Best Practices:

1. **Use Least Privilege:** Only add permissions you need
2. **Rotate Secrets:** Change client secrets regularly
3. **Monitor Usage:** Check audit logs regularly
4. **Limit Scope:** Consider limiting to specific resource groups
5. **Delete When Done:** Remove when not needed

## 🎯 Next Steps After Creation:

1. **Test the new Service Principal**
2. **Update your .env file**
3. **Complete AVD agent installation**
4. **Configure user access**
5. **Test the complete setup**

## 📞 Need Help?

If you encounter any issues:
1. Check the Azure Portal audit logs
2. Verify all permissions are granted
3. Ensure admin consent is given
4. Test with a simple operation first
