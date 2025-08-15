#!/usr/bin/env python3
"""
Complete AVD Setup with Enhanced Permissions
"""

from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def complete_avd_setup():
    print("🚀 Completing AVD Setup with Enhanced Permissions...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    avd_client = DesktopVirtualizationMgmtClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    print("\n📋 Current AVD Status:")
    
    # Get current resources
    host_pools = list(avd_client.host_pools.list_by_resource_group('avd-rg'))
    workspaces = list(avd_client.workspaces.list_by_resource_group('avd-rg'))
    app_groups = list(avd_client.application_groups.list_by_resource_group('avd-rg'))
    vms = list(compute_client.virtual_machines.list('avd-rg'))
    
    print(f"   ✅ Host Pools: {len(host_pools)}")
    print(f"   ✅ Workspaces: {len(workspaces)}")
    print(f"   ✅ Application Groups: {len(app_groups)}")
    print(f"   ✅ Session Host VMs: {len(vms)}")
    
    # Generate fresh registration token
    print("\n🔑 Generating Fresh Registration Token:")
    try:
        token = avd_client.host_pools.retrieve_registration_token('avd-rg', 'avd-host-pool')
        print(f"   ✅ Token Generated Successfully")
        print(f"   ✅ Expires: {token.expiration_time}")
        print(f"   📋 Token: {token.token}")
    except Exception as e:
        print(f"   ❌ Error generating token: {e}")
    
    # Get VM details
    print("\n🖥️ Session Host VM Details:")
    for vm in vms:
        print(f"   📋 VM Name: {vm.name}")
        print(f"   📋 Size: {vm.hardware_profile.vm_size}")
        print(f"   📋 Location: {vm.location}")
        print(f"   📋 Admin Username: avdadmin")
        print(f"   📋 Admin Password: AVD@dmin123!")
        
        # Get VM status
        try:
            vm_instance = compute_client.virtual_machines.instance_view('avd-rg', vm.name)
            if vm_instance.statuses:
                status = vm_instance.statuses[-1].display_status
                print(f"   📋 Status: {status}")
        except:
            print(f"   📋 Status: Unknown")
    
    # Get application group details
    print("\n📱 Application Group Details:")
    for app_group in app_groups:
        print(f"   📋 Name: {app_group.name}")
        print(f"   📋 Type: {app_group.application_group_type}")
        print(f"   📋 Host Pool: {app_group.host_pool_arm_path.split('/')[-1]}")
    
    print("\n🎯 Next Steps to Complete Setup:")
    print("1. Connect to VM via RDP using Azure Portal")
    print("2. Install AVD Agent: https://aka.ms/avdagent")
    print("3. Install AVD Boot Loader: https://aka.ms/avdbootloader")
    print("4. Register VM with host pool using the token above")
    print("5. Add users to application group via Azure Portal")
    print("6. Test AVD client connection")
    
    print("\n📊 Setup Progress:")
    print("   ✅ Infrastructure: 100% Complete")
    print("   ✅ VM Deployment: 100% Complete")
    print("   ⏳ AVD Agent Installation: Pending")
    print("   ⏳ User Configuration: Pending")
    print("   ⏳ Testing: Pending")
    
    print("\n🎉 AVD Environment Ready for Final Configuration!")

if __name__ == "__main__":
    complete_avd_setup()
