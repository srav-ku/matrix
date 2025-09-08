#!/usr/bin/env python3
"""
Simple server to serve The Matrix frontend
"""

from flask import Flask, render_template_string, jsonify, request, redirect
from flask_cors import CORS
import sys
import os
sys.path.append('./src')
from src.database import execute_query

app = Flask(__name__)
CORS(app, origins="*")

# Landing Page HTML matching first uploaded image
LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Matrix</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', system-ui, sans-serif; }
    </style>
</head>
<body class="bg-black text-white">
    <!-- Header -->
    <header class="flex justify-between items-center p-6 border-b border-gray-800">
        <div class="text-2xl font-bold text-green-400">The Matrix</div>
        <nav class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-300 hover:text-white transition-colors">Use cases</a>
            <a href="#" class="text-gray-300 hover:text-white transition-colors">Product</a>
            <a href="#" class="text-gray-300 hover:text-white transition-colors">Docs</a>
            <a href="#" class="text-gray-300 hover:text-white transition-colors">Pricing</a>
            <a href="#" class="text-gray-300 hover:text-white transition-colors">Resources</a>
            <div class="flex items-center space-x-4">
                <button class="px-4 py-2 border border-gray-600 rounded-lg hover:border-gray-500 transition-colors">
                    Book a demo
                </button>
                <a href="/auth" class="px-4 py-2 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium transition-colors">
                    Log in
                </a>
            </div>
        </nav>
    </header>

    <!-- Hero Section -->
    <main class="flex flex-col items-center justify-center px-4 py-20">
        <div class="max-w-6xl mx-auto text-center">
            <h1 class="text-6xl md:text-7xl font-bold mb-6 leading-tight">
                Build seamless <span class="text-green-400">auth</span> experiences
            </h1>
            
            <p class="text-xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
                Use our API to build to improve your customer experience with 
                effortless One Time Passcodes by allowing your users to access 
                your websites or build loyalty in an instant.
            </p>

            <a href="/auth" class="inline-flex items-center px-8 py-4 bg-green-500 text-black rounded-lg hover:bg-green-400 font-semibold text-lg mb-20 transition-colors">
                Get Started
                <svg class="ml-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </a>

            <!-- Demo Cards -->
            <div class="flex flex-col lg:flex-row gap-8 mt-20">
                <!-- Messages Card -->
                <div class="flex-1 bg-gray-900/80 backdrop-blur-sm border border-gray-700 rounded-2xl p-8">
                    <div class="flex items-center justify-between mb-6">
                        <div class="flex items-center space-x-2 text-sm text-gray-400">
                            <div class="w-2 h-2 bg-gray-400 rounded-full"></div>
                            <span>Messages</span>
                        </div>
                        <span class="text-xs text-gray-500">09:35:14</span>
                    </div>
                    
                    <div class="text-left mb-8">
                        <p class="text-gray-300 mb-2">Your Passcode is</p>
                        <p class="text-4xl font-bold text-white">4695</p>
                    </div>

                    <div class="flex items-center justify-center w-12 h-12 bg-green-500/20 rounded-lg mb-4 mx-auto">
                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                    </div>
                    <p class="text-sm text-gray-400 text-center">Enter Passcode</p>
                </div>

                <!-- SMS OTP Card -->
                <div class="flex-1 bg-gray-900/80 backdrop-blur-sm border border-gray-700 rounded-2xl p-8 relative">
                    <div class="flex justify-center mb-4">
                        <div class="flex space-x-1">
                            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                            <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        </div>
                    </div>
                    
                    <div class="flex items-center justify-center w-16 h-16 bg-green-500/20 rounded-2xl mx-auto mb-6">
                        <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    
                    <h3 class="text-2xl font-semibold mb-6 text-center text-white">SMS OTP</h3>
                    <span class="text-xs text-gray-500 absolute top-4 right-4">09:35:14</span>
                    
                    <div class="grid grid-cols-6 gap-2 mb-6">
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                        <div class="aspect-square border border-gray-600 rounded-lg hover:border-green-500 transition-colors"></div>
                    </div>
                    
                    <button class="w-full py-3 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium transition-colors">
                        Verify OTP
                    </button>
                </div>
            </div>
        </div>

        <!-- Features Section -->
        <div class="max-w-7xl mx-auto mt-32 px-4">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold mb-4 text-white">Sed ut perspiciatis unde omnis</h2>
                <h3 class="text-4xl md:text-5xl font-bold text-gray-400">iste natus error sit</h3>
            </div>

            <div class="grid md:grid-cols-2 gap-12">
                <!-- Authentication Feature -->
                <div class="bg-gray-900/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8">
                    <h3 class="text-2xl font-semibold mb-4 text-white">Authentication in just seconds</h3>
                    <p class="text-gray-300 mb-6 leading-relaxed">
                        Create seamless Web and Mobile experiences for your users. Don't worry, they 
                        won't even have to enter the code, it populates itself, like magic.
                    </p>
                    
                    <div class="space-y-2">
                        <div class="flex space-x-1 mb-2">
                            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                            <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        </div>
                        <div class="bg-black border border-gray-800 rounded-lg p-4 font-mono text-sm overflow-x-auto">
                            <div class="text-blue-400">curl --request POST \\\\</div>
                            <div class="text-blue-400 ml-4">--url https://api.matrix.to/movies \\\\</div>
                            <div class="text-blue-400 ml-4">--header 'Content-Type: application/json' \\\\</div>
                            <div class="text-blue-400 ml-4">--data '{</div>
                            <div class="text-yellow-300 ml-8">"query": "action movies",</div>
                            <div class="text-yellow-300 ml-8">"year": "2024",</div>
                            <div class="text-yellow-300 ml-8">"limit": "10"</div>
                            <div class="text-blue-400 ml-4">}'</div>
                        </div>
                    </div>
                </div>

                <!-- Features Grid -->
                <div class="space-y-8">
                    <div class="bg-gray-900/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8">
                        <h3 class="text-2xl font-semibold mb-4 text-white">Add custom claims to control</h3>
                        <p class="text-gray-300 mb-6 leading-relaxed">
                            Use our APIs to create the experience you want for your users. Our movie database is available here.
                        </p>
                        
                        <div class="bg-black border border-gray-800 rounded-lg p-4 font-mono text-sm">
                            <div class="text-blue-400">"role: admin"</div>
                            <div class="text-gray-400 mt-2">"access: read-only"</div>
                            <div class="text-orange-400 mt-4">"level: premium"</div>
                        </div>
                    </div>

                    <div class="bg-gray-900/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8">
                        <h3 class="text-2xl font-semibold mb-4 text-white">Customize Search Options</h3>
                        <p class="text-gray-300 mb-6 leading-relaxed">
                            Use our APIs to create the experience you want for your users. Multiple search options are available.
                        </p>
                        
                        <div class="flex justify-center items-center space-x-4">
                            <div class="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center text-gray-400 hover:border-green-500 transition-colors cursor-pointer">G</div>
                            <div class="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center text-gray-400 hover:border-green-500 transition-colors cursor-pointer">Y</div>
                            <div class="w-12 h-12 border border-green-500 rounded-lg flex items-center justify-center bg-green-500/10 text-green-400">R</div>
                            <div class="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center text-gray-400 hover:border-green-500 transition-colors cursor-pointer">D</div>
                            <div class="w-10 h-10 border border-gray-600 rounded flex items-center justify-center text-gray-400 hover:border-green-500 transition-colors cursor-pointer text-sm">📽</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
