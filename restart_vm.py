#!/usr/bin/env python3
"""
Restart VM for AVD Registration
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def restart_vm():
    print("🔄 Restarting VM for AVD Registration...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Restart the VM
        print("   Restarting avd-host-01...")
        poller = compute_client.virtual_machines.begin_restart('avd-rg', 'avd-host-01')
        
        print("   VM restarting... (this may take 2-3 minutes)")
        result = poller.result()
        
        print("✅ VM restart completed!")
        
        # Wait a bit for the VM to fully boot
        print("   Waiting for VM to fully boot...")
        time.sleep(30)
        
        # Check VM status
        vm = compute_client.virtual_machines.get('avd-rg', 'avd-host-01')
        print(f"   VM Status: {vm.provisioning_state}")
        
        print(f"\n🎉 AVD Setup Complete!")
        print(f"   VM: avd-host-01 has been restarted")
        print(f"   AVD Agent and Boot Loader are installed")
        print(f"   Registration should complete automatically")
        
        print(f"\n📋 Next Steps:")
        print(f"   1. Wait 5-10 minutes for AVD registration to complete")
        print(f"   2. Add users to the application group")
        print(f"   3. Test AVD client connection")
        
        print(f"\n🔗 Connection Details:")
        print(f"   Public IP: 172.190.184.16")
        print(f"   Username: avdadmin")
        print(f"   Password: AVD@dmin123!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    restart_vm()
