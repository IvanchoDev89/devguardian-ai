@extends('layouts.app')

@section('content')
<div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                        🛡️ Vulnerability Scanner
                    </h1>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="startScan()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        🔍 Start Scan
                    </button>
                    <button onclick="showStatistics()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        📊 Statistics
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Scanner Section -->
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg mb-6">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                    Scan Repository or Upload Files
                </h3>
                
                <!-- Tab Navigation -->
                <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
                    <nav class="-mb-px flex space-x-8">
                        <button onclick="switchTab('repository')" id="repository-tab" class="tab-button active">
                            Repository Scan
                        </button>
                        <button onclick="switchTab('files')" id="files-tab" class="tab-button">
                            File Upload
                        </button>
                    </nav>
                </div>

                <!-- Repository Scan Form -->
                <div id="repository-form" class="tab-content">
                    <form onsubmit="scanRepository(event)">
                        <div class="grid grid-cols-1 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Repository URL
                                </label>
                                <div class="mt-1">
                                    <input type="url" id="repo-url" required
                                           class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                                           placeholder="https://github.com/user/repo.git">
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Branch
                                </label>
                                <div class="mt-1">
                                    <input type="text" id="repo-branch" value="main"
                                           class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Scan Type
                                </label>
                                <div class="mt-1">
                                    <select id="scan-type" class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                                        <option value="quick">Quick Scan</option>
                                        <option value="deep">Deep Scan</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="mt-6">
                            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
                                🚀 Start Repository Scan
                            </button>
                        </div>
                    </form>
                </div>

                <!-- File Upload Form -->
                <div id="files-form" class="tab-content hidden">
                    <form onsubmit="scanFiles(event)">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                Upload Code Files
                            </label>
                            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors">
                                <div class="space-y-1 text-center">
                                    <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 00-5.656 0L28 28m0 0l9.172-9.172a4 4 0 00-5.656 0L28 28" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                    </svg>
                                    <div class="flex text-sm text-gray-600">
                                        <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-green-600 hover:text-green-500 focus-within:ring-2 focus-within:ring-green-500">
                                            <span>Upload files</span>
                                            <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple accept=".php,.js,.ts,.vue,.py,.java,.cpp,.c,.h,.go,.rs" onchange="handleFileSelect(event)">
                                        </label>
                                    </div>
                                    <p class="text-xs text-gray-500">
                                        PHP, JavaScript, TypeScript, Vue, Python, Java, C/C++, Go, Rust up to 10MB each
                                    </p>
                                </div>
                                <div id="file-list" class="mt-4 space-y-2"></div>
                            </div>
                        </div>
                        <div class="mt-4">
                            <div class="flex items-center">
                                <input type="checkbox" id="deep-scan" class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded">
                                <label for="deep-scan" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
                                    Enable Deep Scan (Slower but more thorough)
                                </label>
                            </div>
                        </div>
                        <div class="mt-6">
                            <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
                                🔍 Scan Files
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

        <!-- Results Section -->
        <div id="results-section" class="hidden">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                        Scan Results
                    </h3>
                    <div id="scan-results"></div>
                </div>
            </div>
        </div>

        <!-- Statistics Modal -->
        <div id="statistics-modal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full hidden">
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800">
                <div class="mt-3 text-center">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                        📊 Vulnerability Statistics
                    </h3>
                    <div class="mt-2 px-7 py-3">
                        <div id="statistics-content" class="text-sm text-gray-500 dark:text-gray-400">
                            Loading statistics...
                        </div>
                    </div>
                    <div class="items-center px-4 py-3">
                        <button onclick="closeStatistics()" class="px-4 py-2 bg-green-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.tab-button {
    @apply py-2 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 border-b-2 border-transparent hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300;
}

.tab-button.active {
    @apply text-green-600 border-green-500 dark:text-green-500 dark:border-green-400;
}

.tab-content {
    @apply mt-6;
}

.vulnerability-item {
    @apply border-l-4 pl-4 py-3;
}

.vulnerability-critical {
    @apply border-red-500 bg-red-50 dark:bg-red-900/20;
}

.vulnerability-high {
    @apply border-orange-500 bg-orange-50 dark:bg-orange-900/20;
}

.vulnerability-medium {
    @apply border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20;
}

.vulnerability-low {
    @apply border-blue-500 bg-blue-50 dark:bg-blue-900/20;
}
</style>

<script>
let selectedFiles = [];
let currentTab = 'repository';

function switchTab(tab) {
    currentTab = tab;
    
    // Hide all forms
    document.getElementById('repository-form').classList.add('hidden');
    document.getElementById('files-form').classList.add('hidden');
    
    // Remove active class from all tabs
    document.getElementById('repository-tab').classList.remove('active');
    document.getElementById('files-tab').classList.remove('active');
    
    // Show selected form and activate tab
    if (tab === 'repository') {
        document.getElementById('repository-form').classList.remove('hidden');
        document.getElementById('repository-tab').classList.add('active');
    } else {
        document.getElementById('files-form').classList.remove('hidden');
        document.getElementById('files-tab').classList.add('active');
    }
}

function handleFileSelect(event) {
    selectedFiles = Array.from(event.target.files);
    displayFileList();
}

function displayFileList() {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'flex items-center justify-between p-2 bg-gray-50 rounded';
        fileItem.innerHTML = `
            <span class="text-sm text-gray-700">${file.name} (${formatFileSize(file.size)})</span>
            <button type="button" onclick="removeFile(${index})" class="text-red-600 hover:text-red-800 text-sm">
                                Remove
                            </button>
        `;
        fileList.appendChild(fileItem);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFileList();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function scanRepository(event) {
    event.preventDefault();
    
    const repoUrl = document.getElementById('repo-url').value;
    const branch = document.getElementById('repo-branch').value;
    const scanType = document.getElementById('scan-type').value;
    
    showLoading();
    
    try {
        const response = await fetch('/api/v1/vulnerabilities/scan-repository', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({
                repository_url: repoUrl,
                branch: branch,
                scan_type: scanType
            })
        });
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        showError('Repository scan failed: ' + error.message);
    }
}

