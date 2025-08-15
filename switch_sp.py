#!/usr/bin/env python3
"""
Switch between Service Principals
"""

import os
import shutil
from datetime import datetime

def backup_current_env():
    """Backup current .env file"""
    if os.path.exists('.env'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'.env.backup_{timestamp}'
        shutil.copy('.env', backup_name)
        print(f"✅ Current .env backed up as {backup_name}")
        return backup_name
    return None

def create_avd_env():
    """Create .env file for AVD Service Principal"""
    print("🔧 Creating .env file for AVD Service Principal...")
    
    print("\nPlease provide the following information:")
    tenant_id = input("Tenant ID: ").strip()
    client_id = input("Client ID (Application ID): ").strip()
    client_secret = input("Client Secret: ").strip()
    subscription_id = input("Subscription ID: ").strip()
    
    env_content = f"""# AVD Management Service Principal
AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
AZURE_SUBSCRIPTION_ID={subscription_id}

# Web Application Settings
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_ENV=development
PORT=5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created for AVD Service Principal")

def switch_to_original():
    """Switch back to original Service Principal"""
    print("🔄 Switching back to original Service Principal...")
    
    # List available backups
    backups = [f for f in os.listdir('.') if f.startswith('.env.backup_')]
    
    if not backups:
        print("❌ No backup files found")
        return
    
    print("\nAvailable backups:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
    
    try:
        choice = int(input("\nSelect backup to restore (number): ")) - 1
        if 0 <= choice < len(backups):
            shutil.copy(backups[choice], '.env')
            print(f"✅ Restored {backups[choice]}")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input")

def main():
    print("🔄 Service Principal Switcher")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Create AVD Service Principal .env")
        print("2. Switch back to original Service Principal")
        print("3. Test current Service Principal")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            backup_current_env()
            create_avd_env()
        elif choice == '2':
            switch_to_original()
        elif choice == '3':
            print("\nTesting current Service Principal...")
            os.system('python test_avd_sp.py')
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
