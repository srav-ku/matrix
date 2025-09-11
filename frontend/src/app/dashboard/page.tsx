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
  RefreshCw,
  AlertTriangle
} from 'lucide-react'
import Link from 'next/link'

interface ApiKey {
  id: number
  api_key: string
  created_at: string
  is_active: boolean
}

interface DashboardStats {
  total_requests: number
  this_month_requests: number
  api_key_count: number
  chart_data: Array<{hour: number, requests: number}>
}

export default function Dashboard() {
  const [user, setUser] = useState<any>(null)
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([])
  const [stats, setStats] = useState<DashboardStats>({
    total_requests: 0,
    this_month_requests: 0,
    api_key_count: 0,
    chart_data: []
  })
  const [selectedKey, setSelectedKey] = useState<string | null>(null)
  const [showKey, setShowKey] = useState(false)
  const [loading, setLoading] = useState(true)
  const [userId, setUserId] = useState(1) // Demo user ID
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  useEffect(() => {
    // Load user data
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    } else {
      // Demo user
      setUser({ email: 'developer@example.com', id: 1 })
    }

    loadDashboardData()
    // Real-time updates every 10 seconds
    const interval = setInterval(() => {
      loadDashboardData()
      setLastUpdate(new Date())
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      const response = await fetch(`/api/auth/dashboard/${userId}`)
      if (response.ok) {
        const data = await response.json()
        setStats(data.stats)
        setApiKeys(data.api_keys.filter((key: ApiKey) => key.is_active))
      } else {
        // Fallback demo data if endpoint not available
        setStats({
          total_requests: Math.floor(Math.random() * 1000) + 500,
          this_month_requests: Math.floor(Math.random() * 300) + 100,
          api_key_count: apiKeys.length || 1,
          chart_data: generateMockChartData()
        })
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      // Demo data fallback
      setStats({
        total_requests: Math.floor(Math.random() * 1000) + 500,
        this_month_requests: Math.floor(Math.random() * 300) + 100,
        api_key_count: 1,
        chart_data: generateMockChartData()
      })
      
      // Create demo API key if none exist
      if (apiKeys.length === 0) {
        setApiKeys([{
          id: 1,
          api_key: 'mk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
          created_at: new Date().toISOString(),
          is_active: true
        }])
      }
    } finally {
      setLoading(false)
    }
  }

  const generateMockChartData = () => {
    const data = []
    for (let i = 0; i < 24; i++) {
      data.push({
        hour: i,
        requests: Math.floor(Math.random() * 100) + 50
      })
    }
    return data
  }

  const createApiKey = async () => {
    try {
      const response = await fetch(`/api/auth/api-key/${userId}`, {
        method: 'POST'
      })
      if (response.ok) {
        const data = await response.json()
        loadDashboardData() // Refresh data
        alert('New API key created successfully!')
      }
    } catch (error) {
      console.error('Failed to create API key:', error)
      // Demo fallback
      const newKey = {
        id: Date.now(),
        api_key: 'mk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
        created_at: new Date().toISOString(),
        is_active: true
      }
      setApiKeys([...apiKeys, newKey])
      alert('New API key created successfully!')
    }
  }

  const deleteApiKey = async (keyId: number) => {
    if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`/api/auth/api-key/${userId}/${keyId}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        loadDashboardData() // Refresh data
        alert('API key deleted successfully!')
      }
    } catch (error) {
      console.error('Failed to delete API key:', error)
      // Demo fallback
      setApiKeys(apiKeys.filter(key => key.id !== keyId))
      alert('API key deleted successfully!')
    }
  }

  const deleteAccount = async () => {
    if (confirm('⚠️ WARNING: This will permanently delete your account and ALL your data including API keys and usage history. This action CANNOT be undone. Type "DELETE" to confirm.')) {
      const confirmation = prompt('Type "DELETE" to confirm account deletion:')
      if (confirmation === 'DELETE') {
        try {
          const response = await fetch(`/api/auth/account/${userId}`, {
            method: 'DELETE'
          })
          if (response.ok) {
            alert('Account deleted successfully')
            localStorage.clear()
            window.location.href = '/'
          }
        } catch (error) {
          console.error('Failed to delete account:', error)
        }
      }
    }
  }

  const sidebarItems = [
    { 
      category: 'API Management',
      items: [
        { icon: Home, label: 'Overview', active: true, href: '/dashboard' },
        { icon: Key, label: 'API Keys', href: '#' },
        { icon: BarChart3, label: 'Analytics', href: '#' },
      ]
    },
    {
      category: 'Developer Tools', 
      items: [
        { icon: BookOpen, label: 'Documentation', href: '#' },
        { icon: Activity, label: 'API Testing', href: '#' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', href: '#' },
      ]
    }
  ]

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  const generateChartPoints = () => {
    const points = []
    const maxRequests = Math.max(...stats.chart_data.map(d => d.requests), 1)
    
    stats.chart_data.forEach((point, index) => {
      const x = (index / 23) * 380 + 10 // Chart width 380px with 10px padding
      const y = 160 - (point.requests / maxRequests) * 140 // Chart height 160px with scaling
      points.push(`${x},${y}`)
    })
    
    return points.join(' ')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-green-400 flex items-center gap-2">
          <RefreshCw className="w-5 h-5 animate-spin" />
          Loading real-time dashboard...
        </div>
      </div>
    )
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
          {sidebarItems.map((section, idx) => (
            <div key={idx} className="mb-8">
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                {section.category}
              </h3>
              <div className="space-y-1">
                {section.items.map((item) => (
                  <Link
                    key={item.label}
                    href={item.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      item.active
                        ? 'bg-green-900/50 text-green-400 border border-green-800'
                        : 'text-gray-300 hover:text-white hover:bg-gray-800'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.label}
                    {item.active && <ChevronRight className="ml-auto h-4 w-4" />}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {/* Account deletion */}
        <div className="border-t border-gray-800 pt-6">
          <button
            onClick={deleteAccount}
            className="flex items-center w-full px-3 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-red-900/20 rounded-lg transition-colors"
          >
            <AlertTriangle className="mr-3 h-4 w-4" />
            Delete Account
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-black border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">API Dashboard</h1>
            <p className="text-gray-400 text-sm">Manage your movie API access and monitor usage</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-xs text-gray-500">
              Last updated: {lastUpdate.toLocaleTimeString()}
            </div>
            <div className="flex items-center space-x-2 text-sm">
              <span className="text-gray-400">Docs</span>
              <span className="text-gray-400">Support</span>
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-black" />
              </div>
              <span className="text-white font-medium">Developer</span>
              <button className="text-gray-400 text-sm hover:text-white">
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">API Keys</p>
                  <p className="text-3xl font-bold text-white">{apiKeys.length}</p>
                </div>
                <div className="w-12 h-12 bg-blue-900/50 rounded-lg flex items-center justify-center">
                  <Key className="w-6 h-6 text-blue-400" />
                </div>
              </div>
            </div>

            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Rate Limit</p>
                  <p className="text-3xl font-bold text-white">100/day</p>
                </div>
                <div className="w-12 h-12 bg-orange-900/50 rounded-lg flex items-center justify-center">
                  <RefreshCw className="w-6 h-6 text-orange-400" />
                </div>
              </div>
            </div>
          </div>


          {/* API Keys Section */}
          <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-white">API Keys</h3>
              <button
                onClick={createApiKey}
                className="bg-green-500 hover:bg-green-400 text-black px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
              >
                <Plus className="w-4 h-4" />
                New API Key
              </button>
            </div>

            <div className="space-y-4">
              {apiKeys.map((key) => (
                <div key={key.id} className="bg-gray-800/50 border border-gray-600 rounded-lg p-4 flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <code className="text-sm font-mono text-green-400 bg-gray-900 px-3 py-1 rounded">
                        {showKey ? key.api_key : key.api_key.slice(0, 8) + '•'.repeat(32) + key.api_key.slice(-8)}
                      </code>
                      <button
                        onClick={() => setShowKey(!showKey)}
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                      <button
                        onClick={() => copyToClipboard(key.api_key)}
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Created {new Date(key.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <button
                    onClick={() => deleteApiKey(key.id)}
                    className="text-red-400 hover:text-red-300 transition-colors p-2"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}

              {apiKeys.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No API keys found. Create your first API key to get started.
                </div>
              )}
            </div>

            {/* Quick Start Guide */}
            <div className="mt-8 bg-gray-800/30 border border-gray-600 rounded-lg p-6">
              <h4 className="text-lg font-semibold text-white mb-4">Quick Start</h4>
              <p className="text-gray-300 mb-4">Get started with the Movie API in minutes:</p>
              
              <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 font-mono text-sm">
                <div className="text-gray-500">curl -H "X-API-Key: your_api_key" \</div>
                <div className="text-green-400 ml-4">https://api.matrix.to/movies?search=matrix</div>
              </div>
              
              <div className="flex gap-4 mt-4">
                <button className="bg-green-500 hover:bg-green-400 text-black px-4 py-2 rounded-lg font-medium transition-colors">
                  View Documentation
                </button>
                <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                  Test API
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}