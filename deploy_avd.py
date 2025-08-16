#!/usr/bin/env python3
"""
Azure Virtual Desktop (AVD) Deployment Script
Optimized for Azure Free Tier with minimal resource usage
"""

import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

console = Console()

class AVDDeployer:
    def __init__(self):
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        
        if not all([self.tenant_id, self.client_id, self.client_secret, self.subscription_id]):
            raise ValueError("Missing required Azure credentials in .env file")
        
        # Initialize credential
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        # Initialize clients
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.network_client = NetworkManagementClient(self.credential, self.subscription_id)
        self.compute_client = ComputeManagementClient(self.credential, self.subscription_id)
        self.avd_client = DesktopVirtualizationMgmtClient(self.credential, self.subscription_id)
        self.storage_client = StorageManagementClient(self.credential, self.subscription_id)
        
        # AVD Configuration
        self.location = "eastus"  # Free tier friendly location
        self.resource_group_name = "avd-rg"
        self.vnet_name = "avd-vnet"
        self.subnet_name = "avd-subnet"
        self.host_pool_name = "avd-host-pool"
        self.workspace_name = "avd-workspace"
        self.app_group_name = "avd-app-group"
        
    def create_resource_group(self):
        """Create resource group for AVD"""
        console.print(f"[bold blue]Creating resource group: {self.resource_group_name}[/bold blue]")
        
        try:
            resource_group = self.resource_client.resource_groups.create_or_update(
                self.resource_group_name,
                {"location": self.location}
            )
            console.print(f"[green]✓ Resource group created: {resource_group.name}[/green]")
            return resource_group
        except AzureError as e:
            console.print(f"[red]✗ Failed to create resource group: {e}[/red]")
            raise
    
    def create_virtual_network(self):
        """Create virtual network for AVD"""
        console.print(f"[bold blue]Creating virtual network: {self.vnet_name}[/bold blue]")
        
        vnet_params = {
            "location": self.location,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            },
            "subnets": [
                {
                    "name": self.subnet_name,
                    "address_prefix": "10.0.1.0/24"
                }
            ]
        }
        
        try:
            vnet_poller = self.network_client.virtual_networks.begin_create_or_update(
                self.resource_group_name,
                self.vnet_name,
                vnet_params
            )
            vnet = vnet_poller.result()
            console.print(f"[green]✓ Virtual network created: {vnet.name}[/green]")
            return vnet
        except AzureError as e:
            console.print(f"[red]✗ Failed to create virtual network: {e}[/red]")
            raise
    
    def create_host_pool(self):
        """Create AVD host pool"""
        console.print(f"[bold blue]Creating AVD host pool: {self.host_pool_name}[/bold blue]")
        
        host_pool_params = {
            "location": self.location,
            "host_pool_type": "Pooled",
            "load_balancer_type": "BreadthFirst",
            "max_session_limit": 10,
            "personal_desktop_assignment_type": "Automatic",
            "registration_info": {
                "expiration_time": (datetime.now() + timedelta(days=30)).isoformat(),
                "registration_token_operation": "Update"
            }
        }
        
        try:
            host_pool = self.avd_client.host_pools.create_or_update(
                self.resource_group_name,
                self.host_pool_name,
                host_pool_params
            )
            # host_pool = host_pool_poller.result()
            console.print(f"[green]✓ Host pool created: {host_pool.name}[/green]")
            return host_pool
        except AzureError as e:
            console.print(f"[red]✗ Failed to create host pool: {e}[/red]")
            raise
    
    def create_workspace(self):
        """Create AVD workspace"""
        console.print(f"[bold blue]Creating AVD workspace: {self.workspace_name}[/bold blue]")
        
        workspace_params = {
            "location": self.location,
            "description": "AVD Workspace for Free Tier"
        }
        
        try:
            workspace = self.avd_client.workspaces.create_or_update(
                self.resource_group_name,
                self.workspace_name,
                workspace_params
            )
            console.print(f"[green]✓ Workspace created: {workspace.name}[/green]")
            return workspace
        except AzureError as e:
            console.print(f"[red]✗ Failed to create workspace: {e}[/red]")
            raise
    
    def create_application_group(self):
        """Create AVD application group"""
        console.print(f"[bold blue]Creating AVD application group: {self.app_group_name}[/bold blue]")
        
        app_group_params = {
            "location": self.location,
            "host_pool_arm_path": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.DesktopVirtualization/hostPools/{self.host_pool_name}",
            "application_group_type": "Desktop"
        }
        
        try:
            app_group = self.avd_client.application_groups.create_or_update(
                self.resource_group_name,
                self.app_group_name,
                app_group_params
            )
            console.print(f"[green]✓ Application group created: {app_group.name}[/green]")
            return app_group
        except AzureError as e:
            console.print(f"[red]✗ Failed to create application group: {e}[/red]")
            raise
    
    def deploy_session_hosts(self, count: int = 1):
        """Deploy session host VMs (minimal for free tier)"""
        console.print(f"[bold blue]Deploying {count} session host(s)...[/bold blue]")
        
        # Use minimal VM size for free tier
        vm_size = "Standard_B1s"  # 1 vCPU, 1 GB RAM - free tier friendly
        
        for i in range(count):
            vm_name = f"avd-session-host-{i+1:02d}"
            console.print(f"[blue]Creating VM: {vm_name}[/blue]")
            
            # This is a simplified VM creation - in production you'd want more configuration
            # For now, we'll create a basic VM structure
            vm_params = {
                "location": self.location,
                "hardware_profile": {
                    "vm_size": vm_size
                },
                "os_profile": {
                    "computer_name": vm_name,
                            "admin_username": os.getenv("AVD_ADMIN_USERNAME", "avdadmin"),
        "admin_password": os.getenv("AVD_ADMIN_PASSWORD", "CHANGE_THIS_PASSWORD")
                },
                "network_profile": {
                    "network_interfaces": [
                        {
                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Network/networkInterfaces/{vm_name}-nic"
                        }
                    ]
                },
                "storage_profile": {
                    "image_reference": {
                        "publisher": "MicrosoftWindowsDesktop",
                        "offer": "windows-11",
                        "sku": "win11-22h2-pro",
                        "version": "latest"
                    }
                }
            }
            
            try:
                # Note: This is a simplified approach. In production, you'd need to:
                # 1. Create network interface first
                # 2. Handle disk creation
                # 3. Configure AVD agent installation
                console.print(f"[yellow]⚠ VM creation simplified for demo. Full deployment requires additional steps.[/yellow]")
                console.print(f"[green]✓ VM configuration prepared: {vm_name}[/green]")
                
            except AzureError as e:
                console.print(f"[red]✗ Failed to create VM {vm_name}: {e}[/red]")
                raise
    
    def deploy_avd_infrastructure(self):
        """Deploy complete AVD infrastructure"""
        console.print("[bold green]🚀 Starting AVD Deployment for Azure Free Tier[/bold green]")
        console.print(f"[blue]Location: {self.location}[/blue]")
        console.print(f"[blue]Resource Group: {self.resource_group_name}[/blue]")
        
        try:
            # Step 1: Create resource group
            self.create_resource_group()
            
            # Step 2: Create virtual network
            self.create_virtual_network()
            
            # Step 3: Create AVD components
            self.create_host_pool()
            self.create_workspace()
            self.create_application_group()
            
            # Step 4: Deploy session hosts (minimal for free tier)
            self.deploy_session_hosts(count=1)
            
            console.print("[bold green]✅ AVD Infrastructure deployment completed![/bold green]")
            console.print("\n[bold yellow]Next Steps:[/bold yellow]")
            console.print("1. Complete VM deployment with AVD agent")
            console.print("2. Configure user access")
            console.print("3. Test connectivity")
            console.print("4. Monitor costs in Azure portal")
            
        except Exception as e:
            console.print(f"[bold red]❌ Deployment failed: {e}[/bold red]")
            raise

@click.command()
@click.option('--session-hosts', default=1, help='Number of session hosts to deploy (default: 1)')
@click.option('--location', default='eastus', help='Azure region (default: eastus)')
def main(session_hosts: int, location: str):
    """Deploy Azure Virtual Desktop infrastructure"""
    try:
        deployer = AVDDeployer()
        deployer.location = location
        deployer.deploy_avd_infrastructure()
    except Exception as e:
        console.print(f"[bold red]Deployment failed: {e}[/bold red]")
        exit(1)

if __name__ == "__main__":
    main()