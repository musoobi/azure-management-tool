#!/usr/bin/env python3
"""
Create NSG with RDP Rules
"""

from azure.mgmt.network import NetworkManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_nsg_with_rules():
    print("🔒 Creating NSG with RDP Rules...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Create NSG
        nsg_name = 'avd-nsg'
        print(f"Creating NSG: {nsg_name}")
        
        nsg_params = {
            'location': 'eastus',
            'security_rules': [
                {
                    'name': 'AllowRDP',
                    'priority': 1000,
                    'protocol': 'Tcp',
                    'access': 'Allow',
                    'direction': 'Inbound',
                    'source_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_address_prefix': '*',
                    'destination_port_range': '3389',
                    'description': 'Allow RDP access'
                },
                {
                    'name': 'AllowHTTPS',
                    'priority': 1001,
                    'protocol': 'Tcp',
                    'access': 'Allow',
                    'direction': 'Inbound',
                    'source_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_address_prefix': '*',
                    'destination_port_range': '443',
                    'description': 'Allow HTTPS access'
                },
                {
                    'name': 'AllowHTTP',
                    'priority': 1002,
                    'protocol': 'Tcp',
                    'access': 'Allow',
                    'direction': 'Inbound',
                    'source_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_address_prefix': '*',
                    'destination_port_range': '80',
                    'description': 'Allow HTTP access'
                },
                {
                    'name': 'DenyAllInbound',
                    'priority': 4096,
                    'protocol': '*',
                    'access': 'Deny',
                    'direction': 'Inbound',
                    'source_address_prefix': '*',
                    'source_port_range': '*',
                    'destination_address_prefix': '*',
                    'destination_port_range': '*',
                    'description': 'Deny all other inbound traffic'
                }
            ]
        }
        
        nsg = network_client.network_security_groups.begin_create_or_update(
            'avd-rg', nsg_name, nsg_params
        ).result()
        
        print(f"✅ NSG created: {nsg.name}")
        
        # Attach NSG to NIC
        nic_name = 'avd-host-01-nic'
        print(f"Attaching NSG to NIC: {nic_name}")
        
        nic = network_client.network_interfaces.get('avd-rg', nic_name)
        nic.network_security_group = nsg
        
        updated_nic = network_client.network_interfaces.begin_create_or_update(
            'avd-rg', nic_name, nic
        ).result()
        
        print("✅ NSG attached to NIC")
        
        # Also attach to subnet for future VMs
        print("Attaching NSG to subnet...")
        subnet_name = 'avd-subnet'
        vnet_name = 'avd-vnet'
        
        subnet = network_client.subnets.get('avd-rg', vnet_name, subnet_name)
        subnet.network_security_group = nsg
        
        updated_subnet = network_client.subnets.begin_create_or_update(
            'avd-rg', vnet_name, subnet_name, subnet
        ).result()
        
        print("✅ NSG attached to subnet")
        
        print("\n🎉 NSG Configuration Complete!")
        print("RDP (port 3389) is now allowed")
        print("You can now connect to the VM via Azure Portal RDP")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_nsg_with_rules()
