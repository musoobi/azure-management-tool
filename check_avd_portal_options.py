#!/usr/bin/env python3
"""
Check AVD Portal Setup Options
"""

from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_avd_portal_options():
    print("🔍 Checking AVD Portal Setup Options...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    avd_client = DesktopVirtualizationMgmtClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Get host pool details
        host_pool = avd_client.host_pools.get('avd-rg', 'avd-host-pool')
        print(f"Host Pool: {host_pool.name}")
        print(f"Type: {host_pool.host_pool_type}")
        
        # Get registration token
        registration_info = avd_client.host_pools.retrieve_registration_token('avd-rg', 'avd-host-pool')
        print(f"\n🔑 Registration Token:")
        print(f"   Token: {registration_info.token}")
        print(f"   Expires: {registration_info.expiration_time}")
        
        # Get VM details
        vm = compute_client.virtual_machines.get('avd-rg', 'avd-host-01')
        print(f"\n🖥️ VM Details:")
        print(f"   Name: {vm.name}")
        print(f"   Status: {vm.provisioning_state}")
        print(f"   Public IP: 172.190.184.16")
        
        print(f"\n🎯 EASIEST SETUP METHODS:")
        print(f"\n1. 🏆 AZURE PORTAL - ONE CLICK SETUP:")
        print(f"   - Go to Azure Portal → Azure Virtual Desktop")
        print(f"   - Click 'Host pools' → 'avd-host-pool'")
        print(f"   - Click 'Session hosts' → 'Add session hosts'")
        print(f"   - Select your VM: avd-host-01")
        print(f"   - Portal will automatically:")
        print(f"     ✅ Install AVD Agent")
        print(f"     ✅ Install AVD Boot Loader")
        print(f"     ✅ Register with host pool")
        print(f"     ✅ Configure everything")
        
        print(f"\n2. 🔧 AZURE CLI - AUTOMATED SCRIPT:")
        print(f"   - Use az vm run-command to run scripts")
        print(f"   - Automatically download and install agents")
        print(f"   - Register with host pool")
        
        print(f"\n3. 📋 MANUAL - WITH OUR TOKEN:")
        print(f"   - Connect to VM via RDP")
        print(f"   - Download agents manually")
        print(f"   - Use token: {registration_info.token}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_avd_portal_options()
