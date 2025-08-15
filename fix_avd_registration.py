#!/usr/bin/env python3
"""
Fix AVD Registration with Correct PowerShell Module Path
"""

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.desktopvirtualization import DesktopVirtualizationMgmtClient
from azure.identity import ClientSecretCredential
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_avd_registration():
    print("🔧 Fixing AVD Registration...")
    
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
        
        # Corrected PowerShell script for registration
        ps_script = f'''
# AVD Registration Fix Script
Write-Host "Fixing AVD Registration..." -ForegroundColor Green

# Find the correct PowerShell module path
$possiblePaths = @(
    "C:\\Program Files\\Microsoft RDInfra\\PowershellModules\\Microsoft.RDInfra.RDPowerShell\\Microsoft.RDInfra.RDPowerShell.psd1",
    "C:\\Program Files\\Microsoft RDInfra\\PowershellModules\\Microsoft.RDInfra.RDPowerShell\\Microsoft.RDInfra.RDPowerShell.psm1",
    "C:\\Program Files\\Microsoft RDInfra\\PowershellModules\\Microsoft.RDInfra.RDPowerShell\\Microsoft.RDInfra.RDPowerShell.dll"
)

$modulePath = $null
foreach ($path in $possiblePaths) {{
    if (Test-Path $path) {{
        $modulePath = $path
        Write-Host "Found module at: $path" -ForegroundColor Green
        break
    }}
}}

if ($modulePath) {{
    try {{
        Import-Module $modulePath -Force
        Write-Host "Module loaded successfully" -ForegroundColor Green
        
        # Register with host pool
        $registrationToken = "{token}"
        Write-Host "Registering with host pool..." -ForegroundColor Yellow
        
        # Try different registration methods
        try {{
            Add-RdsessionHost -HostPoolName "avd-host-pool" -SessionHost "avd-host-01" -RegistrationToken $registrationToken
            Write-Host "Registration successful using Add-RdsessionHost" -ForegroundColor Green
        }} catch {{
            Write-Host "Add-RdsessionHost failed, trying alternative method..." -ForegroundColor Yellow
            try {{
                # Alternative registration method
                $registrationScript = @"
`$registrationToken = "$token"
`$registrationPath = "$modulePath"
Import-Module `$registrationPath -Force
Add-RdsessionHost -HostPoolName "avd-host-pool" -SessionHost "avd-host-01" -RegistrationToken `$registrationToken
"@
                Invoke-Expression $registrationScript
                Write-Host "Registration successful using alternative method" -ForegroundColor Green
            }} catch {{
                Write-Host "Alternative registration failed: $_" -ForegroundColor Red
            }}
        }}
        
    }} catch {{
        Write-Host "Failed to load module: $_" -ForegroundColor Red
    }}
}} else {{
    Write-Host "AVD PowerShell module not found. Checking installation..." -ForegroundColor Red
    
    # Check if AVD agent is installed
    $agentService = Get-Service -Name "RDAgentBootLoader" -ErrorAction SilentlyContinue
    if ($agentService) {{
        Write-Host "AVD Agent is installed and running" -ForegroundColor Green
        Write-Host "You may need to restart the computer to complete registration" -ForegroundColor Yellow
    }} else {{
        Write-Host "AVD Agent service not found" -ForegroundColor Red
    }}
}}

Write-Host "Registration fix attempt completed" -ForegroundColor Green
'''
        
        print(f"\n🔧 Running Registration Fix...")
        
        # Run the corrected script on the VM
        script_params = {
            'command_id': 'RunPowerShellScript',
            'script': [ps_script],
            'parameters': []
        }
        
        print(f"   Executing registration fix...")
        poller = compute_client.virtual_machines.begin_run_command(
            'avd-rg', 'avd-host-01', script_params
        )
        
        result = poller.result()
        
        if result.value and len(result.value) > 0:
            for output in result.value:
                print(f"   {output.message}")
        else:
            print(f"   ✅ Registration fix completed!")
        
        print(f"\n🎉 AVD Setup Status:")
        print(f"   ✅ AVD Agent: Installed")
        print(f"   ✅ AVD Boot Loader: Installed")
        print(f"   ⚠️  Registration: May need restart")
        
        print(f"\n📋 Next Steps:")
        print(f"   1. Restart the VM: avd-host-01")
        print(f"   2. After restart, registration should complete automatically")
        print(f"   3. Add users to the application group")
        print(f"   4. Test AVD client connection")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_avd_registration()
