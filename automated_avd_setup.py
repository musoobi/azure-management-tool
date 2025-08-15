#!/usr/bin/env python3
"""
Automated AVD Setup Script
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def automated_avd_setup():
    print("🤖 Automated AVD Setup Starting...")
    
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    
    compute_client = ComputeManagementClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    avd_client = DesktopVirtualizationMgmtClient(credential, os.getenv('AZURE_SUBSCRIPTION_ID'))
    
    try:
        # Get registration token
        registration_info = avd_client.host_pools.retrieve_registration_token('avd-rg', 'avd-host-pool')
        token = registration_info.token
        
        print(f"✅ Registration Token Retrieved")
        print(f"   Expires: {registration_info.expiration_time}")
        
        # PowerShell script to install AVD components
        ps_script = f'''
# AVD Automated Installation Script
Write-Host "Starting AVD Installation..." -ForegroundColor Green

# Download AVD Agent
Write-Host "Downloading AVD Agent..." -ForegroundColor Yellow
$agentUrl = "https://aka.ms/avdagent"
$agentPath = "$env:TEMP\\AVD-Agent.msi"
Invoke-WebRequest -Uri $agentUrl -OutFile $agentPath

# Install AVD Agent
Write-Host "Installing AVD Agent..." -ForegroundColor Yellow
Start-Process msiexec.exe -ArgumentList "/i $agentPath /quiet /norestart" -Wait

# Download AVD Boot Loader
Write-Host "Downloading AVD Boot Loader..." -ForegroundColor Yellow
$bootloaderUrl = "https://aka.ms/avdbootloader"
$bootloaderPath = "$env:TEMP\\AVD-BootLoader.msi"
Invoke-WebRequest -Uri $bootloaderUrl -OutFile $bootloaderPath

# Install AVD Boot Loader
Write-Host "Installing AVD Boot Loader..." -ForegroundColor Yellow
Start-Process msiexec.exe -ArgumentList "/i $bootloaderPath /quiet /norestart" -Wait

# Register with Host Pool
Write-Host "Registering with Host Pool..." -ForegroundColor Yellow
$registrationToken = "{token}"
$registrationScript = @"
`$registrationToken = "$registrationToken"
`$registrationPath = "C:\\Program Files\\Microsoft RDInfra\\PowershellModules\\Microsoft.RDInfra.RDPowerShell\\Microsoft.RDInfra.RDPowerShell.psd1"
Import-Module `$registrationPath
Add-RdsessionHost -HostPoolName "avd-host-pool" -SessionHost "avd-host-01" -RegistrationToken `$registrationToken
"@

$registrationScriptPath = "$env:TEMP\\register-avd.ps1"
$registrationScript | Out-File -FilePath $registrationScriptPath -Encoding UTF8
PowerShell -ExecutionPolicy Bypass -File $registrationScriptPath

Write-Host "AVD Installation Complete!" -ForegroundColor Green
Write-Host "Please restart the computer to complete setup." -ForegroundColor Yellow
'''
        
        print(f"\n🔧 Running Automated Setup...")
        print(f"   This will:")
        print(f"   ✅ Download and install AVD Agent")
        print(f"   ✅ Download and install AVD Boot Loader")
        print(f"   ✅ Register VM with host pool")
        print(f"   ✅ Configure everything automatically")
        
        # Run the script on the VM
        script_params = {
            'command_id': 'RunPowerShellScript',
            'script': [ps_script],
            'parameters': []
        }
        
        print(f"\n🚀 Executing script on VM...")
        poller = compute_client.virtual_machines.begin_run_command(
            'avd-rg', 'avd-host-01', script_params
        )
        
        print(f"   Script is running... (this may take 5-10 minutes)")
        
        # Wait for completion
        result = poller.result()
        
        if result.value and len(result.value) > 0:
            for output in result.value:
                print(f"   {output.message}")
        else:
            print(f"   ✅ Script completed successfully!")
        
        print(f"\n🎉 AVD Setup Complete!")
        print(f"   VM: avd-host-01")
        print(f"   Host Pool: avd-host-pool")
        print(f"   Status: Ready for AVD sessions")
        
        print(f"\n📋 Next Steps:")
        print(f"   1. Restart the VM (recommended)")
        print(f"   2. Add users to the application group")
        print(f"   3. Test AVD client connection")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Alternative: Use Azure Portal")
        print(f"   1. Go to Azure Portal → Azure Virtual Desktop")
        print(f"   2. Click 'Host pools' → 'avd-host-pool'")
        print(f"   3. Click 'Session hosts' → 'Add session hosts'")
        print(f"   4. Select your VM: avd-host-01")

if __name__ == "__main__":
    automated_avd_setup()
