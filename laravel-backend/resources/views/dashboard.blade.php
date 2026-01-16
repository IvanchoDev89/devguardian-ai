<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - DevGuardian AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { font-family: 'Inter', sans-serif; }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <h1 class="text-2xl font-bold text-gray-900">DevGuardian AI</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <button class="relative p-2 text-gray-600 hover:text-gray-900">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                        </svg>
                        <span class="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
                    </button>
                    <div class="flex items-center">
                        <img class="h-8 w-8 rounded-full mr-3" src="https://ui-avatars.com/api/?name=User&background=6366f1&color=fff" alt="User">
                        <span class="text-gray-700 font-medium">John Doe</span>
                    </div>
                    <a href="{{ route('logout') }}" class="text-gray-600 hover:text-gray-900">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Welcome Section -->
        <div class="mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">Welcome back, John!</h2>
            <p class="text-gray-600">Here's what's happening with your security scans today.</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white card-hover">
                <h3 class="text-lg font-semibold mb-2">Start New Scan</h3>
                <p class="mb-4">Scan your code for vulnerabilities</p>
                <button class="bg-white text-indigo-600 px-4 py-2 rounded-md hover:bg-gray-100 transition-colors">
                    Upload Files
                </button>
            </div>

            <div class="bg-gradient-to-r from-green-500 to-teal-600 rounded-lg p-6 text-white card-hover">
                <h3 class="text-lg font-semibold mb-2">View Reports</h3>
                <p class="mb-4">Check your security analysis results</p>
                <button class="bg-white text-green-600 px-4 py-2 rounded-md hover:bg-gray-100 transition-colors">
                    View All
                </button>
            </div>

            <div class="bg-gradient-to-r from-orange-500 to-red-600 rounded-lg p-6 text-white card-hover">
                <h3 class="text-lg font-semibold mb-2">AI Fixes</h3>
                <p class="mb-4">Apply AI-generated security fixes</p>
                <button class="bg-white text-orange-600 px-4 py-2 rounded-md hover:bg-gray-100 transition-colors">
                    View Fixes
                </button>
            </div>
        </div>

        <!-- Stats Overview -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-lg p-6 shadow-sm">
                <div class="flex items-center">
                    <div class="bg-blue-100 p-3 rounded-full mr-4">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Total Scans</p>
                        <p class="text-2xl font-bold text-gray-900">142</p>
                        <p class="text-sm text-green-600">+12% this month</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg p-6 shadow-sm">
                <div class="flex items-center">
                    <div class="bg-red-100 p-3 rounded-full mr-4">
                        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Vulnerabilities</p>
                        <p class="text-2xl font-bold text-gray-900">23</p>
                        <p class="text-sm text-red-600">5 critical</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg p-6 shadow-sm">
                <div class="flex items-center">
                    <div class="bg-green-100 p-3 rounded-full mr-4">
                        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Fixed Issues</p>
                        <p class="text-2xl font-bold text-gray-900">89</p>
                        <p class="text-sm text-green-600">+23 this week</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg p-6 shadow-sm">
                <div class="flex items-center">
                    <div class="bg-purple-100 p-3 rounded-full mr-4">
                        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">AI Fixes Applied</p>
                        <p class="text-2xl font-bold text-gray-900">45</p>
                        <p class="text-sm text-green-600">+8 this week</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Activity & Chart -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Recent Scans -->
            <div class="bg-white rounded-lg shadow-sm">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Recent Scans</h3>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div class="flex items-center">
                                <div class="bg-blue-100 p-2 rounded-full mr-3">
                                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">user-auth.php</p>
                                    <p class="text-xs text-gray-500">2 hours ago</p>
                                </div>
                            </div>
                            <span class="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800">Critical</span>
                        </div>

                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div class="flex items-center">
                                <div class="bg-blue-100 p-2 rounded-full mr-3">
                                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">dashboard.js</p>
                                    <p class="text-xs text-gray-500">5 hours ago</p>
                                </div>
                            </div>
                            <span class="px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">Medium</span>
                        </div>

                        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div class="flex items-center">
                                <div class="bg-blue-100 p-2 rounded-full mr-3">
                                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">api.py</p>
                                    <p class="text-xs text-gray-500">1 day ago</p>
                                </div>
                            </div>
                            <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">Low</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Security Score Chart -->
            <div class="bg-white rounded-lg shadow-sm">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Security Score Trend</h3>
                </div>
                <div class="p-6">
                    <canvas id="securityChart" width="400" height="200"></canvas>
                </div>
            </div>
        </div>

        <!-- Quick Tips -->
        <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6 border border-indigo-200">
            <div class="flex items-start">
                <div class="bg-indigo-100 p-2 rounded-full mr-4">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Security Tip</h3>
                    <p class="text-gray-600">Regularly updating your dependencies and applying security patches can prevent up to 60% of common vulnerabilities. Consider setting up automated dependency scanning.</p>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Security Score Chart
        const ctx = document.getElementById('securityChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Security Score',
                    data: [65, 72, 78, 85],
                    borderColor: 'rgb(99, 102, 241)',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    </script>
</body>
</html>
        :root {
            --primary-dark: #0a0e27;
            --secondary-dark: #151931;
            --accent-green: #00ff41;
            --accent-red: #ff0040;
            --accent-blue: #00d4ff;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --border-color: #2a3f5f;
            --card-bg: rgba(10, 14, 39, 0.95);
            --sidebar-bg: rgba(10, 14, 39, 0.98);
            --hover-bg: rgba(0, 255, 65, 0.1);
            --success: #00ff41;
            --warning: #f59e0b;
            --danger: #ff0040;
            --critical: #dc2626;
        }
        
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body {
            font-family: 'Roboto Mono', monospace;
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
            min-height: 100vh;
            color: var(--text-primary);
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.05;
            background-image: 
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 35px,
                    rgba(0, 255, 65, 0.1) 35px,
                    rgba(0, 255, 65, 0.1) 70px
                );
            animation: bgMove 20s linear infinite;
        }
        
        @keyframes bgMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(70px, 70px); }
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 255, 65, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 64, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(0, 212, 255, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }
        
        .dashboard-container {
            display: flex;
            min-height: 100vh;
            position: relative;
            z-index: 2;
        }
        
        .sidebar {
            width: 320px;
            background: var(--sidebar-bg);
            border-right: 2px solid var(--border-color);
            color: var(--text-primary);
            padding: 2rem 0;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            z-index: 1000;
            backdrop-filter: blur(20px);
        }
        
        .sidebar::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 2px;
            height: 100%;
            background: linear-gradient(180deg, var(--accent-green), var(--accent-blue), var(--accent-green));
            animation: borderGlow 3s linear infinite;
        }
        
        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        
        .logo {
            font-family: 'Russo One', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 3rem;
            padding: 0 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        
        .logo-shield {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, var(--accent-green), var(--accent-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .nav-menu {
            list-style: none;
        }
        
        .nav-item {
            margin-bottom: 0.5rem;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            padding: 1rem 1.5rem;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
            position: relative;
            font-weight: 500;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.85rem;
        }
        
        .nav-link:hover {
            background: var(--hover-bg);
            color: var(--accent-green);
            border-left-color: var(--accent-green);
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        .nav-link.active {
            background: var(--hover-bg);
            color: var(--accent-green);
            border-left-color: var(--accent-green);
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        .nav-link.active::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--accent-green);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        .nav-icon {
            margin-right: 1rem;
            font-size: 1.2rem;
            width: 24px;
            text-align: center;
        }
        
        .main-content {
            flex: 1;
            margin-left: 320px;
            padding: 2rem;
            position: relative;
        }
        
        .header {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue), var(--accent-green));
            animation: borderGlow 3s linear infinite;
        }
        
        .header-title {
            font-family: 'Russo One', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .user-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-green), var(--accent-blue));
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-dark);
            font-weight: 700;
            font-size: 1.2rem;
            border: 2px solid var(--accent-green);
            font-family: 'Russo One', sans-serif;
            text-transform: uppercase;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
            animation: borderGlow 3s linear infinite;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 255, 65, 0.2);
            border-color: var(--accent-green);
        }
        
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .stat-icon {
            width: 65px;
            height: 65px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            position: relative;
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.1), rgba(0, 212, 255, 0.1));
            border: 2px solid var(--accent-green);
        }
        
        .stat-value {
            font-family: 'Russo One', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            color: var(--accent-green);
            letter-spacing: -1px;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: 'Orbitron', monospace;
        }
        
        .stat-change {
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .positive { 
            background: rgba(0, 255, 65, 0.1); 
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }
        .negative { 
            background: rgba(255, 0, 64, 0.1); 
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
        }
        
        .card {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
            animation: borderGlow 3s linear infinite;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .card-title {
            font-family: 'Russo One', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
            font-family: 'Orbitron', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, var(--accent-green), var(--accent-blue));
            color: var(--primary-dark);
            border: 2px solid var(--accent-green);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 255, 65, 0.4);
        }
        
        .btn-danger {
            background: linear-gradient(45deg, var(--accent-red), var(--critical));
            color: var(--text-primary);
            border: 2px solid var(--accent-red);
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th, .table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .table th {
            font-weight: 700;
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: 'Orbitron', monospace;
        }
        
        .table td {
            color: var(--text-primary);
            font-weight: 500;
            font-family: 'Roboto Mono', monospace;
        }
        
        .badge {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Orbitron', monospace;
        }
        
        .badge-critical { 
            background: rgba(220, 38, 38, 0.1); 
            color: var(--critical);
            border: 1px solid var(--critical);
        }
        .badge-high { 
            background: rgba(255, 0, 64, 0.1); 
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
        }
        .badge-medium { 
            background: rgba(245, 158, 11, 0.1); 
            color: var(--warning);
            border: 1px solid var(--warning);
        }
        .badge-low { 
            background: rgba(0, 212, 255, 0.1); 
            color: var(--accent-blue);
            border: 1px solid var(--accent-blue);
        }
        
        .security-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent-green);
            display: inline-block;
            margin-right: 0.75rem;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        @media (max-width: 1024px) {
            .sidebar { transform: translateX(-100%); }
            .main-content { margin-left: 0; }
            .content-grid { grid-template-columns: 1fr; }
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="dashboard-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <div class="logo-shield">🛡️</div>
                <span>DevGuardian</span>
            </div>
            <nav>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a href="#" class="nav-link active">
                            <span class="nav-icon">📊</span>
                            Security Operations
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">🔍</span>
                            Threat Scanner
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">⚠️</span>
                            Security Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">🤖</span>
                            AI Defense Systems
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">👥</span>
                            Access Control
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">📋</span>
                            Mission Reports
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">
                            <span class="nav-icon">⚙️</span>
                            System Configuration
                        </a>
                    </li>
                </ul>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="header">
                <div>
                    <h1 class="header-title">Security Operations Center</h1>
                    <p class="header-subtitle">
                        <span class="security-indicator"></span>
                        All systems operational • Last threat assessment: 2 minutes ago
                    </p>
                </div>
                <div class="user-info">
                    <div class="user-avatar">{{ substr(auth()->user()->email ?? 'A', 0, 1) }}</div>
                    <form action="{{ route('logout') }}" method="POST" style="display: inline;">
                        @csrf
                        <button type="submit" class="btn btn-danger">🚪 Secure Logout</button>
                    </form>
                </div>
            </header>

            <!-- Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-header">
                        <div>
                            <div class="stat-value">0</div>
                            <div class="stat-label">Critical Threats</div>
                        </div>
                        <div class="stat-icon">🚨</div>
                    </div>
                    <span class="stat-change positive">↑ 0% from last scan</span>
                </div>

                <div class="stat-card">
                    <div class="stat-header">
                        <div>
                            <div class="stat-value">0</div>
                            <div class="stat-label">Security Events</div>
                        </div>
                        <div class="stat-icon">⚡</div>
                    </div>
                    <span class="stat-change positive">↑ 0% from last hour</span>
                </div>

                <div class="stat-card">
                    <div class="stat-header">
                        <div>
                            <div class="stat-value">100%</div>
                            <div class="stat-label">Defense Status</div>
                        </div>
                        <div class="stat-icon">🛡️</div>
                    </div>
                    <span class="stat-change positive">All protections active</span>
                </div>

                <div class="stat-card">
                    <div class="stat-header">
                        <div>
                            <div class="stat-value">ONLINE</div>
                            <div class="stat-label">AI Defense</div>
                        </div>
                        <div class="stat-icon">🤖</div>
                    </div>
                    <span class="stat-change positive">Monitoring active</span>
                </div>
            </div>

            <!-- Content Grid -->
            <div class="content-grid">
                <!-- Recent Vulnerabilities -->
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>🔍</span>
                            Recent Threat Intelligence
                        </h2>
                        <a href="#" class="btn btn-primary">View All →</a>
                    </div>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Threat Level</th>
                                <th>Target System</th>
                                <th>Detected</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span class="badge badge-critical">🚨 Critical</span></td>
                                <td>app.js</td>
                                <td>2 hours ago</td>
                            </tr>
                            <tr>
                                <td><span class="badge badge-high">⚠️ High</span></td>
                                <td>config.yml</td>
                                <td>5 hours ago</td>
                            </tr>
                            <tr>
                                <td><span class="badge badge-medium">⚡ Medium</span></td>
                                <td>database.sql</td>
                                <td>1 day ago</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Security Actions -->
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>🛡️</span>
                            Defense Operations
                        </h2>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <a href="#" class="btn btn-primary">🔍 Execute Deep Scan</a>
                        <a href="#" class="btn btn-primary">🤖 Deploy AI Defense</a>
                        <a href="#" class="btn btn-primary">📊 Generate Threat Report</a>
                        <a href="#" class="btn btn-primary">🔒 Initiate Lockdown</a>
                        <a href="#" class="btn btn-primary">📧 Send Security Alert</a>
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
