@extends('layouts.app')

@section('content')
<div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                        🛡️ Vulnerability Management
                    </h1>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="{{ route('vulnerabilities.scanner') }}" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        🔍 New Scan
                    </a>
                    <button onclick="refreshData()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        🔄 Refresh
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Filters -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                    Filter Vulnerabilities
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Severity</label>
                        <select id="severity-filter" onchange="applyFilters()" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                            <option value="">All Severities</option>
                            <option value="critical">🚨 Critical</option>
                            <option value="high">⚠️ High</option>
                            <option value="medium">⚡ Medium</option>
                            <option value="low">ℹ️ Low</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
                        <select id="status-filter" onchange="applyFilters()" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                            <option value="">All Statuses</option>
                            <option value="detected">🔍 Detected</option>
                            <option value="analyzing">🔬 Analyzing</option>
                            <option value="fixing">🔧 Fixing</option>
                            <option value="fixed">✅ Fixed</option>
                            <option value="ignored">🚫 Ignored</option>
                            <option value="false_positive">❌ False Positive</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Date Range</label>
                        <select id="date-filter" onchange="applyFilters()" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                            <option value="">All Time</option>
                            <option value="today">Today</option>
                            <option value="week">This Week</option>
                            <option value="month">This Month</option>
                            <option value="year">This Year</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Search</label>
                        <input type="text" id="search-filter" onkeyup="applyFilters()" placeholder="Search vulnerabilities..." class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Vulnerabilities List -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
                <div class="flex items-center justify-between mb-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                        Detected Vulnerabilities
                    </h3>
                    <div class="text-sm text-gray-500">
                        <span id="vulnerability-count">Loading...</span> vulnerabilities found
                    </div>
                </div>

                <!-- Bulk Actions -->
                <div class="mb-6 flex space-x-4">
                    <button onclick="bulkGenerateFixes()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-medium">
                        🤖 Generate All Fixes
                    </button>
                    <button onclick="bulkUpdateStatus('fixed')" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium">
                        ✅ Mark All Fixed
                    </button>
                    <button onclick="exportResults()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm font-medium">
                        📊 Export Results
                    </button>
                </div>

                <!-- Vulnerabilities Table -->
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    <input type="checkbox" id="select-all" onchange="toggleSelectAll()" class="rounded border-gray-300 text-green-600 shadow-sm focus:border-green-300 focus:ring-green-500">
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Severity
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Title
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Location
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Status
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Detected
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody id="vulnerabilities-tbody" class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            <!-- Vulnerabilities will be loaded here -->
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="mt-6 flex items-center justify-between">
                    <div class="text-sm text-gray-700 dark:text-gray-300">
                        Showing <span id="showing-start">0</span> to <span id="showing-end">0</span> of <span id="total-results">0</span> results
                    </div>
                    <div class="flex space-x-2">
                        <button onclick="previousPage()" id="prev-btn" class="px-3 py-1 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50" disabled>
                            Previous
                        </button>
                        <button onclick="nextPage()" id="next-btn" class="px-3 py-1 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50" disabled>
                            Next
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.vulnerability-row {
    @apply hover:bg-gray-50 dark:hover:bg-gray-700;
}

.severity-critical {
    @apply bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300;
}

.severity-high {
    @apply bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300;
}

.severity-medium {
    @apply bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300;
}

.severity-low {
    @apply bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300;
}

.status-detected {
    @apply bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300;
}

.status-analyzing {
    @apply bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300;
}

.status-fixing {
    @apply bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300;
}

.status-fixed {
    @apply bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300;
}
</style>

<script>
let vulnerabilities = [];
let filteredVulnerabilities = [];
let currentPage = 1;
let itemsPerPage = 10;

// Load vulnerabilities on page load
document.addEventListener('DOMContentLoaded', loadVulnerabilities);

async function loadVulnerabilities() {
    try {
        const response = await fetch('/api/v1/vulnerabilities');
        vulnerabilities = await response.json();
        filteredVulnerabilities = [...vulnerabilities];
        renderVulnerabilities();
    } catch (error) {
        console.error('Failed to load vulnerabilities:', error);
    }
}

function applyFilters() {
    const severityFilter = document.getElementById('severity-filter').value;
    const statusFilter = document.getElementById('status-filter').value;
    const dateFilter = document.getElementById('date-filter').value;
    const searchTerm = document.getElementById('search-filter').value.toLowerCase();

    filteredVulnerabilities = vulnerabilities.filter(vuln => {
        // Severity filter
        if (severityFilter && vuln.severity !== severityFilter) return false;
        
        // Status filter
        if (statusFilter && vuln.status !== statusFilter) return false;
        
        // Date filter
        if (dateFilter) {
            const detectedDate = new Date(vuln.detected_at);
            const now = new Date();
            
            switch (dateFilter) {
                case 'today':
                    if (detectedDate.toDateString() !== now.toDateString()) return false;
                    break;
                case 'week':
                    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                    if (detectedDate < weekAgo) return false;
                    break;
                case 'month':
                    const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                    if (detectedDate < monthAgo) return false;
                    break;
                case 'year':
                    const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
                    if (detectedDate < yearAgo) return false;
                    break;
            }
        }
        
        // Search filter
        if (searchTerm) {
            const searchFields = [vuln.title, vuln.description, vuln.identifier].join(' ').toLowerCase();
            if (!searchFields.includes(searchTerm)) return false;
        }
        
        return true;
    });
    
    currentPage = 1;
    renderVulnerabilities();
}

