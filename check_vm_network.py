#!/usr/bin/env python3
"""
Check VM Network Configuration
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_vm_network():
    print("🔍 Checking VM Network Configuration...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Get VM details
        vm = compute_client.virtual_machines.get('avd-rg', 'avd-host-01')
        print(f"VM Name: {vm.name}")
        print(f"Location: {vm.location}")
        print(f"Size: {vm.hardware_profile.vm_size}")
        
        print("\nNetwork Interfaces:")
        for nic in vm.network_profile.network_interfaces:
            nic_name = nic.id.split('/')[-1]
            print(f"  - {nic_name}")
            
            # Get NIC details
            nic_details = network_client.network_interfaces.get('avd-rg', nic_name)
            
            if nic_details.ip_configurations:
                ip_config = nic_details.ip_configurations[0]
                print(f"    Private IP: {ip_config.private_ip_address}")
                print(f"    Subnet: {ip_config.subnet.id.split('/')[-1]}")
                
                # Check if public IP is assigned
                if hasattr(ip_config, 'public_ip_address') and ip_config.public_ip_address:
                    print(f"    Public IP: {ip_config.public_ip_address.id.split('/')[-1]}")
                else:
                    print(f"    Public IP: None (Private subnet)")
        
        print("\n🔧 Connection Options:")
        print("1. Use Azure Portal RDP (Recommended)")
        print("   - Go to Azure Portal → Virtual Machines → avd-host-01")
        print("   - Click 'Connect' → 'RDP'")
        print("   - Download and open the RDP file")
        
        print("\n2. Add Public IP to VM")
        print("   - This requires modifying the VM configuration")
        print("   - Not recommended for security reasons")
        
        print("\n3. Create Azure Bastion")
        print("   - Provides secure RDP access")
        print("   - Requires additional setup and cost")
        
        print("\n4. Set up VPN Connection")
        print("   - Connect your Ubuntu machine to Azure VNet")
        print("   - More complex setup required")
        
        print("\n🎯 Recommended Approach:")
        print("Use Azure Portal RDP - it's the easiest and most secure method!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_vm_network()
