'use client'

import { useState } from 'react'
import { 
  Home, 
  Settings, 
  BookOpen, 
  ChevronRight,
  User,
  Save,
  Shield,
  Bell,
  Globe,
  Key,
  Trash2,
  AlertTriangle,
  Eye,
  EyeOff
} from 'lucide-react'
import Link from 'next/link'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general')
  const [showApiKeys, setShowApiKeys] = useState(false)
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    security: true
  })
  const [apiSettings, setApiSettings] = useState({
    rateLimit: 100,
    timeout: 30,
    retries: 3
  })

  const sidebarItems = [
    { 
      category: 'API Management',
      items: [
        { icon: Home, label: 'Overview', href: '/dashboard' },
      ]
    },
    {
      category: 'Developer Tools', 
      items: [
        { icon: BookOpen, label: 'Documentation', href: '/documentation' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', active: true, href: '/settings' },
      ]
    }
  ]

  const deleteAccount = async () => {
    if (confirm('⚠️ WARNING: This will permanently delete your account and ALL your data including API keys and usage history. This action CANNOT be undone. Type "DELETE" to confirm.')) {
      const confirmation = prompt('Type "DELETE" to confirm account deletion:')
      if (confirmation === 'DELETE') {
        try {
          const response = await fetch(`/api/auth/account/1`, {
            method: 'DELETE'
          })
          if (response.ok) {
            alert('Account deleted successfully')
            localStorage.clear()
            window.location.href = '/'
          }
        } catch (error) {
          console.error('Failed to delete account:', error)
          alert('Failed to delete account. Please try again.')
        }
      }
    }
  }

  const saveSettings = () => {
    alert('Settings saved successfully!')
  }

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Sidebar */}
      <div className="w-64 bg-black border-r border-gray-800 p-6 flex flex-col">
        <div className="mb-8">
          <div className="text-2xl font-bold text-green-400">The Matrix</div>
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
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-black border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Settings</h1>
            <p className="text-gray-400 text-sm">Manage your account and API preferences</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-black" />
            </div>
          </div>
        </header>

        <div className="flex-1 flex">
          {/* Settings Navigation */}
          <div className="w-64 bg-gray-900/30 border-r border-gray-800 p-6">
            <nav className="space-y-1">
              {[
                { id: 'general', label: 'General', icon: Settings },
                { id: 'security', label: 'Security', icon: Shield },
                { id: 'notifications', label: 'Notifications', icon: Bell },
                { id: 'api', label: 'API Settings', icon: Key },
                { id: 'advanced', label: 'Advanced', icon: Globe },
                { id: 'account', label: 'Account Management', icon: AlertTriangle }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-green-900/50 text-green-400 border border-green-800'
                      : 'text-gray-300 hover:text-white hover:bg-gray-800'
                  }`}
                >
                  <tab.icon className="mr-3 h-4 w-4" />
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Settings Content */}
          <main className="flex-1 overflow-y-auto p-6">
            {activeTab === 'general' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">General Settings</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Profile Information</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                      <input
                        type="email"
                        defaultValue="developer@example.com"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Display Name</label>
                      <input
                        type="text"
                        defaultValue="Developer"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Timezone</label>
                      <select className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent">
                        <option>UTC</option>
                        <option>America/New_York</option>
                        <option>Europe/London</option>
                        <option>Asia/Tokyo</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">Security Settings</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Password</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Current Password</label>
                      <input
                        type="password"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">New Password</label>
                      <input
                        type="password"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Confirm New Password</label>
                      <input
                        type="password"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Two-Factor Authentication</h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white">Enable 2FA for enhanced security</p>
                      <p className="text-gray-400 text-sm">Adds an extra layer of protection to your account</p>
                    </div>
                    <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors">
                      Enable 2FA
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'notifications' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">Notification Preferences</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <div className="space-y-4">
                    {Object.entries(notifications).map(([key, value]) => (
                      <div key={key} className="flex items-center justify-between">
                        <div>
                          <p className="text-white capitalize">{key} Notifications</p>
                          <p className="text-gray-400 text-sm">
                            {key === 'email' && 'Receive updates via email'}
                            {key === 'push' && 'Browser push notifications'}
                            {key === 'security' && 'Security alerts and warnings'}
                          </p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={value}
                            onChange={(e) => setNotifications(prev => ({ ...prev, [key]: e.target.checked }))}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'api' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">API Configuration</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Default Settings</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Rate Limit (requests/day)</label>
                      <input
                        type="number"
                        value={apiSettings.rateLimit}
                        onChange={(e) => setApiSettings(prev => ({ ...prev, rateLimit: parseInt(e.target.value) }))}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Request Timeout (seconds)</label>
                      <input
                        type="number"
                        value={apiSettings.timeout}
                        onChange={(e) => setApiSettings(prev => ({ ...prev, timeout: parseInt(e.target.value) }))}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Max Retries</label>
                      <input
                        type="number"
                        value={apiSettings.retries}
                        onChange={(e) => setApiSettings(prev => ({ ...prev, retries: parseInt(e.target.value) }))}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'advanced' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">Advanced Settings</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Developer Options</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-white">Debug Mode</p>
                        <p className="text-gray-400 text-sm">Enable detailed API response logging</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                      </label>
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-white">Beta Features</p>
                        <p className="text-gray-400 text-sm">Access experimental API features</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" />
                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                      </label>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Webhook URL</label>
                      <input
                        type="url"
                        placeholder="https://your-app.com/webhook"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                      <p className="text-gray-400 text-sm mt-1">Receive real-time notifications about your API usage</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'account' && (
              <div className="max-w-2xl space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-4">Account Management</h2>
                </div>

                <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Export Data</h3>
                  <p className="text-gray-300 mb-4">Download all your account data including API usage history</p>
                  <button className="bg-green-500 hover:bg-green-400 text-black px-4 py-2 rounded-lg font-medium transition-colors">
                    Export Data
                  </button>
                </div>

                <div className="bg-red-900/20 border border-red-700 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-red-400 mb-4 flex items-center">
                    <AlertTriangle className="w-5 h-5 mr-2" />
                    Danger Zone
                  </h3>
                  <p className="text-gray-300 mb-4">
                    Permanently delete your account and all associated data. This action cannot be undone.
                  </p>
                  <button
                    onClick={deleteAccount}
                    className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete Account
                  </button>
                </div>
              </div>
            )}

            {/* Save Button */}
            <div className="mt-8 pt-6 border-t border-gray-700">
              <button
                onClick={saveSettings}
                className="bg-green-500 hover:bg-green-400 text-black px-6 py-2 rounded-lg font-medium transition-colors flex items-center"
              >
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}