'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Shield, Smartphone, Code } from 'lucide-react'

export default function HomePage() {
  const [otpCode, setOtpCode] = useState('')

  return (
    <div className="min-h-screen gradient-bg text-white">
      {/* Header */}
      <header className="flex justify-between items-center p-6">
        <div className="flex items-center space-x-2">
          <div className="text-2xl font-bold">ezId</div>
        </div>
        <nav className="hidden md:flex items-center space-x-8">
          <Link href="#" className="text-gray-300 hover:text-white">Use cases</Link>
          <Link href="#" className="text-gray-300 hover:text-white">Product</Link>
          <Link href="#" className="text-gray-300 hover:text-white">Docs</Link>
          <Link href="#" className="text-gray-300 hover:text-white">Pricing</Link>
          <Link href="#" className="text-gray-300 hover:text-white">Resources</Link>
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 border border-gray-600 rounded-lg hover:border-gray-500">
              Book a demo
            </button>
            <Link href="/dashboard" className="px-4 py-2 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium">
              Log in
            </Link>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex flex-col items-center justify-center px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl md:text-7xl font-bold mb-6">
            Build seamless <span className="text-green-500">auth</span> experiences
          </h1>
          
          <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
            Use our API to build to improve your customer experience with 
            effortless One Time Passcodes by allowing your users to access 
            your websites or build loyalty in an instant.
          </p>

          <button className="inline-flex items-center px-8 py-4 bg-green-500 text-black rounded-lg hover:bg-green-400 font-semibold text-lg mb-20">
            Get Started
            <ArrowRight className="ml-2 w-5 h-5" />
          </button>

          {/* Demo Cards */}
          <div className="flex flex-col lg:flex-row gap-8 mt-20">
            {/* Messages Card */}
            <div className="flex-1 glass-card rounded-2xl p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-2 text-sm text-gray-400">
                  <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  <span>Messages</span>
                </div>
                <span className="text-xs text-gray-500">09:35:14</span>
              </div>
              
              <div className="text-left mb-8">
                <p className="text-gray-300 mb-2">Your Passcode is</p>
                <p className="text-4xl font-bold">4695</p>
              </div>

              <div className="flex items-center justify-center w-12 h-12 bg-green-500/20 rounded-lg mb-4 mx-auto">
                <Shield className="w-6 h-6 text-green-500" />
              </div>
              <p className="text-sm text-gray-400">Enter Passcode</p>
            </div>

            {/* SMS OTP Card */}
            <div className="flex-1 glass-card rounded-2xl p-8 relative">
              <div className="flex justify-center mb-4">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                </div>
              </div>
              
              <div className="flex items-center justify-center w-16 h-16 bg-green-500/20 rounded-2xl mx-auto mb-6">
                <Smartphone className="w-8 h-8 text-green-500" />
              </div>
              
              <h3 className="text-2xl font-semibold mb-6 text-center">SMS OTP</h3>
              <span className="text-xs text-gray-500 absolute top-4 right-4">09:35:14</span>
              
              <div className="grid grid-cols-6 gap-2 mb-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="aspect-square border border-gray-600 rounded-lg"></div>
                ))}
              </div>
              
              <button className="w-full py-3 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium">
                Verify OTP
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="max-w-6xl mx-auto mt-32 px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Sed ut perspiciatis unde omnis</h2>
            <h3 className="text-4xl font-bold text-gray-400">iste natus error sit</h3>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Authentication Feature */}
            <div className="glass-card rounded-2xl p-8">
              <h3 className="text-2xl font-semibold mb-4">Authentication in just seconds</h3>
              <p className="text-gray-300 mb-6">
                Create seamless Web and Mobile experiences for your users. Don't worry, they 
                won't even have to enter the code, it populates itself, like magic.
              </p>
              
              <div className="space-y-2">
                <div className="flex space-x-1 mb-2">
                  <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                </div>
                <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm">
                  <div className="text-blue-400">curl --request POST \\</div>
                  <div className="text-blue-400 ml-4">--url https://api.ezid.to/send/otp \\</div>
                  <div className="text-blue-400 ml-4">--header 'Content-Type: application/json' \\</div>
                  <div className="text-blue-400 ml-4">--data &apos;{&apos;</div>
                  <div className="text-yellow-300 ml-8">"client_id": "ezid_client_id",</div>
                  <div className="text-yellow-300 ml-8">"client_secret": "ezid_client_secret",</div>
                  <div className="text-yellow-300 ml-8">"digits": "6"</div>
                  <div className="text-yellow-300 ml-8">"channel": "sms",</div>
                  <div className="text-yellow-300 ml-8">"target": "+60 000000",</div>
                  <div className="text-yellow-300 ml-8">"template": "Your code is &lt;code&gt;code&lt;/code&gt;":</div>
                  <div className="text-blue-400 ml-4">&apos;}</div>
                </div>
              </div>
            </div>

            {/* Custom Claims Feature */}
            <div className="space-y-8">
              <div className="glass-card rounded-2xl p-8">
                <h3 className="text-2xl font-semibold mb-4">Add custom claims to control</h3>
                <p className="text-gray-300 mb-6">
                  Use our APIs to create the rience you want for your users. Our clients are available here.
                </p>
                
                <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm">
                  <div className="text-blue-400">"claims: full-access"</div>
                  <div className="text-gray-400 mt-2">"status: read-only"</div>
                  <div className="text-orange-400 mt-4">"claims: editor"</div>
                </div>
              </div>

              <div className="glass-card rounded-2xl p-8">
                <h3 className="text-2xl font-semibold mb-4">Customize OTP Length</h3>
                <p className="text-gray-300 mb-6">
                  Use our APIs to create the rience you want for your users. Our clients are available here.
                </p>
                
                <div className="flex justify-center space-x-4">
                  <div className="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center">5</div>
                  <div className="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center">2</div>
                  <div className="w-12 h-12 border border-green-500 rounded-lg flex items-center justify-center bg-green-500/10">8</div>
                  <div className="w-12 h-12 border border-gray-600 rounded-lg flex items-center justify-center">6</div>
                  <div className="w-8 h-8 border border-gray-600 rounded flex items-center justify-center mt-2">✉</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}