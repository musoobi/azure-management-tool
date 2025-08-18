#!/usr/bin/env python3
"""
Azure Management Web Application
Flask-based web interface for Azure resource management
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from dotenv import load_dotenv
from azure_manager import AzureManager
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Azure manager instance
azure_manager = None

def get_azure_manager():
    """Get or create Azure manager instance"""
    global azure_manager
    if azure_manager is None:
        try:
            azure_manager = AzureManager()
            if not azure_manager.authenticate('service_principal'):
                azure_manager = None
        except Exception as e:
            logger.error(f"Failed to initialize Azure manager: {e}")
            azure_manager = None
    return azure_manager

def reset_azure_manager():
    """Reset the Azure manager instance to force re-authentication"""
    global azure_manager
    azure_manager = None

@app.route('/')
def index():
    """Redirect to settings page by default"""
    return redirect(url_for('settings'))

@app.route('/dashboard')
def dashboard_page():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/settings')
def settings():
    """Settings page for Azure configuration"""
    return render_template('settings.html')

@app.route('/api/settings/azure')
def get_azure_settings():
    """Get current Azure configuration settings - returns blank values for security"""
    try:
        settings = {
            'subscription_id': '',
            'tenant_id': '',
            'client_id': '',
            'client_secret': '',
            'default_location': 'East US',
            'default_resource_group': ''
        }
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Error getting Azure settings: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/azure', methods=['POST'])
def update_azure_settings():
    """Update Azure configuration settings"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subscription_id', 'tenant_id', 'client_id', 'client_secret']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Read current .env file
        env_file = '.env'
        env_content = []
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.readlines()
        
        # Update or add Azure configuration
        azure_config = {
            'AZURE_SUBSCRIPTION_ID': data['subscription_id'],
            'AZURE_TENANT_ID': data['tenant_id'],
            'AZURE_CLIENT_ID': data['client_id'],
            'AZURE_CLIENT_SECRET': data['client_secret'],
            'AZURE_DEFAULT_LOCATION': data.get('default_location', 'East US'),
            'AZURE_DEFAULT_RESOURCE_GROUP': data.get('default_resource_group', '')
        }
        
        # Remove existing Azure config lines
        env_content = [line for line in env_content if not line.startswith('AZURE_')]
        
        # Add new Azure configuration
        for key, value in azure_config.items():
            env_content.append(f'{key}={value}\n')
        
        # Write updated .env file
        with open(env_file, 'w') as f:
            f.writelines(env_content)
        
        # Reset Azure manager to force re-authentication with new credentials
        reset_azure_manager()
        
        # Test the new configuration
        try:
            test_manager = AzureManager()
            if test_manager.authenticate('service_principal'):
                return jsonify({
                    'success': True,
                    'message': 'Azure configuration updated successfully and connection verified!'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Configuration updated but authentication failed. Please verify your credentials.'
                }), 400
        except Exception as auth_error:
            return jsonify({
                'success': False,
                'error': f'Configuration updated but authentication failed: {str(auth_error)}'
            }), 400
            
    except Exception as e:
        logger.error(f"Error updating Azure settings: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings/test-connection')
def test_azure_connection():
    """Test Azure connection with current settings"""
    try:
        reset_azure_manager()  # Force fresh authentication
        manager = get_azure_manager()
        
        if manager:
            # Try to get subscription info to verify connection
            sub_info = manager.get_subscription_info()
            return jsonify({
                'success': True,
                'message': 'Azure connection successful!',
                'subscription': sub_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to authenticate with Azure. Please check your credentials.'
            }), 400
            
    except Exception as e:
        logger.error(f"Error testing Azure connection: {e}")
        return jsonify({
            'success': False,
            'error': f'Connection test failed: {str(e)}'
        }), 500

@app.route('/api/auth/status')
def auth_status():
    """Check authentication status"""
    manager = get_azure_manager()
    if manager:
        return jsonify({
            'authenticated': True,
            'subscription_id': manager.subscription_id
        })
    return jsonify({
        'authenticated': False,
        'error': 'Not authenticated'
    })

@app.route('/api/dashboard')
def dashboard():
    """Get dashboard data"""
    manager = get_azure_manager()
    if not manager:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get subscription info
        sub_info = manager.get_subscription_info()
        
        # Get resource groups
        resource_groups = manager.list_resource_groups()
        
        # Get virtual machines
        vms = manager.list_virtual_machines()
        
        # Get storage accounts
        storage_accounts = manager.list_storage_accounts()
        
        # Get web apps
        web_apps = manager.list_web_apps()
        
        return jsonify({
            'subscription': sub_info,
            'resource_groups': resource_groups,
            'virtual_machines': vms,
            'storage_accounts': storage_accounts,
            'web_apps': web_apps
        })
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/vms')
def get_vms():
    """Get virtual machines"""
    manager = get_azure_manager()
    if not manager:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        resource_group = request.args.get('resource_group')
        vms = manager.list_virtual_machines(resource_group)
        return jsonify({'vms': vms})
    except Exception as e:
        logger.error(f"Error getting VMs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/storage')
def get_storage():
    """Get storage accounts"""
    manager = get_azure_manager()
    if not manager:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        resource_group = request.args.get('resource_group')
        accounts = manager.list_storage_accounts(resource_group)
        return jsonify({'storage_accounts': accounts})
    except Exception as e:
        logger.error(f"Error getting storage accounts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/webapps')
def get_webapps():
    """Get web apps"""
    manager = get_azure_manager()
    if not manager:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        resource_group = request.args.get('resource_group')
        apps = manager.list_web_apps(resource_group)
        return jsonify({'web_apps': apps})
    except Exception as e:
        logger.error(f"Error getting web apps: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/resourcegroups')
def get_resource_groups():
    """Get resource groups"""
    manager = get_azure_manager()
    if not manager:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        resource_groups = manager.list_resource_groups()
        return jsonify({'resource_groups': resource_groups})
    except Exception as e:
        logger.error(f"Error getting resource groups: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'azure_connected': get_azure_manager() is not None
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
