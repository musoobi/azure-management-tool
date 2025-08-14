#!/usr/bin/env python3
"""
Azure Setup Script
Interactive setup for Azure authentication
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

def main():
    """Main setup function"""
    console.print(Panel.fit("[bold blue]Azure Setup Wizard[/bold blue]", border_style="blue"))
    
    console.print("This wizard will help you set up Azure authentication.\n")
    
    # Get subscription ID
    subscription_id = Prompt.ask(
        "Enter your Azure subscription ID",
        default=os.getenv('AZURE_SUBSCRIPTION_ID', '')
    )
    
    if not subscription_id:
        console.print("[bold red]Subscription ID is required![/bold red]")
        console.print("You can find your subscription ID in the Azure portal:")
        console.print("1. Go to portal.azure.com")
        console.print("2. Click on 'Subscriptions' in the left menu")
        console.print("3. Copy the subscription ID\n")
        sys.exit(1)
    
    # Choose authentication method
    auth_method = Prompt.ask(
        "Choose authentication method",
        choices=["interactive", "service_principal", "managed_identity"],
        default="interactive"
    )
    
    if auth_method == "interactive":
        setup_interactive(subscription_id)
    elif auth_method == "service_principal":
        setup_service_principal(subscription_id)
    elif auth_method == "managed_identity":
        setup_managed_identity(subscription_id)
    
    # Test the configuration
    test_configuration()

def setup_interactive(subscription_id):
    """Setup interactive authentication"""
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

def setup_service_principal(subscription_id):
    """Setup service principal authentication"""
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
    
    if Confirm.ask("Have you completed the Azure portal setup?"):
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
    else:
        console.print("[yellow]Please complete the Azure portal setup first, then run this script again.[/yellow]")
        sys.exit(1)

def setup_managed_identity(subscription_id):
    """Setup managed identity authentication"""
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

def test_configuration():
    """Test the configuration"""
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"1. Test authentication: python azure_cli.py auth")
    console.print(f"2. View dashboard: python azure_cli.py dashboard")
    console.print(f"3. List resources: python azure_cli.py list vms")
    
    if Confirm.ask("\nWould you like to test the configuration now?"):
        try:
            from azure_manager import AzureManager
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
            
            if subscription_id:
                manager = AzureManager(subscription_id)
                if manager.authenticate("auto"):
                    console.print("[bold green]✓ Configuration test successful![/bold green]")
                    
                    # Get subscription info
                    sub_info = manager.get_subscription_info()
                    if sub_info:
                        console.print(f"\n[bold]Subscription Details:[/bold]")
                        console.print(f"  Name: {sub_info.get('name', 'Unknown')}")
                        console.print(f"  ID: {sub_info.get('id', 'Unknown')}")
                        console.print(f"  State: {sub_info.get('state', 'Unknown')}")
                else:
                    console.print("[bold red]✗ Configuration test failed![/bold red]")
                    console.print("Please check your credentials and try again.")
            else:
                console.print("[bold red]No subscription ID found in .env file![/bold red]")
                
        except Exception as e:
            console.print(f"[bold red]Error testing configuration: {str(e)}[/bold red]")

if __name__ == "__main__":
    main()
