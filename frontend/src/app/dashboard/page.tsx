'use client'

import { useState, useEffect } from 'react'
import { 
  Home, 
  Key, 
  BarChart3, 
  Settings, 
  BookOpen, 
  Activity,
  ChevronRight,
  User,
  Eye,
  EyeOff,
  Copy,
  Plus,
  Trash2,
  RefreshCw
} from 'lucide-react'
import Link from 'next/link'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [apiRequests, setApiRequests] = useState(0)
  const [apiKeys, setApiKeys] = useState([])
  const [selectedKey, setSelectedKey] = useState(null)
  const [showKey, setShowKey] = useState(false)
  
  // Mock usage data
  const usageData = [
    { time: '0h', requests: 150 },
    { time: '3h', requests: 230 },
    { time: '6h', requests: 189 },
    { time: '9h', requests: 278 },
    { time: '12h', requests: 345 },
    { time: '15h', requests: 420 },
    { time: '18h', requests: 380 },
    { time: '21h', requests: 290 },
  ]

  useEffect(() => {
    // Load user data from localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }

    // Generate initial API key
    const savedKeys = localStorage.getItem('apiKeys')
    if (!savedKeys) {
      const initialKey = {
        id: 'api_key_1',
        name: 'Default API Key',
        key: 'mk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
        created: new Date().toISOString(),
        lastUsed: new Date().toISOString(),
        requests: 1247
      }
      setApiKeys([initialKey])
      localStorage.setItem('apiKeys', JSON.stringify([initialKey]))
    } else {
      setApiKeys(JSON.parse(savedKeys))
    }

    // Animate request counter
    const timer = setInterval(() => {
      setApiRequests(prev => prev < 1247 ? prev + 15 : 1247)
    }, 100)

    return () => clearInterval(timer)
  }, [])

  const sidebarItems = [
    { 
      category: 'API Management',
      items: [
        { icon: Home, label: 'Overview', active: true, href: '/dashboard' },
        { icon: Key, label: 'API Keys', href: '/dashboard/keys' },
        { icon: BarChart3, label: 'Analytics', href: '/dashboard/analytics' },
      ]
    },
    {
      category: 'Developer Tools', 
      items: [
        { icon: BookOpen, label: 'Documentation', href: '/docs' },
        { icon: Activity, label: 'API Testing', href: '/dashboard/testing' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', href: '/dashboard/settings' },
      ]
    }
  ]

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    // Could add a toast notification here
  }

  const generateNewKey = () => {
    const newKey = {
      id: 'api_key_' + (apiKeys.length + 1),
      name: `API Key ${apiKeys.length + 1}`,
      key: 'mk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
      created: new Date().toISOString(),
      lastUsed: null,
      requests: 0
    }
    const updatedKeys = [...apiKeys, newKey]
    setApiKeys(updatedKeys)
    localStorage.setItem('apiKeys', JSON.stringify(updatedKeys))
  }

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Sidebar */}
      <div className="w-64 bg-black border-r border-gray-800 p-6 flex flex-col">
        <div className="mb-8">
          <Link href="/" className="text-2xl font-bold text-green-400">The Matrix</Link>
          <p className="text-xs text-gray-500 mt-1">Movie API Platform</p>
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
                    href={item.href || '#'}
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

        {/* Support Section */}
        <div className="border-t border-gray-800 pt-6">
          <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-800 cursor-pointer">
            <BookOpen className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium">API Documentation</p>
              <p className="text-xs text-gray-500">Get help & examples</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold">API Dashboard</h2>
            <p className="text-gray-400">Manage your movie API access and monitor usage</p>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/docs" className="text-gray-400 cursor-pointer hover:text-white">Docs</Link>
            <Link href="#support" className="text-gray-400 cursor-pointer hover:text-white">Support</Link>
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-black" />
              </div>
              <div className="text-right">
                <p className="text-sm font-medium">{user?.email || 'Developer'}</p>
                <button 
                  onClick={() => {
                    localStorage.removeItem('user')
                    localStorage.removeItem('apiKeys')
                    window.location.href = '/auth'
                  }}
                  className="text-xs text-gray-400 cursor-pointer hover:text-white"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-6 overflow-auto">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-gray-900/50 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Requests</p>
                  <p className="text-2xl font-bold text-white">{apiRequests.toLocaleString()}</p>
                </div>
                <Activity className="w-8 h-8 text-green-400" />
              </div>
            </div>
            
            <div className="bg-gray-900/50 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">API Keys</p>
                  <p className="text-2xl font-bold text-white">{apiKeys.length}</p>
                </div>
                <Key className="w-8 h-8 text-blue-400" />
              </div>
            </div>
            
            <div className="bg-gray-900/50 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">This Month</p>
                  <p className="text-2xl font-bold text-white">8,450</p>
                </div>
                <BarChart3 className="w-8 h-8 text-purple-400" />
              </div>
            </div>
            
            <div className="bg-gray-900/50 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Rate Limit</p>
                  <p className="text-2xl font-bold text-white">1000/hr</p>
                </div>
                <RefreshCw className="w-8 h-8 text-orange-400" />
              </div>
            </div>
          </div>

          {/* Usage Chart */}
          <div className="bg-gray-900/50 rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold mb-6">API Usage (Last 24 Hours)</h3>
            <div className="h-64 relative">
              <svg className="w-full h-full" viewBox="0 0 900 240">
                <defs>
                  <linearGradient id="usageGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#22c55e', stopOpacity: 0.3 }} />
                    <stop offset="100%" style={{ stopColor: '#22c55e', stopOpacity: 0 }} />
                  </linearGradient>
                </defs>
                
                {/* Grid lines */}
                {[0, 1, 2, 3, 4, 5, 6].map(i => (
                  <line
                    key={i}
                    x1="50"
                    y1={30 + i * 30}
                    x2="850"
                    y2={30 + i * 30}
                    stroke="#374151"
                    strokeWidth="0.5"
                  />
                ))}
                
                {/* Y-axis labels */}
                <text x="30" y="35" fill="#9CA3AF" fontSize="10">500</text>
                <text x="30" y="65" fill="#9CA3AF" fontSize="10">400</text>
                <text x="30" y="95" fill="#9CA3AF" fontSize="10">300</text>
                <text x="30" y="125" fill="#9CA3AF" fontSize="10">200</text>
                <text x="30" y="155" fill="#9CA3AF" fontSize="10">100</text>
                <text x="40" y="185" fill="#9CA3AF" fontSize="10">0</text>
                
                {/* Chart line */}
                <path
                  d="M50,150 L150,120 L250,140 L350,90 L450,75 L550,95 L650,110 L750,130 L850,120"
                  stroke="#22c55e"
                  strokeWidth="2"
                  fill="none"
                />
                
                {/* Fill area under curve */}
                <path
                  d="M50,150 L150,120 L250,140 L350,90 L450,75 L550,95 L650,110 L750,130 L850,120 L850,185 L50,185 Z"
                  fill="url(#usageGradient)"
                />
                
                {/* X-axis labels */}
                {usageData.map((data, i) => (
                  <text key={i} x={50 + i * 100} y="205" fill="#9CA3AF" fontSize="10">{data.time}</text>
                ))}
              </svg>
            </div>
          </div>

          {/* API Keys Section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold">API Keys</h3>
              <button 
                onClick={generateNewKey}
                className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>New API Key</span>
              </button>
            </div>
            
            <div className="space-y-4">
              {apiKeys.map((key) => (
                <div key={key.id} className="bg-gray-900/50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="text-white font-medium">{key.name}</h4>
                      <p className="text-sm text-gray-400">Created {new Date(key.created).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-400">{key.requests} requests</span>
                      <button className="p-2 text-gray-400 hover:text-red-400 transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-black border border-gray-700 rounded-lg px-4 py-2 font-mono text-sm">
                      {showKey === key.id ? key.key : key.key.replace(/./g, '•')}
                    </div>
                    <button 
                      onClick={() => setShowKey(showKey === key.id ? null : key.id)}
                      className="p-2 text-gray-400 hover:text-white transition-colors"
                    >
                      {showKey === key.id ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    <button 
                      onClick={() => copyToClipboard(key.key)}
                      className="p-2 text-gray-400 hover:text-white transition-colors"
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Start */}
          <div className="bg-gray-900/50 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">Quick Start</h3>
            <p className="text-gray-400 mb-4">Get started with the Movie API in minutes:</p>
            
            <div className="bg-black border border-gray-700 rounded-lg p-4 font-mono text-sm mb-4">
              <div className="text-blue-400">curl -H "X-API-Key: {apiKeys[0]?.key || 'your_api_key'}" \</div>
              <div className="text-blue-400 ml-4">https://api.matrix.to/movies?search=matrix</div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link href="/docs" className="px-4 py-2 bg-green-500 text-black rounded-lg hover:bg-green-400 font-medium transition-colors">
                View Documentation
              </Link>
              <Link href="/dashboard/testing" className="px-4 py-2 border border-gray-600 rounded-lg hover:border-gray-500 transition-colors">
                Test API
              </Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}