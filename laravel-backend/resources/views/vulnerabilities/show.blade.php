@extends('layouts.app')

@section('content')
<div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                        🤖 AI Fix Details
                    </h1>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="{{ route('vulnerabilities.index') }}" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        ← Back to Vulnerabilities
                    </a>
                    <button onclick="applyFix()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                        ✅ Apply Fix
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Vulnerability Info -->
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg mb-6">
            <div class="px-4 py-5 sm:p-6">
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        <div class="w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                            <span class="text-2xl">🚨</span>
                        </div>
                    </div>
                    <div class="ml-4 flex-1">
                        <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                            {{ $vulnerability->title }}
                        </h2>
                        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                            {{ $vulnerability->description }}
                        </p>
                        <div class="mt-2 flex items-center space-x-4">
                            <span class="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                                🚨 {{ strtoupper($vulnerability->severity) }}
                            </span>
                            <span class="text-sm text-gray-500 dark:text-gray-400">
                                Detected: {{ $vulnerability->detected_at->format('M j, Y g:i A') }}
                            </span>
                            @if($vulnerability->cvss_score)
                                <span class="text-sm text-gray-500 dark:text-gray-400">
                                    CVSS Score: {{ $vulnerability->cvss_score }}
                                </span>
                            @endif
                        </div>
                        @if($vulnerability->location)
                            <div class="mt-2">
                                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Location:</span>
                                <code class="ml-2 px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-sm">
                                    {{ $vulnerability->location['path'] ?? $vulnerability->location }}
                                </code>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </div>

        <!-- AI Fix -->
        @if($fix)
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                        🤖 Generated AI Fix
                    </h3>
                    
                    <!-- Fix Confidence -->
                    <div class="mb-4">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Confidence Score</span>
                            <div class="flex items-center">
                                <div class="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2 mr-2">
                                    <div class="bg-green-600 h-2 rounded-full" style="width: {{ $fix->confidence }}%"></div>
                                </div>
                                <span class="text-sm text-gray-600 dark:text-gray-400">{{ $fix->confidence }}%</span>
                            </div>
                        </div>
                    </div>

                    <!-- Fix Explanation -->
                    <div class="mb-6">
                        <h4 class="text-md font-medium text-gray-900 dark:text-white mb-2">Explanation</h4>
                        <div class="bg-blue-50 dark:bg-blue-900/20 border border border-blue-200 dark:border-blue-800 rounded-md p-4">
                            <p class="text-sm text-blue-800 dark:text-blue-300">{{ $fix->explanation }}</p>
                        </div>
                    </div>

                    <!-- Recommendations -->
                    @if($fix->recommendations)
                        <div class="mb-6">
                            <h4 class="text-md font-medium text-gray-900 dark:text-white mb-2">Recommendations</h4>
                            <ul class="list-disc list-inside space-y-2">
                                @foreach($fix->recommendations as $recommendation)
                                    <li class="text-sm text-gray-700 dark:text-gray-300">{{ $recommendation }}</li>
                                @endforeach
                            </ul>
                        </div>
                    @endif

                    <!-- Code Comparison -->
                    <div class="mb-6">
                        <h4 class="text-md font-medium text-gray-900 dark:text-white mb-4">Code Changes</h4>
                        
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <!-- Original Code -->
                            <div>
                                <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">🔴 Original Code</h5>
                                <div class="bg-red-50 dark:bg-red-900/20 border border border-red-200 dark:border-red-800 rounded-md">
                                    <pre class="p-4 text-sm text-red-800 dark:text-red-300 overflow-x-auto"><code>{{ $vulnerability->original_code ?? 'N/A' }}</code></pre>
                                </div>
                            </div>
                            
                            <!-- Fixed Code -->
                            <div>
                                <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">🟢 Fixed Code</h5>
                                <div class="bg-green-50 dark:bg-green-900/20 border border border-green-200 dark:border-green-800 rounded-md">
                                    <pre class="p-4 text-sm text-green-800 dark:text-green-300 overflow-x-auto"><code>{{ $fix->fixed_code }}</code></pre>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex space-x-4">
                        <button onclick="copyFixedCode()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-medium">
                            📋 Copy Fixed Code
                        </button>
                        <button onclick="downloadFix()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium">
                            💾 Download Fix
                        </button>
                        <button onclick="createPullRequest()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm font-medium">
                            🔃 Create Pull Request
                        </button>
                    </div>
                </div>
            </div>
        @else
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <div class="text-center">
                        <div class="text-gray-400 mb-4">
                            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24">
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 000-2H9z"></path>
                                <path d="M4 4h16v12a1 1 0 001 1h4a1 1 0 001-1V4z"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-2">
                            No AI Fix Available
                        </h3>
                        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                            Generate an AI fix for this vulnerability using the button below.
                        </p>
                        <button onclick="generateNewFix()" class="mt-4 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg text-sm font-medium">
                            🤖 Generate AI Fix
                        </button>
                    </div>
                </div>
            </div>
        @endif

        <!-- Fix History -->
        @if($fixes && count($fixes) > 0)
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                        📜 Fix History
                    </h3>
                    
                    <div class="space-y-4">
                        @foreach($fixes as $historyFix)
                            <div class="border-l-4 border-gray-200 dark:border-gray-700 pl-4 py-3">
                                <div class="flex items-center justify-between">
                                    <div>
                                        <div class="text-sm font-medium text-gray-900 dark:text-white">
                                            Fix #{{ $loop->index + 1 }}
                                        </div>
                                        <div class="text-sm text-gray-600 dark:text-gray-400">
                                            {{ $historyFix->created_at->format('M j, Y g:i A') }}
                                        </div>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <span class="px-2 py-1 text-xs font-semibold rounded-full {{ $historyFix->status === 'applied' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' : 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300' }}">
                                            {{ $historyFix->status }}
                                        </span>
                                        <span class="text-sm text-gray-600 dark:text-gray-400">
                                            {{ $historyFix->confidence }}% confidence
                                        </span>
                                    </div>
                                </div>
                            </div>
                        @endforeach
                    </div>
                </div>
            </div>
        @endif
    </div>
</div>

<script>
// Copy fixed code to clipboard
function copyFixedCode() {
    const fixedCode = document.querySelector('.bg-green-50 code').textContent;
    navigator.clipboard.writeText(fixedCode).then(() => {
        alert('Fixed code copied to clipboard!');
    });
}

// Download fix as file
function downloadFix() {
    const fixedCode = document.querySelector('.bg-green-50 code').textContent;
    const blob = new Blob([fixedCode], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fix_{{ $vulnerability->id }}.patch`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Create pull request (mock implementation)
function createPullRequest() {
    alert('Pull request creation would be implemented with GitHub/GitLab API integration');
}

// Generate new AI fix
function generateNewFix() {
    window.location.href = `/vulnerabilities/{{ $vulnerability->id }}/generate-fix`;
}

// Apply fix
function applyFix() {
    if (confirm('Are you sure you want to apply this fix? This will modify your codebase.')) {
        fetch(`/vulnerabilities/{{ $vulnerability->id }}/apply-fix`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({
                fix_id: '{{ $fix->id ?? '' }}',
                create_pull_request: false
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Fix applied successfully!');
                window.location.reload();
            } else {
                alert('Failed to apply fix: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            alert('Error applying fix: ' + error.message);
        });
    }
}
</script>
@endsection