function renderVulnerabilities() {
    const tbody = document.getElementById('vulnerabilities-tbody');
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = filteredVulnerabilities.slice(start, end);
    
    tbody.innerHTML = '';
    
    pageData.forEach(vuln => {
        const row = createVulnerabilityRow(vuln);
        tbody.appendChild(row);
    });
    
    updatePagination();
    updateCounts();
}

function createVulnerabilityRow(vulnerability) {
    const tr = document.createElement('tr');
    tr.className = 'vulnerability-row';
    
    const severityClass = `severity-${vulnerability.severity}`;
    const statusClass = `status-${vulnerability.status}`;
    const severityIcon = getSeverityIcon(vulnerability.severity);
    const statusIcon = getStatusIcon(vulnerability.status);
    
    tr.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap">
            <input type="checkbox" class="vulnerability-checkbox rounded border-gray-300 text-green-600 shadow-sm focus:border-green-300 focus:ring-green-500" value="${vulnerability.id}">
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${severityClass}">
                ${severityIcon} ${vulnerability.severity.toUpperCase()}
            </span>
        </td>
        <td class="px-6 py-4">
            <div class="text-sm font-medium text-gray-900 dark:text-white">
                ${vulnerability.title}
            </div>
            <div class="text-sm text-gray-500 dark:text-gray-400">
                ${vulnerability.description}
            </div>
        </td>
        <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
            ${vulnerability.location?.path || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                ${statusIcon} ${vulnerability.status.replace('_', ' ').toUpperCase()}
            </span>
        </td>
        <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
            ${new Date(vulnerability.detected_at).toLocaleDateString()}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <button onclick="viewDetails('${vulnerability.id}')" class="text-green-600 hover:text-green-900 mr-3">
                👁️ View
            </button>
            <button onclick="generateFix('${vulnerability.id}')" class="text-blue-600 hover:text-blue-900 mr-3">
                🤖 AI Fix
            </button>
            <button onclick="updateStatus('${vulnerability.id}')" class="text-gray-600 hover:text-gray-900">
                ⚙️ Status
            </button>
        </td>
    `;
    
    return tr;
}

function getSeverityIcon(severity) {
    const icons = {
        critical: '🚨',
        high: '⚠️',
        medium: '⚡',
        low: 'ℹ️'
    };
    return icons[severity] || '❓';
}

function getStatusIcon(status) {
    const icons = {
        detected: '🔍',
        analyzing: '🔬',
        fixing: '🔧',
        fixed: '✅',
        ignored: '🚫',
        false_positive: '❌'
    };
    return icons[status] || '❓';
}

function updatePagination() {
    const totalPages = Math.ceil(filteredVulnerabilities.length / itemsPerPage);
    const start = (currentPage - 1) * itemsPerPage + 1;
    const end = Math.min(currentPage * itemsPerPage, filteredVulnerabilities.length);
    
    document.getElementById('showing-start').textContent = start;
    document.getElementById('showing-end').textContent = end;
    document.getElementById('total-results').textContent = filteredVulnerabilities.length;
    
    document.getElementById('prev-btn').disabled = currentPage === 1;
    document.getElementById('next-btn').disabled = currentPage === totalPages;
}

function updateCounts() {
    document.getElementById('vulnerability-count').textContent = filteredVulnerabilities.length;
}

function toggleSelectAll() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.vulnerability-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
}

function getSelectedVulnerabilities() {
    const checkboxes = document.querySelectorAll('.vulnerability-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

async function bulkGenerateFixes() {
    const selectedIds = getSelectedVulnerabilities();
    
    if (selectedIds.length === 0) {
        alert('Please select vulnerabilities to generate fixes for');
        return;
    }
    
    for (const id of selectedIds) {
        await generateFix(id);
    }
}

async function bulkUpdateStatus(status) {
    const selectedIds = getSelectedVulnerabilities();
    
    if (selectedIds.length === 0) {
        alert('Please select vulnerabilities to update');
        return;
    }
    
    try {
        for (const id of selectedIds) {
            const response = await fetch(`/api/v1/vulnerabilities/${id}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify({ status })
            });
        }
        
        await loadVulnerabilities();
        
    } catch (error) {
        alert('Failed to update status: ' + error.message);
    }
}

function viewDetails(id) {
    window.location.href = `/vulnerabilities/${id}`;
}

async function generateFix(id) {
    try {
        const response = await fetch(`/api/v1/vulnerabilities/${id}/generate-fix`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('AI fix generation started! Check the fixes tab for results.');
        } else {
            alert('Failed to generate AI fix: ' + result.message);
        }
        
    } catch (error) {
        alert('Error generating AI fix: ' + error.message);
    }
}

function updateStatus(id) {
    const newStatus = prompt('Enter new status (detected, analyzing, fixing, fixed, ignored, false_positive):');
    
    if (newStatus && ['detected', 'analyzing', 'fixing', 'fixed', 'ignored', 'false_positive'].includes(newStatus)) {
        bulkUpdateStatus(newStatus);
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderVulnerabilities();
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredVulnerabilities.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderVulnerabilities();
    }
}

function refreshData() {
    loadVulnerabilities();
}

function exportResults() {
    const csvContent = [
        ['ID', 'Title', 'Severity', 'Status', 'Location', 'Detected At'],
        ...filteredVulnerabilities.map(vuln => [
            vuln.id,
            vuln.title,
            vuln.severity,
            vuln.status,
            vuln.location?.path || '',
            vuln.detected_at
        ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `vulnerabilities_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}
</script>
@endsection
