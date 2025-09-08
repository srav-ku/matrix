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
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 p-6 flex flex-col">
        <div className="mb-8">
          <h1 className="text-2xl font-bold">ezId</h1>
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
        <header className="border-b border-gray-800 p-6 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">Welcome</h2>
            <p className="text-gray-400">Sed ut perspiciatis unde omnis iste natus error sit voluptatem</p>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-400">Docs</span>
            <span className="text-gray-400">ezid.io</span>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-black" />
              </div>
              <div>
                <p className="text-sm font-medium">Mike Malex</p>
                <p className="text-xs text-gray-400">Logout</p>
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-6 overflow-auto">
          {/* Stats Section */}
          <div className="grid grid-cols-4 gap-6 mb-8">
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{activeUsers}</div>
              <div className="text-sm text-gray-400">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{magicLinks}</div>
              <div className="text-sm text-gray-400">Magic Links</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{smsOTP}</div>
              <div className="text-sm text-gray-400">SMS OTP</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">Active Users</div>
              <div className="text-sm text-gray-400">Magic Links</div>
            </div>
          </div>

          {/* Chart */}
          <div className="glass-card rounded-2xl p-6 mb-8">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-semibold">Active Users</h3>
              <div className="flex space-x-4 text-sm text-gray-400">
                <span>Active Users</span>
                <span>Magic Links</span>
                <span>SMS OTP</span>
              </div>
            </div>
            
            {/* Simple SVG Chart */}
            <div className="h-64 relative">
              <svg className="w-full h-full" viewBox="0 0 800 200">
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#22c55e', stopOpacity: 0.3 }} />
                    <stop offset="100%" style={{ stopColor: '#22c55e', stopOpacity: 0 }} />
                  </linearGradient>
                </defs>
                
                {/* Grid lines */}
                {[0, 1, 2, 3, 4].map(i => (
                  <line
                    key={i}
                    x1="0"
                    y1={i * 40}
                    x2="800"
                    y2={i * 40}
                    stroke="#374151"
                    strokeWidth="1"
                  />
                ))}
                
                {/* Chart line */}
                <path
                  d="M50,150 Q150,120 250,100 Q350,80 450,60 Q550,45 650,30 Q750,20 750,15"
                  stroke="#22c55e"
                  strokeWidth="3"
                  fill="none"
                />
                
                {/* Fill area */}
                <path
                  d="M50,150 Q150,120 250,100 Q350,80 450,60 Q550,45 650,30 Q750,20 750,15 L750,200 L50,200 Z"
                  fill="url(#gradient)"
                />
                
                {/* Data points */}
                {chartData.map((point, index) => (
                  <circle
                    key={index}
                    cx={50 + index * 100}
                    cy={200 - (point.users / 6)}
                    r="4"
                    fill="#22c55e"
                    className="animate-pulse"
                  />
                ))}
              </svg>
              
              {/* X-axis labels */}
              <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-400 px-12">
                {['0', '3', '6', '9', '12', '15', '18', '21'].map(time => (
                  <span key={time}>{time}</span>
                ))}
              </div>
            </div>
          </div>

          {/* Example Apps */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-6">Explore example apps</h3>
            <div className="grid grid-cols-2 gap-6">
              {/* Magic Link */}
              <div className="glass-card rounded-2xl p-6">
                <h4 className="text-lg font-semibold mb-4">Magic link</h4>
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                    <Activity className="w-5 h-5" />
                  </div>
                  <span className="text-sm text-gray-400">React + JS</span>
                  <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
                    <span className="text-xs text-black font-bold">N</span>
                  </div>
                  <span className="text-sm text-gray-400">Node GitHub</span>
                  <div className="w-6 h-6 bg-green-600 rounded flex items-center justify-center">
                    <span className="text-xs text-white font-bold">M</span>
                  </div>
                  <span className="text-sm text-gray-400">Mongo DB</span>
                </div>
              </div>

              {/* SMS OTP */}
              <div className="glass-card rounded-2xl p-6">
                <h4 className="text-lg font-semibold mb-4">SMS OTP</h4>
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                    <Activity className="w-5 h-5" />
                  </div>
                  <span className="text-sm text-gray-400">React + JS</span>
                  <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
                    <span className="text-xs text-black font-bold">N</span>
                  </div>
                  <span className="text-sm text-gray-400">Node GitHub</span>
                  <div className="w-6 h-6 bg-green-600 rounded flex items-center justify-center">
                    <span className="text-xs text-white font-bold">M</span>
                  </div>
                  <span className="text-sm text-gray-400">Mongo DB</span>
                </div>
              </div>
            </div>
          </div>

          {/* Documentation */}
          <div className="glass-card rounded-2xl p-6">
            <h3 className="text-xl font-semibold mb-4">Documentation & support</h3>
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                <HelpCircle className="w-6 h-6 text-green-500" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold mb-2">Documentation & support</h4>
                <p className="text-gray-400">
                  Learn how to quickly connect and deploy EZID by reading our extensive documentation. 
                  If you have questions or need assistance, join our community Slack channel to talk to us. We're here to help!
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}