#!/usr/bin/env python3
"""
Add Public IP to VM
"""

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_public_ip():
    print("🌐 Adding Public IP to VM...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Create public IP
        public_ip_name = 'avd-host-01-pip'
        print(f"Creating public IP: {public_ip_name}")
        
        public_ip_params = {
            'location': 'eastus',
            'public_ip_allocation_method': 'Dynamic',
            'idle_timeout_in_minutes': 4
        }
        
        public_ip = network_client.public_ip_addresses.begin_create_or_update(
            'avd-rg', public_ip_name, public_ip_params
        ).result()
        
        print(f"✅ Public IP created: {public_ip.name}")
        print(f"   IP Address: {public_ip.ip_address}")
        
        # Update NIC to use public IP
        nic_name = 'avd-host-01-nic'
        print(f"Updating NIC: {nic_name}")
        
        nic = network_client.network_interfaces.get('avd-rg', nic_name)
        nic.ip_configurations[0].public_ip_address = public_ip
        
        updated_nic = network_client.network_interfaces.begin_create_or_update(
            'avd-rg', nic_name, nic
        ).result()
        
        print("✅ NIC updated with public IP")
        print(f"   You can now connect to: {public_ip.ip_address}")
        print(f"   Username: avdadmin")
        print(f"   Password: AVD@dmin123!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_public_ip()
