<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - DevGuardian AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Inter', sans-serif; }
        .input-focus {
            transition: all 0.2s ease;
        }
        .input-focus:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <!-- Logo and Header -->
        <div class="text-center">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">DevGuardian AI</h1>
            <p class="text-gray-600">Create your security account</p>
        </div>

        <!-- Registration Form -->
        <form class="bg-white rounded-lg shadow-lg p-8" method="POST" action="{{ route('register.store') }}">
            @csrf
            <div class="space-y-6">
                <!-- Name Field -->
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                        Full Name
                    </label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        required
                        class="input-focus w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none"
                        placeholder="John Doe"
                    >
                    @error('name')
                        <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                <!-- Email Field -->
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                        Email Address
                    </label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        class="input-focus w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none"
                        placeholder="john@example.com"
                    >
                    @error('email')
                        <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                <!-- Password Field -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                        Password
                    </label>
                    <div class="relative">
                        <input
                            id="password"
                            name="password"
                            type="password"
                            required
                            class="input-focus w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none"
                            placeholder="•••••••••"
                            onkeyup="checkPasswordStrength()"
                        >
                        <button
                            type="button"
                            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            onclick="togglePassword('password')"
                        >
                            <svg id="passwordEyeIcon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </button>
                    </div>
                    <div id="passwordStrength" class="mt-2 hidden">
                        <div class="flex items-center space-x-2">
                            <div class="flex-1 bg-gray-200 rounded-full h-2">
                                <div id="strengthBar" class="h-2 rounded-full transition-all duration-300"></div>
                            </div>
                            <span id="strengthText" class="text-sm"></span>
                        </div>
                    </div>
                    @error('password')
                        <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                <!-- Confirm Password Field -->
                <div>
                    <label for="password_confirmation" class="block text-sm font-medium text-gray-700 mb-2">
                        Confirm Password
                    </label>
                    <div class="relative">
                        <input
                            id="password_confirmation"
                            name="password_confirmation"
                            type="password"
                            required
                            class="input-focus w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none"
                            placeholder="•••••••••"
                        >
                        <button
                            type="button"
                            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            onclick="togglePassword('password_confirmation')"
                        >
                            <svg id="confirmEyeIcon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                            </svg>
                        </button>
                    </div>
                    @error('password_confirmation')
                        <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                <!-- Terms and Conditions -->
                <div class="flex items-center">
                    <input
                        id="terms"
                        name="terms"
                        type="checkbox"
                        required
                        class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                    >
                    <label for="terms" class="ml-2 block text-sm text-gray-700">
                        I agree to the <a href="#" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a> and <a href="#" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
                    </label>
                </div>

                <!-- Submit Button -->
                <button
                    type="submit"
                    class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors font-medium"
                >
                    Create Account
                </button>
            </div>
        </form>

        <!-- Login Link -->
        <div class="text-center">
            <p class="text-gray-600">
                Already have an account?
                <a href="{{ route('login') }}" class="font-medium text-indigo-600 hover:text-indigo-500">
                    Sign in here
                </a>
            </p>
        </div>

        <!-- Features Notice -->
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l2-2z" clip-rule="evenodd"></path>
                    </svg>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-green-800">
                        <strong>Free to Start:</strong> Get instant access to vulnerability scanning and AI-powered security analysis. No credit card required.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function togglePassword(fieldId) {
            const passwordInput = document.getElementById(fieldId);
            const eyeIcon = fieldId === 'password' ? document.getElementById('passwordEyeIcon') : document.getElementById('confirmEyeIcon');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeIcon.innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.842-2.737m3.378 5.727A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.842-2.737M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                `;
            } else {
                passwordInput.type = 'password';
                eyeIcon.innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                `;
            }
        }

        function checkPasswordStrength() {
            const password = document.getElementById('password').value;
            const strengthDiv = document.getElementById('passwordStrength');
            const strengthBar = document.getElementById('strengthBar');
            const strengthText = document.getElementById('strengthText');
            
            if (password.length === 0) {
                strengthDiv.classList.add('hidden');
                return;
            }
            
            strengthDiv.classList.remove('hidden');
            
            let strength = 0;
            let strengthColor = '';
            let strengthMessage = '';
            
            // Check password strength
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;
            
            if (strength <= 2) {
                strengthColor = 'bg-red-500';
                strengthMessage = 'Weak';
            } else if (strength <= 3) {
                strengthColor = 'bg-yellow-500';
                strengthMessage = 'Fair';
            } else if (strength <= 4) {
                strengthColor = 'bg-blue-500';
                strengthMessage = 'Good';
            } else {
                strengthColor = 'bg-green-500';
                strengthMessage = 'Strong';
            }
            
            strengthBar.className = `h-2 rounded-full transition-all duration-300 ${strengthColor}`;
            strengthBar.style.width = `${(strength / 5) * 100}%`;
            strengthText.className = `text-sm ${strengthColor.replace('bg-', 'text-')}`;
            strengthText.textContent = strengthMessage;
        }

        // Auto-focus on name field
        document.getElementById('name').focus();
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
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
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
        
        .auth-container {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 0 100px rgba(0, 255, 65, 0.1);
            width: 100%;
            max-width: 500px;
            padding: 3rem;
            position: relative;
            overflow: hidden;
        }
        
        .auth-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue), var(--accent-green));
            animation: borderGlow 3s linear infinite;
        }
        
        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        
        .logo-section {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .logo {
            font-family: 'Russo One', sans-serif;
            font-size: 2.5rem;
            color: var(--accent-green);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        
        .tagline {
            color: var(--text-secondary);
            font-size: 1rem;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 2rem;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--accent-green);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        input {
            width: 100%;
            padding: 1rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            font-family: 'Roboto Mono', monospace;
            transition: all 0.3s ease;
            background: rgba(21, 25, 49, 0.8);
            color: var(--text-primary);
        }
        
        input:focus {
            outline: none;
            border-color: var(--accent-green);
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
            background: rgba(21, 25, 49, 1);
        }
        
        input::placeholder {
            color: var(--text-secondary);
            opacity: 0.7;
        }
        
        .btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(45deg, var(--accent-green), var(--accent-blue));
            color: var(--primary-dark);
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
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
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 255, 65, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .alert {
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 8px;
            background: rgba(255, 0, 64, 0.1);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            font-size: 0.875rem;
            animation: alertPulse 2s ease-in-out infinite;
        }
        
        @keyframes alertPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .login-link {
            text-align: center;
            margin-top: 2rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        .login-link a {
            color: var(--accent-green);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        
        .login-link a:hover {
            color: var(--accent-blue);
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        
        .password-strength {
            margin-top: 0.5rem;
            height: 4px;
            background: var(--border-color);
            border-radius: 2px;
            overflow: hidden;
        }
        
        .password-strength-bar {
            height: 100%;
            transition: all 0.3s ease;
            border-radius: 2px;
        }
        
        .strength-weak { background: var(--accent-red); width: 33%; }
        .strength-medium { background: #f59e0b; width: 66%; }
        .strength-strong { background: var(--accent-green); width: 100%; }
        
        .security-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid var(--accent-green);
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-size: 0.75rem;
            color: var(--accent-green);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .requirements {
            margin-top: 0.5rem;
            font-size: 0.75rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }
        
        .requirements ul {
            margin-left: 1rem;
            margin-top: 0.25rem;
        }
        
        @media (max-width: 640px) {
            .auth-container {
                padding: 2rem 1.5rem;
                margin: 1rem;
            }
            
            .logo {
                font-size: 2rem;
            }
            
            .security-badge {
                position: relative;
                top: auto;
                right: auto;
                margin-bottom: 1rem;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="auth-container">
        <div class="security-badge">🔐 ENLISTMENT</div>
        
        <div class="logo-section">
            <div class="logo">DevGuardian AI</div>
            <div class="tagline">Join the Security Elite</div>
        </div>
        
        <h1 class="form-title">Operative Registration</h1>
        
        @if($errors->any())
            <div class="alert">
                @foreach($errors->all() as $error)
                    🚨 {{ $error }}
                @endforeach
            </div>
        @endif
        
        <form method="POST" action="{{ route('register.store') }}" id="registerForm">
            @csrf
            <div class="form-group">
                <label for="name">Operative Name</label>
                <input type="text" id="name" name="name" value="{{ old('name') }}" required autocomplete="name" placeholder="John Doe">
            </div>
            
            <div class="form-group">
                <label for="email">Access Code</label>
                <input type="email" id="email" name="email" value="{{ old('email') }}" required autocomplete="email" placeholder="operative@devguardian.ai">
            </div>
            
            <div class="form-group">
                <label for="password">Security Key</label>
                <input type="password" id="password" name="password" required autocomplete="new-password" placeholder="••••••••">
                <div class="password-strength">
                    <div class="password-strength-bar" id="passwordStrength"></div>
                </div>
                <div class="requirements">
                    Must contain:
                    <ul>
                        <li>8+ characters</li>
                        <li>Upper & lowercase letters</li>
                        <li>Numbers</li>
                        <li>Special characters</li>
                    </ul>
                </div>
            </div>
            
            <div class="form-group">
                <label for="password_confirmation">Confirm Security Key</label>
                <input type="password" id="password_confirmation" name="password_confirmation" required autocomplete="new-password" placeholder="••••••••">
            </div>
            
            <button type="submit" class="btn" id="submitBtn">
                <span class="loading" id="loading"></span>
                <span id="btnText">Enlist Now</span>
            </button>
        </form>
        
        <div class="login-link">
            Already registered? <a href="{{ route('login') }}">Access System</a>
        </div>
    </div>
    
    <script>
        document.getElementById('password').addEventListener('input', function(e) {
            const password = e.target.value;
            const strengthBar = document.getElementById('passwordStrength');
            
            let strength = 0;
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;
            
            strengthBar.className = 'password-strength-bar';
            if (password.length > 0) {
                if (strength <= 1) strengthBar.classList.add('strength-weak');
                else if (strength === 2) strengthBar.classList.add('strength-medium');
                else strengthBar.classList.add('strength-strong');
            }
        });
        
        // Form submission with loading state
        const registerForm = document.getElementById('registerForm');
        const submitBtn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const btnText = document.getElementById('btnText');
        
        registerForm.addEventListener('submit', function(e) {
            loading.style.display = 'inline-block';
            btnText.textContent = 'Processing...';
            submitBtn.disabled = true;
        });
        
        // Auto-focus on name field
        document.getElementById('name').focus();
        
        // Add input animations
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
        
        // Add typing sound effect simulation (visual feedback)
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                this.style.borderColor = 'var(--accent-blue)';
                setTimeout(() => {
                    this.style.borderColor = 'var(--border-color)';
                }, 200);
            });
        });
    </script>
</body>
</html>
