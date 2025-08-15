#!/usr/bin/env python3
"""
Add Standard SKU Public IP to VM
"""

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_standard_public_ip():
    print("�� Adding Standard SKU Public IP to VM...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Create Standard SKU public IP
        public_ip_name = 'avd-host-01-pip'
        print(f"Creating Standard SKU public IP: {public_ip_name}")
        
        public_ip_params = {
            'location': 'eastus',
            'sku': {
                'name': 'Standard'
            },
            'public_ip_allocation_method': 'Static',
            'idle_timeout_in_minutes': 4
        }
        
        public_ip = network_client.public_ip_addresses.begin_create_or_update(
            'avd-rg', public_ip_name, public_ip_params
        ).result()
        
        print(f"✅ Standard SKU Public IP created: {public_ip.name}")
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
        print(f"\n🎉 Connection Details:")
        print(f"   Public IP: {public_ip.ip_address}")
        print(f"   Username: avdadmin")
        print(f"   Password: AVD@dmin123!")
        print(f"   Port: 3389 (RDP)")
        
        print(f"\n🔧 Connect from Ubuntu:")
        print(f"   # Install Remmina (GUI)")
        print(f"   sudo apt install remmina remmina-plugin-rdp")
        print(f"   # Then connect to: {public_ip.ip_address}")
        
        print(f"\n   # Or use xfreerdp (command line)")
        print(f"   sudo apt install freerdp2-x11")
        print(f"   xfreerdp /v:{public_ip.ip_address} /u:avdadmin /p:AVD@dmin123!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Alternative: Use Azure Portal RDP")
        print(f"   1. Go to Azure Portal → Virtual Machines → avd-host-01")
        print(f"   2. Click 'Connect' → 'RDP'")
        print(f"   3. Download and open the RDP file")

if __name__ == "__main__":
    add_standard_public_ip()
