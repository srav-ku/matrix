'use client'

import { useState, useEffect } from 'react'
import { 
  Home, 
  Mail, 
  MessageSquare, 
  Settings, 
  Key, 
  Shield, 
  CreditCard, 
  HelpCircle,
  Users,
  BarChart3,
  Activity,
  ChevronRight,
  User
} from 'lucide-react'
import Link from 'next/link'

export default function Dashboard() {
  const [activeUsers, setActiveUsers] = useState(0)
  const [magicLinks, setMagicLinks] = useState(0)
  const [smsOTP, setSmsOTP] = useState(0)
  
  // Mock data for chart
  const chartData = [
    { time: '0', users: 100 },
    { time: '3', users: 150 },
    { time: '6', users: 200 },
    { time: '9', users: 280 },
    { time: '12', users: 350 },
    { time: '15', users: 420 },
    { time: '18', users: 500 },
    { time: '21', users: 580 },
  ]

  useEffect(() => {
    // Animate counters
    const timer = setInterval(() => {
      setActiveUsers(prev => prev < 600 ? prev + 10 : 600)
      setMagicLinks(prev => prev < 300 ? prev + 5 : 300)
      setSmsOTP(prev => prev < 450 ? prev + 8 : 450)
    }, 100)

    return () => clearInterval(timer)
  }, [])

  const sidebarItems = [
    { 
      category: 'Customization',
      items: [
        { icon: Home, label: 'Home', active: true },
        { icon: Mail, label: 'Email' },
        { icon: MessageSquare, label: 'SMS' },
      ]
    },
    {
      category: 'Configuration', 
      items: [
        { icon: Key, label: 'API Keys' },
        { icon: Shield, label: 'Auth Token' },
      ]
    },
    {
      category: 'Application',
      items: [
        { icon: CreditCard, label: 'Plan & Billing' },
        { icon: HelpCircle, label: 'Contact Us' },
      ]
    }
  ]

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Sidebar */}
      <div className="w-64 bg-black border-r border-gray-800 p-6 flex flex-col">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-green-400">The Matrix</h1>
        </div>

        <nav className="flex-1">
          {sidebarItems.map((section, sectionIndex) => (
            <div key={sectionIndex} className="mb-8">
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">
                {section.category}
              </h3>
              <div className="space-y-2">
                {section.items.map((item, itemIndex) => (
                  <Link
                    key={itemIndex}
                    href="#"
                    className={`flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                      item.active 
                        ? 'bg-green-500 text-black font-medium' 
                        : 'text-gray-300 hover:text-white hover:bg-gray-800'
                    }`}
                  >
                    <item.icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {/* Community Section */}
        <div className="border-t border-gray-800 pt-6">
          <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-800 cursor-pointer">
            <Users className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Join our slack community</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">Welcome</h2>
            <p className="text-gray-400">Sed ut perspiciatis unde omnis iste natus error sit voluptatem</p>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-400 cursor-pointer hover:text-white">Docs</span>
            <span className="text-gray-400 cursor-pointer hover:text-white">ezid.io</span>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-black" />
              </div>
              <div className="text-right">
                <p className="text-sm font-medium">Mike Males</p>
                <p className="text-xs text-gray-400 cursor-pointer hover:text-white">Logout</p>
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-6 overflow-auto">
          {/* Active Users Header */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold text-white">Active Users</h3>
              <div className="flex space-x-6 text-sm">
                <span className="text-white font-medium">Active Users</span>
                <span className="text-gray-400">Magic Links</span>
                <span className="text-gray-400">SMS OTP</span>
              </div>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-black rounded-lg p-6 mb-8">
            
            {/* Chart matching uploaded image */}
            <div className="h-80 relative">
              <svg className="w-full h-full" viewBox="0 0 900 320">
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#22c55e', stopOpacity: 0.3 }} />
                    <stop offset="100%" style={{ stopColor: '#22c55e', stopOpacity: 0 }} />
                  </linearGradient>
                </defs>
                
                {/* Grid lines */}
                {[0, 1, 2, 3, 4, 5, 6, 7, 8].map(i => (
                  <line
                    key={i}
                    x1="50"
                    y1={40 + i * 30}
                    x2="850"
                    y2={40 + i * 30}
                    stroke="#374151"
                    strokeWidth="0.5"
                  />
                ))}
                
                {/* Y-axis labels */}
                <text x="30" y="50" fill="#9CA3AF" fontSize="11">800M</text>
                <text x="30" y="80" fill="#9CA3AF" fontSize="11">700M</text>
                <text x="30" y="110" fill="#9CA3AF" fontSize="11">600M</text>
                <text x="30" y="140" fill="#9CA3AF" fontSize="11">500M</text>
                <text x="30" y="170" fill="#9CA3AF" fontSize="11">400M</text>
                <text x="30" y="200" fill="#9CA3AF" fontSize="11">300M</text>
                <text x="30" y="230" fill="#9CA3AF" fontSize="11">200M</text>
                <text x="30" y="260" fill="#9CA3AF" fontSize="11">100M</text>
                <text x="40" y="290" fill="#9CA3AF" fontSize="11">0</text>
                
                {/* Chart line matching uploaded image curve */}
                <path
                  d="M50,260 Q120,240 180,220 Q240,200 300,180 Q360,160 420,140 Q480,120 540,100 Q600,85 660,75 Q720,68 780,65 Q820,63 850,62"
                  stroke="#22c55e"
                  strokeWidth="2.5"
                  fill="none"
                />
                
                {/* Fill area under curve */}
                <path
                  d="M50,260 Q120,240 180,220 Q240,200 300,180 Q360,160 420,140 Q480,120 540,100 Q600,85 660,75 Q720,68 780,65 Q820,63 850,62 L850,290 L50,290 Z"
                  fill="url(#gradient)"
                />
                
                {/* X-axis numbers */}
                {[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22].map((num) => (
                  <text key={num} x={50 + num * 35} y="305" fill="#9CA3AF" fontSize="10">{num}</text>
                ))}
              </svg>
              
            </div>
          </div>

          {/* Example Apps */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-6">Explore example apps</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Magic Link */}
              <div className="bg-gray-900/50 rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <div className="w-6 h-6 bg-blue-500 rounded"></div>
                  </div>
                  <span className="text-white font-medium">Magic link</span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-blue-500 rounded-sm"></div>
                    <span className="text-gray-400">React + JS</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-500 rounded-sm"></div>
                    <span className="text-gray-400">Node GitHub</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-600 rounded-sm"></div>
                    <span className="text-gray-400">Mongo DB</span>
                  </div>
                </div>
              </div>

              {/* SMS OTP */}
              <div className="bg-gray-900/50 rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                    <MessageSquare className="w-6 h-6 text-orange-500" />
                  </div>
                  <span className="text-white font-medium">SMS OTP</span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-blue-500 rounded-sm"></div>
                    <span className="text-gray-400">React + JS</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-500 rounded-sm"></div>
                    <span className="text-gray-400">Node GitHub</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-600 rounded-sm"></div>
                    <span className="text-gray-400">Mongo DB</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Documentation */}
          <div>
            <h3 className="text-xl font-semibold mb-6">Documentation & support</h3>
            
            <div className="bg-gray-900/50 rounded-lg p-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <div className="w-6 h-6 bg-green-500 rounded"></div>
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-2">Documentation & support</h4>
                  <p className="text-gray-400 text-sm leading-relaxed">
                    Learn how to quickly connect and deploy EzID by reading our extensive documentation. If you have questions or need assistance, join our community Slack channel to talk to us. We're here to help!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}