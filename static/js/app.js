// Azure Management Tool - Frontend JavaScript

class AzureDashboard {
    constructor() {
        this.apiBase = '/api';
        this.resources = {};
        this.filters = {
            search: '',
            resourceType: '',
            location: '',
            status: ''
        };
        this.init();
    }

    async init() {
        try {
            await this.checkAuth();
            await this.loadDashboard();
            this.setupEventListeners();
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError('Failed to initialize dashboard');
        }
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filters.search = e.target.value.toLowerCase();
                this.applyFilters();
            });
        }

        // Filter dropdowns
        const resourceTypeFilter = document.getElementById('resourceTypeFilter');
        if (resourceTypeFilter) {
            resourceTypeFilter.addEventListener('change', (e) => {
                this.filters.resourceType = e.target.value;
                this.applyFilters();
            });
        }

        const locationFilter = document.getElementById('locationFilter');
        if (locationFilter) {
            locationFilter.addEventListener('change', (e) => {
                this.filters.location = e.target.value;
                this.applyFilters();
            });
        }

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    }

    applyFilters() {
        const resourceCards = document.querySelectorAll('.resource-card');
        
        resourceCards.forEach(card => {
            let show = true;
            
            // Search filter
            if (this.filters.search) {
                const text = card.textContent.toLowerCase();
                if (!text.includes(this.filters.search)) {
                    show = false;
                }
            }
            
            // Resource type filter
            if (this.filters.resourceType && show) {
                const resourceType = card.dataset.resourceType;
                if (resourceType !== this.filters.resourceType) {
                    show = false;
                }
            }
            
            // Location filter
            if (this.filters.location && show) {
                const location = card.dataset.location;
                if (location !== this.filters.location) {
                    show = false;
                }
            }
            
            card.style.display = show ? 'block' : 'none';
        });
        
        this.updateFilterCounts();
    }

    updateFilterCounts() {
        const visibleCards = document.querySelectorAll('.resource-card[style*="block"], .resource-card:not([style*="none"])');
        const totalCards = document.querySelectorAll('.resource-card').length;
        
        const filterInfo = document.getElementById('filterInfo');
        if (filterInfo) {
            filterInfo.textContent = `Showing ${visibleCards.length} of ${totalCards} resources`;
        }
    }

    toggleTheme() {
        const body = document.body;
        const isDark = body.classList.contains('dark-theme');
        
        if (isDark) {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        } else {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        }
        
        this.updateThemeIcon();
    }

    updateThemeIcon() {
        const themeToggle = document.getElementById('themeToggle');
        const isDark = document.body.classList.contains('dark-theme');
        
        if (themeToggle) {
            themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }
    }

    loadSavedTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
        this.updateThemeIcon();
    }

    async checkAuth() {
        try {
            const response = await fetch(`${this.apiBase}/auth/status`);
            const data = await response.json();
            
            const authStatus = document.getElementById('auth-status');
            
            if (data.authenticated) {
                authStatus.className = 'auth-status authenticated';
                authStatus.innerHTML = '<i class="fas fa-check-circle"></i> Connected to Azure';
            } else {
                authStatus.className = 'auth-status error';
                authStatus.innerHTML = '<i class="fas fa-times-circle"></i> Not Authenticated';
                throw new Error(data.error || 'Authentication failed');
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            throw error;
        }
    }

    async loadDashboard() {
        try {
            const response = await fetch(`${this.apiBase}/dashboard`);
            const data = await response.json();
            
            if (response.ok) {
                this.displayDashboard(data);
            } else {
                throw new Error(data.error || 'Failed to load dashboard');
            }
        } catch (error) {
            console.error('Dashboard load failed:', error);
            this.showError(error.message);
        }
    }

    displayDashboard(data) {
        // Hide loading, show dashboard
        document.getElementById('loading').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        
        // Store resource data for modal access
        this.resources = data;
        
        // Update stats
        this.updateStats(data);
        
        // Display resources
        this.displayResourceGroups(data.resource_groups);
        this.displayVirtualMachines(data.virtual_machines);
        this.displayStorageAccounts(data.storage_accounts);
        this.displayWebApps(data.web_apps);
        
        // Load saved theme
        this.loadSavedTheme();
    }

    updateStats(data) {
        document.getElementById('vm-count').textContent = data.virtual_machines?.length || 0;
        document.getElementById('storage-count').textContent = data.storage_accounts?.length || 0;
        document.getElementById('webapp-count').textContent = data.web_apps?.length || 0;
        document.getElementById('rg-count').textContent = data.resource_groups?.length || 0;
        
        // Add estimated cost (placeholder)
        const estimatedCost = this.calculateEstimatedCost(data);
        document.getElementById('cost-display').textContent = `$${estimatedCost}/month`;
    }

    calculateEstimatedCost(data) {
        // Simple cost estimation (placeholder)
        let cost = 0;
        cost += (data.virtual_machines?.length || 0) * 50; // $50 per VM
        cost += (data.storage_accounts?.length || 0) * 20; // $20 per storage account
        cost += (data.web_apps?.length || 0) * 30; // $30 per web app
        return cost.toLocaleString();
    }

    displayResourceGroups(resourceGroups) {
        const container = document.getElementById('resource-groups');
        
        if (!resourceGroups || resourceGroups.length === 0) {
            container.innerHTML = '<div class="resource-card"><p>No resource groups found</p></div>';
            return;
        }

        container.innerHTML = resourceGroups.map(rg => `
            <div class="resource-card" data-resource-type="resourcegroup" data-location="${rg.location}">
                <h3><i class="fas fa-folder"></i> ${rg.name}</h3>
                <p><strong>Location:</strong> ${rg.location}</p>
                <p><strong>State:</strong> <span class="status ${rg.properties.provisioning_state.toLowerCase()}">${rg.properties.provisioning_state}</span></p>
                <p><strong>Tags:</strong> ${Object.keys(rg.tags || {}).length} tags</p>
                <div class="resource-actions">
                    <button onclick="dashboard.viewResource('${rg.name}', 'resourcegroup')" class="btn-secondary">View Details</button>
                </div>
            </div>
        `).join('');
    }

    displayVirtualMachines(vms) {
        const container = document.getElementById('virtual-machines');
        
        if (!vms || vms.length === 0) {
            container.innerHTML = '<div class="resource-card"><p>No virtual machines found</p></div>';
            return;
        }

        container.innerHTML = vms.map(vm => `
            <div class="resource-card" data-resource-type="vm" data-location="${vm.location}">
                <h3><i class="fas fa-server"></i> ${vm.name}</h3>
                <p><strong>Resource Group:</strong> ${vm.resource_group}</p>
                <p><strong>Size:</strong> ${vm.vm_size}</p>
                <p><strong>OS:</strong> ${vm.os_type}</p>
                <p><strong>Status:</strong> <span class="status ${vm.power_state.toLowerCase()}">${vm.power_state}</span></p>
                <div class="resource-actions">
                    <button onclick="dashboard.startVM('${vm.name}', '${vm.resource_group}')" class="btn-success" ${vm.power_state === 'running' ? 'disabled' : ''}>Start</button>
                    <button onclick="dashboard.stopVM('${vm.name}', '${vm.resource_group}')" class="btn-warning" ${vm.power_state === 'stopped' ? 'disabled' : ''}>Stop</button>
                    <button onclick="dashboard.restartVM('${vm.name}', '${vm.resource_group}')" class="btn-info">Restart</button>
                    <button onclick="dashboard.viewResource('${vm.name}', 'vm')" class="btn-secondary">Details</button>
                </div>
            </div>
        `).join('');
    }

    displayStorageAccounts(accounts) {
        const container = document.getElementById('storage-accounts');
        
        if (!accounts || accounts.length === 0) {
            container.innerHTML = '<div class="resource-card"><p>No storage accounts found</p></div>';
            return;
        }

        container.innerHTML = accounts.map(account => `
            <div class="resource-card" data-resource-type="storage" data-location="${account.location}">
                <h3><i class="fas fa-database"></i> ${account.name}</h3>
                <p><strong>Resource Group:</strong> ${account.resource_group}</p>
                <p><strong>SKU:</strong> ${account.sku}</p>
                <p><strong>Kind:</strong> ${account.kind}</p>
                <p><strong>Status:</strong> <span class="status ${account.status.toLowerCase()}">${account.status}</span></p>
                <div class="resource-actions">
                    <button onclick="dashboard.viewResource('${account.name}', 'storage')" class="btn-secondary">View Details</button>
                </div>
            </div>
        `).join('');
    }

    displayWebApps(apps) {
        const container = document.getElementById('web-apps');
        
        if (!apps || apps.length === 0) {
            container.innerHTML = '<div class="resource-card"><p>No web apps found</p></div>';
            return;
        }

        container.innerHTML = apps.map(app => `
            <div class="resource-card" data-resource-type="webapp" data-location="${app.location}">
                <h3><i class="fas fa-globe"></i> ${app.name}</h3>
                <p><strong>Resource Group:</strong> ${app.resource_group}</p>
                <p><strong>State:</strong> <span class="status ${app.state.toLowerCase()}">${app.state}</span></p>
                <p><strong>Host Name:</strong> ${app.default_host_name || 'N/A'}</p>
                <div class="resource-actions">
                    <button onclick="dashboard.viewResource('${app.name}', 'webapp')" class="btn-secondary">View Details</button>
                </div>
            </div>
        `).join('');
    }

    // Resource Actions
    async startVM(vmName, resourceGroup) {
        try {
            const response = await fetch(`${this.apiBase}/resources/vms/${vmName}/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resource_group: resourceGroup })
            });
            
            if (response.ok) {
                this.showNotification('VM started successfully', 'success');
                await this.loadDashboard(); // Refresh data
            } else {
                throw new Error('Failed to start VM');
            }
        } catch (error) {
            this.showNotification('Failed to start VM: ' + error.message, 'error');
        }
    }

    async stopVM(vmName, resourceGroup) {
        try {
            const response = await fetch(`${this.apiBase}/resources/vms/${vmName}/stop`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resource_group: resourceGroup })
            });
            
            if (response.ok) {
                this.showNotification('VM stopped successfully', 'success');
                await this.loadDashboard(); // Refresh data
            } else {
                throw new Error('Failed to stop VM');
            }
        } catch (error) {
            this.showNotification('Failed to stop VM: ' + error.message, 'error');
        }
    }

    async restartVM(vmName, resourceGroup) {
        try {
            const response = await fetch(`${this.apiBase}/resources/vms/${vmName}/restart`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resource_group: resourceGroup })
            });
            
            if (response.ok) {
                this.showNotification('VM restarted successfully', 'success');
                await this.loadDashboard(); // Refresh data
            } else {
                throw new Error('Failed to restart VM');
            }
        } catch (error) {
            this.showNotification('Failed to restart VM: ' + error.message, 'error');
        }
    }

    viewResource(resourceName, resourceType) {
        // Find the resource data
        let resourceData = null;
        
        switch(resourceType) {
            case 'vm':
                resourceData = this.findResourceByName(this.resources.virtual_machines, resourceName);
                break;
            case 'storage':
                resourceData = this.findResourceByName(this.resources.storage_accounts, resourceName);
                break;
            case 'webapp':
                resourceData = this.findResourceByName(this.resources.web_apps, resourceName);
                break;
            case 'resourcegroup':
                resourceData = this.findResourceByName(this.resources.resource_groups, resourceName);
                break;
        }
        
        if (resourceData) {
            this.showResourceModal(resourceName, resourceType, resourceData);
        } else {
            this.showNotification(`Resource ${resourceName} not found`, 'error');
        }
    }

    findResourceByName(resourceList, name) {
        if (!resourceList) return null;
        return resourceList.find(resource => resource.name === name);
    }

    showResourceModal(resourceName, resourceType, resourceData) {
        const modal = document.getElementById('resourceModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        // Set title with icon
        const icons = {
            'vm': 'fas fa-server',
            'storage': 'fas fa-database',
            'webapp': 'fas fa-globe',
            'resourcegroup': 'fas fa-folder'
        };
        
        modalTitle.innerHTML = `<i class="${icons[resourceType]}"></i> ${resourceName}`;
        
        // Generate detailed content based on resource type
        let content = '';
        
        switch(resourceType) {
            case 'vm':
                content = this.generateVMDetails(resourceData);
                break;
            case 'storage':
                content = this.generateStorageDetails(resourceData);
                break;
            case 'webapp':
                content = this.generateWebAppDetails(resourceData);
                break;
            case 'resourcegroup':
                content = this.generateResourceGroupDetails(resourceData);
                break;
        }
        
        modalBody.innerHTML = content;
        modal.style.display = 'block';
        
        // Close modal when clicking outside
        modal.onclick = (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        };
    }

    generateVMDetails(vm) {
        return `
            <div class="resource-details">
                <div class="detail-section">
                    <h3><i class="fas fa-info-circle"></i> Basic Information</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">${vm.name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Resource Group</span>
                            <span class="detail-value">${vm.resource_group}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Location</span>
                            <span class="detail-value">${vm.location}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Status</span>
                            <span class="detail-value status ${vm.power_state.toLowerCase()}">${vm.power_state}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h3><i class="fas fa-cogs"></i> Configuration</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">VM Size</span>
                            <span class="detail-value">${vm.vm_size}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Operating System</span>
                            <span class="detail-value">${vm.os_type}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Provisioning State</span>
                            <span class="detail-value">${vm.provisioning_state || 'N/A'}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h3><i class="fas fa-tools"></i> Actions</h3>
                    <div class="resource-actions">
                        <button onclick="dashboard.startVM('${vm.name}', '${vm.resource_group}')" class="btn-success" ${vm.power_state === 'running' ? 'disabled' : ''}>Start VM</button>
                        <button onclick="dashboard.stopVM('${vm.name}', '${vm.resource_group}')" class="btn-warning" ${vm.power_state === 'stopped' ? 'disabled' : ''}>Stop VM</button>
                        <button onclick="dashboard.restartVM('${vm.name}', '${vm.resource_group}')" class="btn-info">Restart VM</button>
                    </div>
                </div>
            </div>
        `;
    }

    generateStorageDetails(storage) {
        return `
            <div class="resource-details">
                <div class="detail-section">
                    <h3><i class="fas fa-info-circle"></i> Basic Information</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">${storage.name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Resource Group</span>
                            <span class="detail-value">${storage.resource_group}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Location</span>
                            <span class="detail-value">${storage.location}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Status</span>
                            <span class="detail-value status ${storage.status.toLowerCase()}">${storage.status}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h3><i class="fas fa-cogs"></i> Configuration</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">SKU</span>
                            <span class="detail-value">${storage.sku}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Kind</span>
                            <span class="detail-value">${storage.kind}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Access Tier</span>
                            <span class="detail-value">${storage.access_tier || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    generateWebAppDetails(webapp) {
        return `
            <div class="resource-details">
                <div class="detail-section">
                    <h3><i class="fas fa-info-circle"></i> Basic Information</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">${webapp.name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Resource Group</span>
                            <span class="detail-value">${webapp.resource_group}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Location</span>
                            <span class="detail-value">${webapp.location}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">State</span>
                            <span class="detail-value status ${webapp.state.toLowerCase()}">${webapp.state}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h3><i class="fas fa-link"></i> Access Information</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Host Name</span>
                            <span class="detail-value">${webapp.default_host_name || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">URL</span>
                            <span class="detail-value">
                                ${webapp.default_host_name ? `<a href="https://${webapp.default_host_name}" target="_blank">https://${webapp.default_host_name}</a>` : 'N/A'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    generateResourceGroupDetails(rg) {
        const tags = rg.tags || {};
        const tagElements = Object.entries(tags).map(([key, value]) => 
            `<span class="tag">${key}: ${value}</span>`
        ).join('');
        
        return `
            <div class="resource-details">
                <div class="detail-section">
                    <h3><i class="fas fa-info-circle"></i> Basic Information</h3>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">${rg.name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Location</span>
                            <span class="detail-value">${rg.location}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Provisioning State</span>
                            <span class="detail-value status ${rg.properties.provisioning_state.toLowerCase()}">${rg.properties.provisioning_state}</span>
                        </div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h3><i class="fas fa-tags"></i> Tags</h3>
                    <div class="tags-container">
                        ${tagElements.length > 0 ? tagElements : '<span class="detail-value">No tags assigned</span>'}
                    </div>
                </div>
            </div>
        `;
    }

    closeModal() {
        const modal = document.getElementById('resourceModal');
        modal.style.display = 'none';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="notification-close">×</button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    showError(message) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('dashboard').style.display = 'none';
        
        const errorContainer = document.getElementById('error');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorContainer.style.display = 'block';
        
        // Update auth status
        const authStatus = document.getElementById('auth-status');
        authStatus.className = 'auth-status error';
        authStatus.innerHTML = '<i class="fas fa-times-circle"></i> Error';
    }
}

// Initialize the dashboard when the page loads
let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new AzureDashboard();
});
