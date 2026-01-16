<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DevGuardian AI - @yield('title', 'Secure Access')</title>
    <meta name="description" content="DevGuardian AI - Military-grade cybersecurity platform with advanced AI-powered threat detection and vulnerability analysis.">
    <meta name="keywords" content="military cybersecurity, AI security, threat detection, vulnerability analysis">
    <link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
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
            opacity: 0.1;
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
        
        .guest-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            position: relative;
            z-index: 2;
        }
        
        .guest-header {
            position: absolute;
            top: 2rem;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 10;
        }
        
        .guest-logo {
            font-family: 'Russo One', sans-serif;
            font-size: 2rem;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
            margin-bottom: 0.5rem;
        }
        
        .guest-tagline {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .security-badge {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid var(--accent-green);
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-size: 0.75rem;
            color: var(--accent-green);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
            display: inline-block;
        }
        
        @media (max-width: 768px) {
            .guest-container {
                padding: 1rem;
            }
            
            .guest-header {
                top: 1rem;
            }
            
            .guest-logo {
                font-size: 1.5rem;
            }
            
            .guest-tagline {
                font-size: 0.8rem;
            }
        }
    </style>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="guest-header">
        <div class="guest-logo">DevGuardian AI</div>
        <div class="guest-tagline">Military-Grade Security</div>
        <div class="security-badge">🔒 SECURE ZONE</div>
    </div>
    
    <div class="guest-container">
        @yield('content')
    </div>
</body>
</html>
