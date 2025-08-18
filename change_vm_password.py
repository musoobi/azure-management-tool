#!/usr/bin/env python3
"""
Change VM Password Securely
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
import secrets
import string
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_secure_password(length=16):
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def change_vm_password():
    print("🔐 Changing VM Password Securely...")
    
    # Generate a new secure password
    new_password = generate_secure_password()
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # VM details
        resource_group = 'avd-rg'
        vm_name = 'avd-host-01'
        
        print(f"🔄 Updating password for VM: {vm_name}")
        
        # PowerShell script to change password
        username = os.getenv('AVD_ADMIN_USERNAME', 'avdadmin')
        
        powershell_script = f"""
$username = "{username}"
$newPassword = "{new_password}"

try {{
    # Change the password for the specified user
    $securePassword = ConvertTo-SecureString $newPassword -AsPlainText -Force
    Set-LocalUser -Name $username -Password $securePassword
    
    Write-Output "Password changed successfully for user: $username"
    Write-Output "New password: $newPassword"
}} catch {{
    Write-Error "Failed to change password: $_"
    exit 1
}}
"""
        
        # Execute the script on the VM
        print("📡 Executing password change script on VM...")
        
        result = compute_client.virtual_machines.begin_run_command(
            resource_group,
            vm_name,
            {
                'command_id': 'RunPowerShellScript',
                'script': [powershell_script]
            }
        ).result()
        
        if result.value and result.value[0].message:
            print("✅ Password changed successfully!")
            print(f"\n🔐 New Credentials:")
            print(f"   Username: {username}")
            print(f"   Password: {new_password}")
            print(f"   VM: {vm_name}")
            
            # Update environment variable suggestion
            print(f"\n💡 Update your .env file with:")
            print(f"   AVD_ADMIN_PASSWORD={new_password}")
            
            # Save to a secure file (not committed to git)
            with open('.vm_password.txt', 'w') as f:
                f.write(f"Username: {username}\n")
                f.write(f"Password: {new_password}\n")
                f.write(f"VM: {vm_name}\n")
                f.write(f"Generated: {__import__('datetime').datetime.now()}\n")
            
            print(f"\n📝 Password saved to .vm_password.txt (not committed to git)")
            
        else:
            print("❌ Failed to change password")
            if result.value:
                for output in result.value:
                    if output.message:
                        print(f"   Error: {output.message}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Alternative: Change password manually via RDP")
        print(f"   1. Connect to VM via Azure Portal RDP")
        print(f"   2. Open Command Prompt as Administrator")
        print(f"   3. Run: net user {os.getenv('AVD_ADMIN_USERNAME', 'avdadmin')} new_password")

if __name__ == "__main__":
    change_vm_password()