"""

# Authentication HTML
AUTH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Matrix - Authentication</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', system-ui, sans-serif; }
    </style>
</head>
<body class="min-h-screen bg-black text-white flex items-center justify-center relative">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-gradient-to-br from-gray-900/20 via-black to-gray-900/20"></div>
    
    <!-- Notification -->
    <div id="notification" class="fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg backdrop-blur-sm border transition-all duration-300 transform translate-x-full hidden">
        <div class="flex items-center space-x-2">
            <span id="notification-icon"></span>
            <span id="notification-message" class="font-medium"></span>
        </div>
    </div>

    <div class="w-full max-w-md px-6 relative z-10">
        <!-- Header -->
        <div class="text-center mb-8">
            <a href="/" class="inline-block">
                <div class="text-3xl font-bold text-green-400 mb-4">The Matrix</div>
            </a>
            <h1 class="text-2xl font-semibold mb-2" id="auth-title">Welcome back</h1>
            <p class="text-gray-400" id="auth-subtitle">Sign in to access your dashboard</p>
        </div>

        <!-- Auth Form -->
        <div class="bg-gray-900/80 backdrop-blur-sm border border-gray-700 rounded-2xl p-8">
            <form id="authForm" class="space-y-6">
                <!-- Name Field (Sign Up Only) -->
                <div id="nameField" class="hidden">
                    <label for="name" class="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                        </svg>
                        <input type="text" id="name" name="name" class="w-full pl-10 pr-4 py-3 bg-black border border-gray-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white placeholder-gray-500 transition-colors" placeholder="Enter your full name">
                    </div>
                </div>

                <!-- Email Field -->
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                        </svg>
                        <input type="email" id="email" name="email" required class="w-full pl-10 pr-4 py-3 bg-black border border-gray-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white placeholder-gray-500 transition-colors" placeholder="Enter your email address">
                    </div>
                </div>

                <!-- Password Field -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-300 mb-2">Password</label>
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                        </svg>
                        <input type="password" id="password" name="password" required class="w-full pl-10 pr-12 py-3 bg-black border border-gray-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white placeholder-gray-500 transition-colors" placeholder="Enter your password">
                        <button type="button" id="togglePassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300 transition-colors">
                            <svg id="eyeIcon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Confirm Password Field (Sign Up Only) -->
                <div id="confirmPasswordField" class="hidden">
                    <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">Confirm Password</label>
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                        </svg>
                        <input type="password" id="confirmPassword" name="confirmPassword" class="w-full pl-10 pr-4 py-3 bg-black border border-gray-600 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white placeholder-gray-500 transition-colors" placeholder="Confirm your password">
                    </div>
                </div>

                <!-- Remember Me / Forgot Password -->
                <div id="loginOptions" class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input type="checkbox" id="remember" class="w-4 h-4 text-green-500 bg-black border-gray-600 rounded focus:ring-green-500 focus:ring-2">
                        <label for="remember" class="ml-2 text-sm text-gray-300">Remember me</label>
                    </div>
                    <button type="button" class="text-sm text-green-400 hover:text-green-300 transition-colors">Forgot password?</button>
                </div>

                <!-- Submit Button -->
                <button type="submit" id="submitBtn" class="w-full py-3 px-4 bg-green-500 text-black font-semibold rounded-lg hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-black transition-colors flex items-center justify-center space-x-2">
                    <span id="submitText">Sign In</span>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                </button>

                <!-- Toggle Auth Mode -->
                <div class="text-center">
                    <p class="text-sm text-gray-400">
                        <span id="toggleQuestion">Don't have an account? </span>
                        <button type="button" id="toggleMode" class="text-green-400 hover:text-green-300 font-medium transition-colors">Sign up</button>
                    </p>
                </div>
            </form>

            <!-- Divider -->
            <div class="mt-8 mb-6">
                <div class="relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-700"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-2 bg-gray-900 text-gray-400">Or continue with</span>
                    </div>
                </div>
            </div>

            <!-- Social Login -->
            <button type="button" id="googleAuth" class="w-full py-3 px-4 bg-gray-800 text-white font-medium rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-offset-2 focus:ring-offset-black transition-colors flex items-center justify-center space-x-2">
                <svg class="w-5 h-5" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span>Continue with Google</span>
            </button>
        </div>

        <!-- Footer -->
        <div class="text-center mt-8">
            <p class="text-xs text-gray-500">
                By <span id="actionText">signing in</span>, you agree to our 
                <a href="#" class="text-green-400 hover:text-green-300 transition-colors">Terms of Service</a> 
                and 
                <a href="#" class="text-green-400 hover:text-green-300 transition-colors">Privacy Policy</a>
            </p>
        </div>
    </div>

    <script>
        let isLogin = true;
        let isLoading = false;

        function showNotification(type, message) {
            const notification = document.getElementById('notification');
            const icon = document.getElementById('notification-icon');
            const messageEl = document.getElementById('notification-message');
            
            // Set icon based on type
            if (type === 'success') {
                notification.className = 'fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg backdrop-blur-sm border transition-all duration-300 bg-green-900/80 border-green-500 text-green-100';
                icon.innerHTML = '✓';
            } else if (type === 'error') {
                notification.className = 'fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg backdrop-blur-sm border transition-all duration-300 bg-red-900/80 border-red-500 text-red-100';
                icon.innerHTML = '!';
            } else {
                notification.className = 'fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg backdrop-blur-sm border transition-all duration-300 bg-blue-900/80 border-blue-500 text-blue-100';
                icon.innerHTML = 'ℹ';
            }
            
            messageEl.textContent = message;
            notification.classList.remove('translate-x-full');
            
            setTimeout(() => {
                notification.classList.add('translate-x-full');
            }, 5000);
        }

        function toggleAuthMode() {
            isLogin = !isLogin;
            
            const nameField = document.getElementById('nameField');
            const confirmPasswordField = document.getElementById('confirmPasswordField');
            const loginOptions = document.getElementById('loginOptions');
            const authTitle = document.getElementById('auth-title');
            const authSubtitle = document.getElementById('auth-subtitle');
            const submitText = document.getElementById('submitText');
            const toggleQuestion = document.getElementById('toggleQuestion');
            const toggleMode = document.getElementById('toggleMode');
            const actionText = document.getElementById('actionText');
            
            if (isLogin) {
                nameField.classList.add('hidden');
                confirmPasswordField.classList.add('hidden');
                loginOptions.classList.remove('hidden');
                authTitle.textContent = 'Welcome back';
                authSubtitle.textContent = 'Sign in to access your dashboard';
                submitText.textContent = 'Sign In';
                toggleQuestion.textContent = "Don't have an account? ";
                toggleMode.textContent = 'Sign up';
                actionText.textContent = 'signing in';
            } else {
                nameField.classList.remove('hidden');
                confirmPasswordField.classList.remove('hidden');
                loginOptions.classList.add('hidden');
                authTitle.textContent = 'Create your account';
                authSubtitle.textContent = 'Join The Matrix and start your journey';
                submitText.textContent = 'Create Account';
                toggleQuestion.textContent = 'Already have an account? ';
                toggleMode.textContent = 'Sign in';
                actionText.textContent = 'creating an account';
            }
            
            // Clear form
            document.getElementById('authForm').reset();
        }

        function handleSubmit(e) {
            e.preventDefault();
            if (isLoading) return;
            
            const formData = new FormData(e.target);
            const email = formData.get('email');
            const password = formData.get('password');
            const name = formData.get('name');
            const confirmPassword = formData.get('confirmPassword');
            
            // Validation
            if (!email || !password) {
                showNotification('error', 'Please fill in all required fields');
                return;
            }
            
            if (!isLogin && password !== confirmPassword) {
                showNotification('error', 'Passwords do not match');
                return;
            }
            
            if (!isLogin && password.length < 8) {
                showNotification('error', 'Password must be at least 8 characters long');
                return;
            }
            
            isLoading = true;
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitText').textContent = 'Processing...';
            
            // Simulate API call
            setTimeout(() => {
                if (isLogin) {
                    if (email && password) {
                        showNotification('success', 'Login successful! Redirecting to dashboard...');
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 2000);
                    } else {
                        showNotification('error', 'Invalid credentials');
                    }
                } else {
                    showNotification('success', 'Account created successfully! Please check your email for verification.');
                    setTimeout(() => {
                        toggleAuthMode();
                    }, 2000);
                }
                
                isLoading = false;
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('submitText').textContent = isLogin ? 'Sign In' : 'Create Account';
            }, 2000);
        }

        function handleGoogleAuth() {
            showNotification('info', 'Google authentication coming soon!');
        }

        function togglePassword() {
            const passwordField = document.getElementById('password');
            const eyeIcon = document.getElementById('eyeIcon');
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                eyeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>';
            } else {
                passwordField.type = 'password';
                eyeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>';
            }
        }

        // Event listeners
        document.getElementById('authForm').addEventListener('submit', handleSubmit);
        document.getElementById('toggleMode').addEventListener('click', toggleAuthMode);
        document.getElementById('googleAuth').addEventListener('click', handleGoogleAuth);
        document.getElementById('togglePassword').addEventListener('click', togglePassword);
    </script>
</body>
</html>
"""

