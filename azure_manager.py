#!/usr/bin/env python3
"""
Azure Portal Management Tool
Provides comprehensive Azure resource management capabilities via API
"""

import os
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

from azure.identity import (
    ClientSecretCredential, 
    InteractiveBrowserCredential,
    DefaultAzureCredential,
    ManagedIdentityCredential
)
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.costmanagement import CostManagementClient
from azure.core.exceptions import AzureError, ClientAuthenticationError

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class AzureManager:
    """Main class for Azure resource management"""
    
    def __init__(self, subscription_id: Optional[str] = None):
        self.subscription_id = subscription_id or os.getenv('AZURE_SUBSCRIPTION_ID')
        self.credential = None
        self.clients = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        if not self.subscription_id:
            raise ValueError("Azure subscription ID is required. Set AZURE_SUBSCRIPTION_ID environment variable or pass it to constructor.")
    
    def authenticate(self, auth_method: str = "auto") -> bool:
        """
        Authenticate with Azure using the specified method
        
        Args:
            auth_method: "service_principal", "interactive", "managed_identity", or "auto"
        
        Returns:
            bool: True if authentication successful
        """
        try:
            with console.status("[bold green]Authenticating with Azure..."):
                if auth_method == "service_principal" or (auth_method == "auto" and self._has_service_principal_creds()):
                    self.credential = self._get_service_principal_credential()
                elif auth_method == "interactive":
                    self.credential = InteractiveBrowserCredential()
                elif auth_method == "managed_identity":
                    self.credential = ManagedIdentityCredential()
                else:
                    # Try default credential (includes managed identity, environment variables, etc.)
                    self.credential = DefaultAzureCredential()
                
                # Test the credential
                self._test_credential()
                console.print("[bold green]✓ Authentication successful![/bold green]")
                return True
                
        except Exception as e:
            console.print(f"[bold red]✗ Authentication failed: {str(e)}[/bold red]")
            self.logger.error(f"Authentication error: {e}")
            return False
    
    def _has_service_principal_creds(self) -> bool:
        """Check if service principal credentials are available"""
        return all([
            os.getenv('AZURE_TENANT_ID'),
            os.getenv('AZURE_CLIENT_ID'),
            os.getenv('AZURE_CLIENT_SECRET')
        ])
    
    def _get_service_principal_credential(self) -> ClientSecretCredential:
        """Get service principal credential"""
        return ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
    
    def _test_credential(self):
        """Test the credential by making a simple API call"""
        client = ResourceManagementClient(self.credential, self.subscription_id)
        # Try to list resource groups to test the credential
        list(client.resource_groups.list())
    
    def _get_client(self, client_type: str):
        """Get or create an Azure management client"""
        if client_type not in self.clients:
            if client_type == "resource":
                self.clients[client_type] = ResourceManagementClient(self.credential, self.subscription_id)
            elif client_type == "compute":
                self.clients[client_type] = ComputeManagementClient(self.credential, self.subscription_id)
            elif client_type == "network":
                self.clients[client_type] = NetworkManagementClient(self.credential, self.subscription_id)
            elif client_type == "storage":
                self.clients[client_type] = StorageManagementClient(self.credential, self.subscription_id)
            elif client_type == "web":
                self.clients[client_type] = WebSiteManagementClient(self.credential, self.subscription_id)
            elif client_type == "sql":
                self.clients[client_type] = SqlManagementClient(self.credential, self.subscription_id)
            elif client_type == "monitor":
                self.clients[client_type] = MonitorManagementClient(self.credential, self.subscription_id)
            elif client_type == "cost":
                self.clients[client_type] = CostManagementClient(self.credential, self.subscription_id)
        
        return self.clients[client_type]
    
    def list_resource_groups(self) -> List[Dict[str, Any]]:
        """List all resource groups in the subscription"""
        try:
            client = self._get_client("resource")
            resource_groups = []
            
            for rg in client.resource_groups.list():
                resource_groups.append({
                    'name': rg.name,
                    'location': rg.location,
                    'tags': rg.tags or {},
                    'properties': {
                        'provisioning_state': rg.properties.provisioning_state
                    }
                })
            
            return resource_groups
            
        except Exception as e:
            console.print(f"[bold red]Error listing resource groups: {str(e)}[/bold red]")
            return []
    
    def list_virtual_machines(self, resource_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """List virtual machines"""
        try:
            client = self._get_client("compute")
            vms = []
            
            if resource_group:
                vm_list = client.virtual_machines.list(resource_group)
            else:
                vm_list = client.virtual_machines.list_all()
            
            for vm in vm_list:
                try:
                    # Handle os_type properly - it can be a string or an object
                    os_type = 'Unknown'
                    if vm.storage_profile.os_disk.os_type:
                        if hasattr(vm.storage_profile.os_disk.os_type, 'value'):
                            os_type = vm.storage_profile.os_disk.os_type.value
                        else:
                            os_type = str(vm.storage_profile.os_disk.os_type)
                    
                    vms.append({
                        'name': vm.name,
                        'resource_group': vm.id.split('/')[4],
                        'location': vm.location,
                        'vm_size': vm.hardware_profile.vm_size,
                        'os_type': os_type,
                        'power_state': self._get_vm_power_state(client, vm.id.split('/')[4], vm.name),
                        'tags': vm.tags or {}
                    })
                except Exception as vm_error:
                    console.print(f"[yellow]Warning: Error processing VM {vm.name if hasattr(vm, 'name') else 'Unknown'}: {str(vm_error)}[/yellow]")
                    continue
            
            return vms
            
        except Exception as e:
            console.print(f"[bold red]Error listing VMs: {str(e)}[/bold red]")
            return []
    
    def _get_vm_power_state(self, client, resource_group: str, vm_name: str) -> str:
        """Get VM power state"""
        try:
            vm_instance = client.virtual_machines.get(resource_group, vm_name, expand='instanceView')
            if vm_instance.instance_view and vm_instance.instance_view.statuses:
                for status in vm_instance.instance_view.statuses:
                    if status.code.startswith('PowerState/'):
                        return status.code.split('/')[1]
            return 'Unknown'
        except:
            return 'Unknown'
    
    def list_storage_accounts(self, resource_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """List storage accounts"""
        try:
            client = self._get_client("storage")
            accounts = []
            
            if resource_group:
                account_list = client.storage_accounts.list_by_resource_group(resource_group)
            else:
                account_list = client.storage_accounts.list()
            
            for account in account_list:
                accounts.append({
                    'name': account.name,
                    'resource_group': account.id.split('/')[4],
                    'location': account.location,
                    'sku': account.sku.name,
                    'kind': account.kind,
                    'status': account.status_of_primary,
                    'tags': account.tags or {}
                })
            
            return accounts
            
        except Exception as e:
            console.print(f"[bold red]Error listing storage accounts: {str(e)}[/bold red]")
            return []
    
    def list_web_apps(self, resource_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """List web apps"""
        try:
            client = self._get_client("web")
            apps = []
            
            if resource_group:
                app_list = client.web_apps.list_by_resource_group(resource_group)
            else:
                app_list = client.web_apps.list()
            
            for app in app_list:
                apps.append({
                    'name': app.name,
                    'resource_group': app.id.split('/')[4],
                    'location': app.location,
                    'state': app.state,
                    'host_names': app.host_names,
                    'default_host_name': app.default_host_name,
                    'tags': app.tags or {}
                })
            
            return apps
            
        except Exception as e:
            console.print(f"[bold red]Error listing web apps: {str(e)}[/bold red]")
            return []
    
    def get_subscription_info(self) -> Dict[str, Any]:
        """Get subscription information"""
        try:
            # For now, return basic info since ResourceManagementClient doesn't have subscriptions
            # We can enhance this later with a dedicated subscription client if needed
            return {
                'id': self.subscription_id,
                'name': 'Subscription',  # We'll get this from the subscription ID
                'state': 'Enabled'  # Assuming enabled if we can authenticate
            }
            
        except Exception as e:
            console.print(f"[bold red]Error getting subscription info: {str(e)}[/bold red]")
            return {}
    
    def display_dashboard(self):
        """Display a comprehensive dashboard of Azure resources"""
        console.print(Panel.fit("[bold blue]Azure Resource Dashboard[/bold blue]", border_style="blue"))
        
        # Get subscription info
        sub_info = self.get_subscription_info()
        if sub_info:
            console.print(f"[bold]Subscription:[/bold] {sub_info.get('name', 'Unknown')} ({sub_info.get('id', 'Unknown')})")
            console.print(f"[bold]State:[/bold] {sub_info.get('state', 'Unknown')}")
            console.print()
        
        # Resource Groups
        with console.status("[bold green]Loading resource groups..."):
            resource_groups = self.list_resource_groups()
        
        if resource_groups:
            table = Table(title="Resource Groups")
            table.add_column("Name", style="cyan")
            table.add_column("Location", style="magenta")
            table.add_column("State", style="green")
            table.add_column("Tags", style="yellow")
            
            for rg in resource_groups[:10]:  # Show first 10
                tags_str = ", ".join([f"{k}={v}" for k, v in list(rg['tags'].items())[:3]])
                table.add_row(
                    rg['name'],
                    rg['location'],
                    rg['properties']['provisioning_state'],
                    tags_str[:50] + "..." if len(tags_str) > 50 else tags_str
                )
            
            console.print(table)
            if len(resource_groups) > 10:
                console.print(f"[dim]... and {len(resource_groups) - 10} more resource groups[/dim]")
        
        # Virtual Machines
        with console.status("[bold green]Loading virtual machines..."):
            vms = self.list_virtual_machines()
        
        if vms:
            table = Table(title="Virtual Machines")
            table.add_column("Name", style="cyan")
            table.add_column("Resource Group", style="blue")
            table.add_column("Size", style="magenta")
            table.add_column("OS", style="green")
            table.add_column("Power State", style="yellow")
            
            for vm in vms[:10]:  # Show first 10
                table.add_row(
                    vm['name'],
                    vm['resource_group'],
                    vm['vm_size'],
                    vm['os_type'],
                    vm['power_state']
                )
            
            console.print(table)
            if len(vms) > 10:
                console.print(f"[dim]... and {len(vms) - 10} more VMs[/dim]")
        
        # Storage Accounts
        with console.status("[bold green]Loading storage accounts..."):
            storage_accounts = self.list_storage_accounts()
        
        if storage_accounts:
            table = Table(title="Storage Accounts")
            table.add_column("Name", style="cyan")
            table.add_column("Resource Group", style="blue")
            table.add_column("SKU", style="magenta")
            table.add_column("Status", style="green")
            
            for account in storage_accounts[:10]:  # Show first 10
                table.add_row(
                    account['name'],
                    account['resource_group'],
                    account['sku'],
                    account['status']
                )
            
            console.print(table)
            if len(storage_accounts) > 10:
                console.print(f"[dim]... and {len(storage_accounts) - 10} more storage accounts[/dim]")
        
        # Web Apps
        with console.status("[bold green]Loading web apps..."):
            web_apps = self.list_web_apps()
        
        if web_apps:
            table = Table(title="Web Apps")
            table.add_column("Name", style="cyan")
            table.add_column("Resource Group", style="blue")
            table.add_column("State", style="magenta")
            table.add_column("Host Name", style="green")
            
            for app in web_apps[:10]:  # Show first 10
                table.add_row(
                    app['name'],
                    app['resource_group'],
                    app['state'],
                    app['default_host_name'] or "N/A"
                )
            
            console.print(table)
            if len(web_apps) > 10:
                console.print(f"[dim]... and {len(web_apps) - 10} more web apps[/dim]")

if __name__ == "__main__":
    # Example usage
    try:
        manager = AzureManager()
        if manager.authenticate():
            manager.display_dashboard()
        else:
            console.print("[bold red]Failed to authenticate with Azure. Please check your credentials.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
