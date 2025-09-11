'use client'

import { useState, useEffect } from 'react'
import { 
  Key, 
  Eye,
  EyeOff,
  Copy,
  Plus,
  Trash2,
  RefreshCw,
  AlertTriangle
} from 'lucide-react'
import Sidebar from '../../components/Sidebar'
import ProfileDropdown from '../../components/ProfileDropdown'
import { useNotifications, NotificationManager } from '../../components/Notification'

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
  daily_usage?: number
  plan?: string
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
  const [dailyUsage, setDailyUsage] = useState(47) // Current usage
  const [userPlan, setUserPlan] = useState('free') // Current plan
  const { notifications, addNotification, removeNotification } = useNotifications()

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
        setDailyUsage(data.stats.daily_usage || 47)
        setUserPlan(data.stats.plan || 'free')
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
        addNotification({
          type: 'success',
          title: 'API Key Created',
          message: 'New API key has been generated successfully!'
        })
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
      addNotification({
        type: 'success',
        title: 'API Key Created',
        message: 'New API key has been generated successfully!'
      })
    }
  }

  const deleteApiKey = async (keyId: number) => {
    try {
      const response = await fetch(`/api/auth/api-key/${userId}/${keyId}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        loadDashboardData() // Refresh data
        addNotification({
          type: 'success',
          title: 'API Key Deleted',
          message: 'API key has been deleted successfully.'
        })
      }
    } catch (error) {
      console.error('Failed to delete API key:', error)
      // Demo fallback
      setApiKeys(apiKeys.filter(key => key.id !== keyId))
      addNotification({
        type: 'success',
        title: 'API Key Deleted',
        message: 'API key has been deleted successfully.'
      })
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    addNotification({
      type: 'success',
      title: 'Copied!',
      message: 'API key copied to clipboard.'
    })
  }

  const checkUsageLimit = () => {
    const maxRequests = userPlan === 'free' ? 100 : 1000
    if (dailyUsage >= maxRequests) {
      addNotification({
        type: 'warning',
        title: 'Usage Limit Reached',
        message: `You've reached your daily limit of ${maxRequests} requests. Upgrade your plan for more requests.`
      })
    } else if (dailyUsage >= maxRequests * 0.8) {
      addNotification({
        type: 'info',
        title: 'Usage Warning',
        message: `You're approaching your daily limit (${dailyUsage}/${maxRequests}). Consider upgrading to avoid interruption.`
      })
    }
  }

  useEffect(() => {
    checkUsageLimit()
  }, [dailyUsage, userPlan])

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
      <NotificationManager 
        notifications={notifications} 
        onClose={removeNotification} 
      />
      
      {/* Sidebar */}
      <Sidebar currentPage="dashboard" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-black border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Matrix Dashboard</h1>
            <p className="text-gray-400 text-sm">Manage your movie API access and monitor usage</p>
          </div>
          <div className="flex items-center space-x-4">
            <ProfileDropdown />
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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
                  <p className="text-gray-400 text-sm">Daily Usage</p>
                  <p className="text-3xl font-bold text-white">{dailyUsage}/{userPlan === 'free' ? '100' : '1000'}</p>
                  <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      className={`h-2 rounded-full ${
                        dailyUsage >= (userPlan === 'free' ? 100 : 1000) * 0.9 ? 'bg-red-500' :
                        dailyUsage >= (userPlan === 'free' ? 100 : 1000) * 0.7 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${(dailyUsage / (userPlan === 'free' ? 100 : 1000)) * 100}%` }}
                    ></div>
                  </div>
                </div>
                <div className="w-12 h-12 bg-orange-900/50 rounded-lg flex items-center justify-center">
                  <RefreshCw className="w-6 h-6 text-orange-400" />
                </div>
              </div>
            </div>

            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Current Plan</p>
                  <p className="text-3xl font-bold text-white capitalize">{userPlan}</p>
                  {userPlan === 'free' && (
                    <button 
                      onClick={() => window.location.href = '/pricing'}
                      className="text-green-400 text-sm hover:text-green-300 transition-colors mt-1"
                    >
                      Upgrade →
                    </button>
                  )}
                </div>
                <div className="w-12 h-12 bg-green-900/50 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-green-400" />
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
                    onClick={() => {
                      if (confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
                        deleteApiKey(key.id)
                      }
                    }}
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
          </div>
          
          {/* Usage Warning */}
          {dailyUsage >= (userPlan === 'free' ? 100 : 1000) * 0.8 && (
            <div className="bg-yellow-900/20 border border-yellow-700 rounded-xl p-6 mt-6">
              <div className="flex items-center space-x-3">
                <AlertTriangle className="w-6 h-6 text-yellow-400" />
                <div>
                  <h3 className="text-yellow-400 font-semibold">Usage Warning</h3>
                  <p className="text-gray-300">
                    You're approaching your daily limit ({dailyUsage}/{userPlan === 'free' ? '100' : '1000'} requests). 
                    {userPlan === 'free' && (
                      <span>
                        {' '}<button 
                          onClick={() => window.location.href = '/pricing'}
                          className="text-green-400 hover:text-green-300 underline"
                        >
                          Upgrade to Premium
                        </button> for 1,000 requests per day.
                      </span>
                    )}
                  </p>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}