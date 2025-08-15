#!/usr/bin/env python3
"""
Check NSG Configuration for VM
"""

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_nsg_config():
    print("🔒 Checking NSG Configuration...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    network_client = NetworkManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Get VM details
        vm = compute_client.virtual_machines.get('avd-rg', 'avd-host-01')
        print(f"VM Name: {vm.name}")
        
        # Get NIC details
        nic_name = 'avd-host-01-nic'
        nic = network_client.network_interfaces.get('avd-rg', nic_name)
        print(f"NIC: {nic.name}")
        
        # Check if NSG is attached to NIC
        if nic.network_security_group:
            nsg_id = nic.network_security_group.id
            nsg_name = nsg_id.split('/')[-1]
            print(f"✅ NSG attached to NIC: {nsg_name}")
            
            # Get NSG details
            nsg = network_client.network_security_groups.get('avd-rg', nsg_name)
            print(f"\n🔍 NSG Rules:")
            
            # Check inbound rules
            print("Inbound Rules:")
            rdp_rule_found = False
            for rule in nsg.security_rules:
                print(f"  - {rule.name}: {rule.protocol} {rule.source_port_range} -> {rule.destination_port_range}")
                print(f"    Source: {rule.source_address_prefix}, Action: {rule.access}")
                
                # Check for RDP rule
                if (rule.destination_port_range == '3389' and 
                    rule.protocol == 'Tcp' and 
                    rule.access == 'Allow'):
                    rdp_rule_found = True
                    print(f"    ✅ RDP Rule Found!")
            
            if not rdp_rule_found:
                print("  ❌ No RDP rule found (port 3389)")
                
        else:
            print("❌ No NSG attached to NIC")
            
        # Check subnet NSG
        print(f"\n🔍 Subnet NSG Check:")
        subnet_name = 'avd-subnet'
        vnet_name = 'avd-vnet'
        
        try:
            subnet = network_client.subnets.get('avd-rg', vnet_name, subnet_name)
            if subnet.network_security_group:
                subnet_nsg_id = subnet.network_security_group.id
                subnet_nsg_name = subnet_nsg_id.split('/')[-1]
                print(f"✅ Subnet NSG: {subnet_nsg_name}")
                
                # Get subnet NSG details
                subnet_nsg = network_client.network_security_groups.get('avd-rg', subnet_nsg_name)
                print("Subnet NSG Inbound Rules:")
                for rule in subnet_nsg.security_rules:
                    print(f"  - {rule.name}: {rule.protocol} {rule.source_port_range} -> {rule.destination_port_range}")
                    
            else:
                print("❌ No NSG attached to subnet")
                
        except Exception as e:
            print(f"❌ Error checking subnet NSG: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_nsg_config()
