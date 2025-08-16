#!/usr/bin/env python3
"""
AVD Session Host VM Deployment using Azure SDK
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def deploy_session_hosts():
    print("🚀 Starting AVD Session Host VM Deployment...")
    
    # Initialize clients
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    # Configuration
    resource_group = 'avd-rg'
    location = 'eastus'
    vm_size = 'Standard_B1s'  # Free tier friendly
    vm_count = 1
    
    for i in range(vm_count):
        vm_name = f'avd-host-{i+1:02d}'
        nic_name = f'{vm_name}-nic'
        computer_name = f'avdhost{i+1:02d}'  # Short computer name
        
        print(f"Creating network interface: {nic_name}")
        
        # Create network interface
        nic_params = {
            'location': location,
            'ip_configurations': [{
                'name': 'ipconfig1',
                'subnet': {
                    'id': f'/subscriptions/{os.getenv("AZURE_SUBSCRIPTION_ID")}/resourceGroups/{resource_group}/providers/Microsoft.Network/virtualNetworks/avd-vnet/subnets/avd-subnet'
                }
            }]
        }
        
        network_client.network_interfaces.begin_create_or_update(
            resource_group, nic_name, nic_params
        ).result()
        
        print(f"Creating VM: {vm_name}")
        
        # Create VM
        vm_params = {
            'location': location,
            'hardware_profile': {
                'vm_size': vm_size
            },
            'os_profile': {
                'computer_name': computer_name,
                        'admin_username': os.getenv("AVD_ADMIN_USERNAME", "avdadmin"),
        'admin_password': os.getenv("AVD_ADMIN_PASSWORD", "CHANGE_THIS_PASSWORD")
            },
            'network_profile': {
                'network_interfaces': [{
                    'id': f'/subscriptions/{os.getenv("AZURE_SUBSCRIPTION_ID")}/resourceGroups/{resource_group}/providers/Microsoft.Network/networkInterfaces/{nic_name}'
                }]
            },
            'storage_profile': {
                'image_reference': {
                    'publisher': 'MicrosoftWindowsDesktop',
                    'offer': 'windows-10',
                    'sku': 'win10-22h2-pro',
                    'version': 'latest'
                }
            }
        }
        
        compute_client.virtual_machines.begin_create_or_update(
            resource_group, vm_name, vm_params
        ).result()
        
        print(f"✅ VM {vm_name} created successfully!")
    
    print("🎉 All session host VMs deployed successfully!")

if __name__ == "__main__":
    deploy_session_hosts()