# Dashboard HTML matching second uploaded image
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Matrix - Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', system-ui, sans-serif; }
    </style>
</head>
<body class="bg-black text-white flex h-screen">
    <!-- Sidebar -->
    <aside class="w-64 bg-black border-r border-gray-800 flex flex-col">
        <!-- Logo -->
        <div class="p-6 border-b border-gray-800">
            <div class="text-2xl font-bold text-green-400">The Matrix</div>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 p-4 space-y-1">
            <div class="flex items-center space-x-3 bg-green-500 text-black px-3 py-2 rounded-lg mb-4">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
                </svg>
                <span class="font-medium">Home</span>
            </div>

            <div class="space-y-1">
                <div class="text-xs text-gray-400 px-3 py-2 uppercase tracking-wide">Customization</div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                    <span>Email</span>
                </div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                    </svg>
                    <span>SMS</span>
                </div>
            </div>

            <div class="space-y-1 pt-4">
                <div class="text-xs text-gray-400 px-3 py-2 uppercase tracking-wide">Configuration</div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                    </svg>
                    <span>API Keys</span>
                </div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    <span>Auth Token</span>
                </div>
            </div>

            <div class="space-y-1 pt-4">
                <div class="text-xs text-gray-400 px-3 py-2 uppercase tracking-wide">Application</div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                    </svg>
                    <span>Plan & Billing</span>
                </div>
                
                <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                    <span>Contact Us</span>
                </div>
            </div>
        </nav>

        <!-- Bottom Community Section -->
        <div class="p-4 border-t border-gray-800">
            <div class="flex items-center space-x-3 text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-900 cursor-pointer transition-colors">
                <div class="w-6 h-6 bg-purple-500 rounded flex items-center justify-center">
                    <span class="text-xs text-white font-bold">JS</span>
                </div>
                <div class="flex-1">
                    <div class="text-sm font-medium">Join our slack</div>
                    <div class="text-xs text-gray-400">community</div>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col">
        <!-- Top Header -->
        <header class="h-16 border-b border-gray-800 flex items-center justify-between px-6">
            <div class="flex items-center space-x-4">
                <span class="text-gray-400 cursor-pointer hover:text-white transition-colors">Docs</span>
                <span class="text-gray-400 cursor-pointer hover:text-white transition-colors">matrix.io</span>
            </div>
            
            <div class="flex items-center space-x-4">
                <div class="flex items-center space-x-2 cursor-pointer" onclick="logout()">
                    <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                        <span class="text-sm font-semibold text-black">M</span>
                    </div>
                    <div class="text-right">
                        <div class="text-sm font-medium">Mike Males</div>
                        <div class="text-xs text-gray-400 hover:text-white transition-colors">Logout</div>
                    </div>
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </div>
            </div>
        </header>

        <!-- Main Dashboard Content -->
        <main class="flex-1 p-8 bg-black">
            <!-- Welcome Section -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-white mb-2">Welcome</h1>
                <p class="text-gray-400">Sed ut perspiciatis unde omnis iste natus error sit voluptatem</p>
            </div>

            <!-- Active Users Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-xl font-semibold text-white">Active Users</h2>
                    <div class="flex space-x-6 text-sm">
                        <span class="text-white font-medium cursor-pointer">Active Users</span>
                        <span class="text-gray-400 cursor-pointer hover:text-white transition-colors">Magic Links</span>
                        <span class="text-gray-400 cursor-pointer hover:text-white transition-colors">SMS OTP</span>
                    </div>
                </div>
                
                <!-- Chart Area -->
                <div class="bg-black rounded-lg p-6 h-80 relative">
                    <svg class="w-full h-full" viewBox="0 0 900 320">
                        <defs>
                            <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stop-color="#10b981" stop-opacity="0.3" />
                                <stop offset="100%" stop-color="#10b981" stop-opacity="0.05" />
                            </linearGradient>
                        </defs>
                        
                        <!-- Grid lines -->
                        <g stroke="#374151" stroke-width="0.5">
                            <line x1="50" y1="40" x2="850" y2="40"/>
                            <line x1="50" y1="70" x2="850" y2="70"/>
                            <line x1="50" y1="100" x2="850" y2="100"/>
                            <line x1="50" y1="130" x2="850" y2="130"/>
                            <line x1="50" y1="160" x2="850" y2="160"/>
                            <line x1="50" y1="190" x2="850" y2="190"/>
                            <line x1="50" y1="220" x2="850" y2="220"/>
                            <line x1="50" y1="250" x2="850" y2="250"/>
                            <line x1="50" y1="280" x2="850" y2="280"/>
                        </g>
                        
                        <!-- Y-axis labels -->
                        <g fill="#9CA3AF" font-size="11" text-anchor="end">
                            <text x="40" y="50">800M</text>
                            <text x="40" y="80">700M</text>
                            <text x="40" y="110">600M</text>
                            <text x="40" y="140">500M</text>
                            <text x="40" y="170">400M</text>
                            <text x="40" y="200">300M</text>
                            <text x="40" y="230">200M</text>
                            <text x="40" y="260">100M</text>
                            <text x="40" y="290">0</text>
                        </g>
                        
                        <!-- Chart line matching uploaded image curve -->
                        <path
                            d="M50,260 Q120,240 180,220 Q240,200 300,180 Q360,160 420,140 Q480,120 540,100 Q600,85 660,75 Q720,68 780,65 Q820,63 850,62"
                            stroke="#22c55e"
                            stroke-width="2.5"
                            fill="none"
                        />
                        
                        <!-- Fill area under curve -->
                        <path
                            d="M50,260 Q120,240 180,220 Q240,200 300,180 Q360,160 420,140 Q480,120 540,100 Q600,85 660,75 Q720,68 780,65 Q820,63 850,62 L850,290 L50,290 Z"
                            fill="url(#chartGradient)"
                        />
                        
                        <!-- X-axis numbers -->
                        <g fill="#9CA3AF" font-size="10" text-anchor="middle">
                            <text x="50" y="305">0</text>
                            <text x="85" y="305">1</text>
                            <text x="120" y="305">2</text>
                            <text x="155" y="305">3</text>
                            <text x="190" y="305">4</text>
                            <text x="225" y="305">5</text>
                            <text x="260" y="305">6</text>
                            <text x="295" y="305">7</text>
                            <text x="330" y="305">8</text>
                            <text x="365" y="305">9</text>
                            <text x="400" y="305">10</text>
                            <text x="435" y="305">11</text>
                            <text x="470" y="305">12</text>
                            <text x="505" y="305">13</text>
                            <text x="540" y="305">14</text>
                            <text x="575" y="305">15</text>
                            <text x="610" y="305">16</text>
                            <text x="645" y="305">17</text>
                            <text x="680" y="305">18</text>
                            <text x="715" y="305">19</text>
                            <text x="750" y="305">20</text>
                            <text x="785" y="305">21</text>
                            <text x="820" y="305">22</text>
                        </g>
                    </svg>
                </div>
            </div>

            <!-- Movie Database Features -->
            <div class="mb-8">
                <h2 class="text-xl font-semibold text-white mb-6">Explore example apps</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <!-- Magic Link -->
                    <div class="bg-gray-900/50 rounded-lg p-6">
                        <div class="flex items-center space-x-3 mb-4">
                            <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                <div class="w-6 h-6 bg-blue-500 rounded"></div>
                            </div>
                            <span class="text-white font-medium">Magic link</span>
                        </div>
                        
                        <div class="flex items-center space-x-4 text-sm">
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-blue-500 rounded-sm"></div>
                                <span class="text-gray-400">React + JS</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-green-500 rounded-sm"></div>
                                <span class="text-gray-400">Node GitHub</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-green-600 rounded-sm"></div>
                                <span class="text-gray-400">Mongo DB</span>
                            </div>
                        </div>
                    </div>

                    <!-- SMS OTP -->
                    <div class="bg-gray-900/50 rounded-lg p-6">
                        <div class="flex items-center space-x-3 mb-4">
                            <div class="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                                </svg>
                            </div>
                            <span class="text-white font-medium">SMS OTP</span>
                        </div>
                        
                        <div class="flex items-center space-x-4 text-sm">
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-blue-500 rounded-sm"></div>
                                <span class="text-gray-400">React + JS</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-green-500 rounded-sm"></div>
                                <span class="text-gray-400">Node GitHub</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-4 h-4 bg-green-600 rounded-sm"></div>
                                <span class="text-gray-400">Mongo DB</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Documentation Section -->
            <div>
                <h2 class="text-xl font-semibold text-white mb-6">Documentation & support</h2>
                
                <div class="bg-gray-900/50 rounded-lg p-6">
                    <div class="flex items-start space-x-4">
                        <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                            <div class="w-6 h-6 bg-green-500 rounded"></div>
                        </div>
                        <div>
                            <h3 class="text-white font-semibold mb-2">Documentation & support</h3>
                            <p class="text-gray-400 text-sm leading-relaxed">
                                Learn how to quickly connect and deploy The Matrix movie database by reading our extensive documentation. If you have questions or need assistance, join our community Slack channel to talk to us. We're here to help!
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = '/';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def landing():
    """Landing page matching first uploaded image"""
    return render_template_string(LANDING_HTML)