async function scanFiles(event) {
    event.preventDefault();
    
    const scanType = document.getElementById('deep-scan').checked ? 'deep' : 'quick';
    
    if (selectedFiles.length === 0) {
        showError('Please select files to scan');
        return;
    }
    
    showLoading();
    
    const formData = new FormData();
    formData.append('scan_type', scanType);
    
    selectedFiles.forEach(file => {
        formData.append('files[]', file);
    });
    
    try {
        const response = await fetch('/api/v1/vulnerabilities/scan-files', {
            method: 'POST',
            headers: {
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: formData
        });
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        showError('File scan failed: ' + error.message);
    }
}

function displayResults(results) {
    const resultsSection = document.getElementById('results-section');
    const scanResults = document.getElementById('scan-results');
    
    resultsSection.classList.remove('hidden');
    
    let html = `
        <div class="mb-4">
            <p class="text-sm text-gray-600">
                Scan completed! Found <span class="font-bold text-green-600">${results.vulnerabilities_found || 0}</span> vulnerabilities
                ${results.scan_duration ? ` in ${results.scan_duration}s` : ''}
            </p>
        </div>
    `;
    
    if (results.scan_results && results.scan_results.length > 0) {
        results.scan_results.forEach(result => {
            if (result.vulnerability_analysis && result.vulnerability_analysis.vulnerabilities) {
                result.vulnerability_analysis.vulnerabilities.forEach(vuln => {
                    html += createVulnerabilityCard(vuln);
                });
            }
        });
    }
    
    scanResults.innerHTML = html;
}

function createVulnerabilityCard(vulnerability) {
    const severityClass = `vulnerability-${vulnerability.severity}`;
    const severityIcon = getSeverityIcon(vulnerability.severity);
    
    return `
        <div class="vulnerability-item ${severityClass}">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center">
                        <span class="text-lg">${severityIcon}</span>
                        <h4 class="ml-2 text-lg font-medium text-gray-900 dark:text-white">
                            ${vulnerability.title}
                        </h4>
                    </div>
                    <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                        ${vulnerability.description}
                    </p>
                    ${vulnerability.location ? `
                        <p class="mt-1 text-xs text-gray-500 dark:text-gray-500">
                            📍 ${vulnerability.location.path || vulnerability.location}
                        </p>
                    ` : ''}
                </div>
                <div class="ml-4">
                    <button onclick="generateFix('${vulnerability.id}')" class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">
                        🤖 AI Fix
                    </button>
                </div>
            </div>
        </div>
    `;
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

async function generateFix(vulnerabilityId) {
    try {
        const response = await fetch(`/api/v1/vulnerabilities/${vulnerabilityId}/generate-fix`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess('AI fix generation started! Check the fixes tab for results.');
        } else {
            showError('Failed to generate AI fix: ' + result.message);
        }
        
    } catch (error) {
        showError('Error generating AI fix: ' + error.message);
    }
}

async function showStatistics() {
    document.getElementById('statistics-modal').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/v1/vulnerabilities/statistics');
        const stats = await response.json();
        
        const content = document.getElementById('statistics-content');
        content.innerHTML = `
            <div class="space-y-4">
                <div class="flex justify-between">
                    <span>Total Vulnerabilities:</span>
                    <span class="font-bold">${stats.total_vulnerabilities || 0}</span>
                </div>
                <div class="border-t pt-4">
                    <h4 class="font-medium mb-2">By Severity:</h4>
                    ${Object.entries(stats.by_severity || {}).map(([severity, count]) => 
                        `<div class="flex justify-between">
                            <span class="capitalize">${severity}:</span>
                            <span class="font-bold">${count}</span>
                        </div>`
                    ).join('')}
                </div>
                <div class="border-t pt-4">
                    <h4 class="font-medium mb-2">By Status:</h4>
                    ${Object.entries(stats.by_status || {}).map(([status, count]) => 
                        `<div class="flex justify-between">
                            <span class="capitalize">${status.replace('_', ' ')}:</span>
                            <span class="font-bold">${count}</span>
                        </div>`
                    ).join('')}
                </div>
            </div>
        `;
        
    } catch (error) {
        document.getElementById('statistics-content').innerHTML = 
            '<p class="text-red-600">Failed to load statistics</p>';
    }
}

function closeStatistics() {
    document.getElementById('statistics-modal').classList.add('hidden');
}

function showLoading() {
    const resultsSection = document.getElementById('results-section');
    const scanResults = document.getElementById('scan-results');
    
    resultsSection.classList.remove('hidden');
    scanResults.innerHTML = `
        <div class="text-center py-8">
            <div class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0h12c6.627 0 12 5.373 12v12c0 .627-.5.373-1.2-1.2H5.373C4.746 23.25 4 22.627 4v-12z"></path>
                </svg>
                <span class="text-lg font-medium text-gray-900 dark:text-white">Scanning...</span>
            </div>
        </div>
    `;
}

function showError(message) {
    const resultsSection = document.getElementById('results-section');
    const scanResults = document.getElementById('scan-results');
    
    resultsSection.classList.remove('hidden');
    scanResults.innerHTML = `
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

function showSuccess(message) {
    const resultsSection = document.getElementById('results-section');
    const scanResults = document.getElementById('scan-results');
    
    resultsSection.classList.remove('hidden');
    scanResults.innerHTML = `
        <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            <strong>Success:</strong> ${message}
        </div>
    `;
}
</script>
@endsection
