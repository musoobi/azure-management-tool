#!/usr/bin/env python3
"""
Azure CLI Tool
Command-line interface for Azure resource management
"""

import os
import sys
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from azure_manager import AzureManager

# Load environment variables
load_dotenv()

console = Console()

@click.group()
@click.option('--subscription-id', envvar='AZURE_SUBSCRIPTION_ID', help='Azure subscription ID')
@click.option('--auth-method', 
              type=click.Choice(['auto', 'service_principal', 'interactive', 'managed_identity']),
              default='auto',
              help='Authentication method')
@click.pass_context
def cli(ctx, subscription_id, auth_method):
    """Azure Resource Management CLI"""
    ctx.ensure_object(dict)
    ctx.obj['subscription_id'] = subscription_id
    ctx.obj['auth_method'] = auth_method
    
    if not subscription_id:
        console.print("[bold red]Error: Azure subscription ID is required.[/bold red]")
        console.print("Set AZURE_SUBSCRIPTION_ID environment variable or use --subscription-id option.")
        sys.exit(1)

@cli.command()
@click.pass_context
def auth(ctx):
    """Test Azure authentication"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    console.print(Panel.fit("[bold blue]Azure Authentication Test[/bold blue]", border_style="blue"))
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            console.print("[bold green]✓ Authentication successful![/bold green]")
            
            # Get subscription info
            sub_info = manager.get_subscription_info()
            if sub_info:
                console.print(f"\n[bold]Subscription Details:[/bold]")
                console.print(f"  Name: {sub_info.get('name', 'Unknown')}")
                console.print(f"  ID: {sub_info.get('id', 'Unknown')}")
                console.print(f"  State: {sub_info.get('state', 'Unknown')}")
        else:
            console.print("[bold red]✗ Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.pass_context
def dashboard(ctx):
    """Display Azure resource dashboard"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            manager.display_dashboard()
        else:
            console.print("[bold red]Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.group()
@click.pass_context
def list(ctx):
    """List Azure resources"""
    pass

@list.command()
@click.option('--resource-group', help='Filter by resource group')
@click.pass_context
def vms(ctx, resource_group):
    """List virtual machines"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            with console.status("[bold green]Loading virtual machines..."):
                vms = manager.list_virtual_machines(resource_group)
            
            if vms:
                table = Table(title="Virtual Machines")
                table.add_column("Name", style="cyan")
                table.add_column("Resource Group", style="blue")
                table.add_column("Location", style="magenta")
                table.add_column("Size", style="green")
                table.add_column("OS", style="yellow")
                table.add_column("Power State", style="red")
                
                for vm in vms:
                    table.add_row(
                        vm['name'],
                        vm['resource_group'],
                        vm['location'],
                        vm['vm_size'],
                        vm['os_type'],
                        vm['power_state']
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total VMs: {len(vms)}[/dim]")
            else:
                console.print("[yellow]No virtual machines found.[/yellow]")
        else:
            console.print("[bold red]Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@list.command()
@click.option('--resource-group', help='Filter by resource group')
@click.pass_context
def storage(ctx, resource_group):
    """List storage accounts"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            with console.status("[bold green]Loading storage accounts..."):
                accounts = manager.list_storage_accounts(resource_group)
            
            if accounts:
                table = Table(title="Storage Accounts")
                table.add_column("Name", style="cyan")
                table.add_column("Resource Group", style="blue")
                table.add_column("Location", style="magenta")
                table.add_column("SKU", style="green")
                table.add_column("Kind", style="yellow")
                table.add_column("Status", style="red")
                
                for account in accounts:
                    table.add_row(
                        account['name'],
                        account['resource_group'],
                        account['location'],
                        account['sku'],
                        account['kind'],
                        account['status']
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total storage accounts: {len(accounts)}[/dim]")
            else:
                console.print("[yellow]No storage accounts found.[/yellow]")
        else:
            console.print("[bold red]Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@list.command()
@click.option('--resource-group', help='Filter by resource group')
@click.pass_context
def webapps(ctx, resource_group):
    """List web apps"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            with console.status("[bold green]Loading web apps..."):
                apps = manager.list_web_apps(resource_group)
            
            if apps:
                table = Table(title="Web Apps")
                table.add_column("Name", style="cyan")
                table.add_column("Resource Group", style="blue")
                table.add_column("Location", style="magenta")
                table.add_column("State", style="green")
                table.add_column("Host Name", style="yellow")
                
                for app in apps:
                    table.add_row(
                        app['name'],
                        app['resource_group'],
                        app['location'],
                        app['state'],
                        app['default_host_name'] or "N/A"
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total web apps: {len(apps)}[/dim]")
            else:
                console.print("[yellow]No web apps found.[/yellow]")
        else:
            console.print("[bold red]Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@list.command()
@click.pass_context
def resourcegroups(ctx):
    """List resource groups"""
    subscription_id = ctx.obj['subscription_id']
    auth_method = ctx.obj['auth_method']
    
    try:
        manager = AzureManager(subscription_id)
        if manager.authenticate(auth_method):
            with console.status("[bold green]Loading resource groups..."):
                resource_groups = manager.list_resource_groups()
            
            if resource_groups:
                table = Table(title="Resource Groups")
                table.add_column("Name", style="cyan")
                table.add_column("Location", style="blue")
                table.add_column("State", style="magenta")
                table.add_column("Tags", style="green")
                
                for rg in resource_groups:
                    tags_str = ", ".join([f"{k}={v}" for k, v in list(rg['tags'].items())[:3]])
                    table.add_row(
                        rg['name'],
                        rg['location'],
                        rg['properties']['provisioning_state'],
                        tags_str[:50] + "..." if len(tags_str) > 50 else tags_str
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total resource groups: {len(resource_groups)}[/dim]")
            else:
                console.print("[yellow]No resource groups found.[/yellow]")
        else:
            console.print("[bold red]Authentication failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

@cli.command()
@click.pass_context
def setup(ctx):
    """Interactive setup for Azure credentials"""
    console.print(Panel.fit("[bold blue]Azure Setup Wizard[/bold blue]", border_style="blue"))
    
    console.print("This wizard will help you set up Azure authentication.\n")
    
    # Get subscription ID
    subscription_id = Prompt.ask(
        "Enter your Azure subscription ID",
        default=os.getenv('AZURE_SUBSCRIPTION_ID', '')
    )
    
    if not subscription_id:
        console.print("[bold red]Subscription ID is required![/bold red]")
        sys.exit(1)
    
    # Choose authentication method
    auth_method = Prompt.ask(
        "Choose authentication method",
        choices=["service_principal", "interactive", "managed_identity"],
        default="interactive"
    )
    
    if auth_method == "service_principal":
        console.print("\n[bold]Service Principal Setup:[/bold]")
        console.print("You'll need to create a service principal in Azure AD.")
        console.print("Follow these steps:")
        console.print("1. Go to Azure Portal > Azure Active Directory > App registrations")
        console.print("2. Click 'New registration'")
        console.print("3. Give it a name and select 'Accounts in this organizational directory only'")
        console.print("4. After creation, note the Application (client) ID and Directory (tenant) ID")
        console.print("5. Go to 'Certificates & secrets' and create a new client secret")
        console.print("6. Go to 'API permissions' and add 'Azure Service Management' with 'Contributor' role")
        console.print("7. Go to your subscription > Access control (IAM) and add the service principal as Contributor\n")
        
        tenant_id = Prompt.ask("Enter your Azure tenant ID")
        client_id = Prompt.ask("Enter your client ID (Application ID)")
        client_secret = Prompt.ask("Enter your client secret", password=True)
        
        # Create .env file
        env_content = f"""# Azure Configuration
AZURE_SUBSCRIPTION_ID={subscription_id}
AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
AZURE_DEFAULT_LOCATION=East US
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        console.print("[bold green]✓ Configuration saved to .env file[/bold green]")
        
    elif auth_method == "interactive":
        console.print("\n[bold]Interactive Authentication Setup:[/bold]")
        console.print("This will use browser-based authentication.")
        console.print("When you run the tool, it will open your browser for login.\n")
        
        # Create .env file
        env_content = f"""# Azure Configuration
AZURE_SUBSCRIPTION_ID={subscription_id}
AZURE_DEFAULT_LOCATION=East US
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        console.print("[bold green]✓ Configuration saved to .env file[/bold green]")
        
    elif auth_method == "managed_identity":
        console.print("\n[bold]Managed Identity Setup:[/bold]")
        console.print("This is for use within Azure (VMs, App Services, etc.)")
        console.print("The system will automatically use the managed identity.\n")
        
        # Create .env file
        env_content = f"""# Azure Configuration
AZURE_SUBSCRIPTION_ID={subscription_id}
AZURE_DEFAULT_LOCATION=East US
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        console.print("[bold green]✓ Configuration saved to .env file[/bold green]")
    
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"1. Install dependencies: pip install -r requirements.txt")
    console.print(f"2. Test authentication: python azure_cli.py auth")
    console.print(f"3. View dashboard: python azure_cli.py dashboard")

if __name__ == '__main__':
    cli()