@app.route('/auth')
def auth():
    """Authentication page"""
    return render_template_string(AUTH_HTML)

@app.route('/dashboard')
def dashboard():
    """Dashboard matching second uploaded image"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def api_stats():
    """Get movie database statistics"""
    try:
        movies_count = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)[0]['count']
        genres_count = execute_query("SELECT COUNT(*) as count FROM movie_genres", fetch=True)[0]['count'] 
        cast_count = execute_query("SELECT COUNT(*) as count FROM movie_cast", fetch=True)[0]['count']
        
        return jsonify({
            'movies_total': movies_count,
            'genres_total': genres_count, 
            'cast_total': cast_count,
            'active_users': 1234,
            'magic_links': 856,
            'sms_otp': 523
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies')
def get_movies():
    """Get movies from database"""
    try:
        movies = execute_query("""
            SELECT m.id, m.title, m.year, m.runtime, m.rating, 
                   m.director, m.plot, m.poster_url,
                   STRING_AGG(DISTINCT mg.genre, ', ') as genres
            FROM movies m
            LEFT JOIN movie_genres mg ON m.id = mg.movie_id
            GROUP BY m.id, m.title, m.year, m.runtime, m.rating, m.director, m.plot, m.poster_url
            ORDER BY m.year DESC
            LIMIT 10
        """, fetch=True)
        
        return jsonify({'movies': [dict(movie) for movie in movies]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Simple validation for demo
        if email and password:
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Signup endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if email and password and name:
            return jsonify({'success': True, 'message': 'Account created successfully'})
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Test database connection
    try:
        stats = execute_query("SELECT COUNT(*) as count FROM movies", fetch=True)
        print(f"✅ Database connected! Found {stats[0]['count']} movies.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        
    print("🚀 Starting The Matrix on http://0.0.0.0:5000")
    print("🎬 Features:")
    print("  - Landing page matching uploaded design")
    print("  - Professional authentication with notifications")
    print("  - Dashboard with exact UI from uploaded image")
    print("  - Responsive design for all devices")
    print("  - Working movie database backend")
    
    app.run(host='0.0.0.0', port=5000, debug=True)