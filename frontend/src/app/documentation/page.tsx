'use client'

import { useState } from 'react'
import { 
  Home, 
  Settings, 
  BookOpen, 
  ChevronRight,
  User,
  Copy,
  Code,
  Database,
  Key,
  Search,
  BarChart3,
  Shield
} from 'lucide-react'
import Link from 'next/link'

export default function Documentation() {
  const [copiedEndpoint, setCopiedEndpoint] = useState<string | null>(null)

  const copyToClipboard = (text: string, endpoint: string) => {
    navigator.clipboard.writeText(text)
    setCopiedEndpoint(endpoint)
    setTimeout(() => setCopiedEndpoint(null), 2000)
  }

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
        { icon: BookOpen, label: 'Documentation', active: true, href: '/documentation' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', href: '/settings' },
      ]
    }
  ]

  const endpoints = [
    {
      method: 'GET',
      path: '/api/movies',
      description: 'Get all movies with optional filtering and pagination',
      parameters: [
        { name: 'page', type: 'integer', description: 'Page number (default: 1)' },
        { name: 'limit', type: 'integer', description: 'Results per page (default: 20, max: 100)' },
        { name: 'genre', type: 'string', description: 'Filter by genre' },
        { name: 'year', type: 'integer', description: 'Filter by year' },
        { name: 'search', type: 'string', description: 'Search in title, director, or plot' }
      ],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/movies?limit=5&genre=Action"`
    },
    {
      method: 'GET',
      path: '/api/movies/{id}',
      description: 'Get a specific movie by ID',
      parameters: [
        { name: 'id', type: 'integer', description: 'Movie ID' }
      ],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/movies/1"`
    },
    {
      method: 'GET',
      path: '/api/genres',
      description: 'Get all available genres',
      parameters: [],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/genres"`
    },
    {
      method: 'GET',
      path: '/api/years',
      description: 'Get all available years',
      parameters: [],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/years"`
    },
    {
      method: 'GET',
      path: '/api/search',
      description: 'Search movies by title, director, or plot',
      parameters: [
        { name: 'q', type: 'string', description: 'Search query (required)' }
      ],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/search?q=matrix"`
    },
    {
      method: 'GET',
      path: '/api/stats',
      description: 'Get database statistics',
      parameters: [],
      example: `curl -H "X-API-Key: your_api_key" \\
  "https://api.matrix.to/api/stats"`
    }
  ]

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
            <h1 className="text-2xl font-bold text-white">API Documentation</h1>
            <p className="text-gray-400 text-sm">Complete guide to The Matrix Movie API</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-black" />
            </div>
          </div>
        </header>

        {/* Documentation Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {/* Getting Started */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Getting Started</h2>
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6 mb-6">
              <p className="text-gray-300 mb-4">
                The Matrix Movie API provides access to comprehensive movie data including titles, years, genres, cast, directors, and more.
              </p>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="flex items-start space-x-3">
                  <Shield className="w-6 h-6 text-green-400 mt-1" />
                  <div>
                    <h4 className="text-white font-semibold mb-2">Authentication Required</h4>
                    <p className="text-gray-300 text-sm">All API endpoints require a valid API key sent in the X-API-Key header.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Database className="w-6 h-6 text-green-400 mt-1" />
                  <div>
                    <h4 className="text-white font-semibold mb-2">Rich Dataset</h4>
                    <p className="text-gray-300 text-sm">Access to 50+ classic movies from 1936-2014 with complete metadata.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Base URL */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">Base URL</h3>
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="bg-black border border-gray-800 rounded-lg p-4 font-mono text-sm">
                <span className="text-green-400">https://api.matrix.to</span>
              </div>
            </div>
          </div>

          {/* Authentication */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">Authentication</h3>
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <p className="text-gray-300 mb-4">Include your API key in the request header:</p>
              <div className="bg-black border border-gray-800 rounded-lg p-4 font-mono text-sm mb-4">
                <span className="text-blue-400">X-API-Key: </span>
                <span className="text-green-400">your_api_key_here</span>
              </div>
              <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
                <p className="text-yellow-300 text-sm">
                  <strong>Note:</strong> You can create and manage API keys from your dashboard.
                </p>
              </div>
            </div>
          </div>

          {/* Endpoints */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-6">API Endpoints</h3>
            <div className="space-y-6">
              {endpoints.map((endpoint, index) => (
                <div key={index} className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <span className={`px-3 py-1 rounded text-sm font-semibold ${
                      endpoint.method === 'GET' ? 'bg-green-900/50 text-green-400' :
                      endpoint.method === 'POST' ? 'bg-blue-900/50 text-blue-400' :
                      'bg-gray-700 text-gray-300'
                    }`}>
                      {endpoint.method}
                    </span>
                    <span className="font-mono text-white">{endpoint.path}</span>
                  </div>
                  
                  <p className="text-gray-300 mb-4">{endpoint.description}</p>

                  {endpoint.parameters.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-white font-semibold mb-2">Parameters</h4>
                      <div className="space-y-2">
                        {endpoint.parameters.map((param, idx) => (
                          <div key={idx} className="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-4">
                            <code className="text-green-400 text-sm bg-gray-800 px-2 py-1 rounded">
                              {param.name}
                            </code>
                            <span className="text-blue-400 text-sm">{param.type}</span>
                            <span className="text-gray-300 text-sm">{param.description}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mb-4">
                    <h4 className="text-white font-semibold mb-2">Example Request</h4>
                    <div className="bg-black border border-gray-800 rounded-lg p-4 relative">
                      <pre className="text-sm text-gray-300 overflow-x-auto">
                        {endpoint.example}
                      </pre>
                      <button
                        onClick={() => copyToClipboard(endpoint.example, endpoint.path)}
                        className="absolute top-2 right-2 text-gray-400 hover:text-white transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      {copiedEndpoint === endpoint.path && (
                        <div className="absolute top-2 right-10 text-green-400 text-sm">
                          Copied!
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Response Format */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">Response Format</h3>
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <p className="text-gray-300 mb-4">All responses are returned in JSON format:</p>
              <div className="bg-black border border-gray-800 rounded-lg p-4 font-mono text-sm">
                <div className="text-yellow-300">{'{'}</div>
                <div className="text-blue-400 ml-2">&quot;movies&quot;: [</div>
                <div className="text-yellow-300 ml-4">{'{'}</div>
                <div className="text-green-400 ml-6">&quot;id&quot;: 1,</div>
                <div className="text-green-400 ml-6">&quot;title&quot;: &quot;The Matrix&quot;,</div>
                <div className="text-green-400 ml-6">&quot;year&quot;: 1999,</div>
                <div className="text-green-400 ml-6">&quot;director&quot;: &quot;Wachowski&quot;,</div>
                <div className="text-green-400 ml-6">&quot;rating&quot;: &quot;8.7&quot;,</div>
                <div className="text-green-400 ml-6">&quot;genres&quot;: [&quot;Action&quot;, &quot;Sci-Fi&quot;],</div>
                <div className="text-green-400 ml-6">&quot;cast&quot;: [&quot;Keanu Reeves&quot;, &quot;Laurence Fishburne&quot;]</div>
                <div className="text-yellow-300 ml-4">{'}'}</div>
                <div className="text-blue-400 ml-2">],</div>
                <div className="text-blue-400 ml-2">&quot;pagination&quot;: {'{'}</div>
                <div className="text-green-400 ml-4">&quot;page&quot;: 1,</div>
                <div className="text-green-400 ml-4">&quot;limit&quot;: 20,</div>
                <div className="text-green-400 ml-4">&quot;total&quot;: 50,</div>
                <div className="text-green-400 ml-4">&quot;pages&quot;: 3</div>
                <div className="text-blue-400 ml-2">{'}'}</div>
                <div className="text-yellow-300">{'}'}</div>
              </div>
            </div>
          </div>

          {/* Error Handling */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-4">Error Handling</h3>
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <p className="text-gray-300 mb-4">The API uses standard HTTP status codes:</p>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <span className="bg-green-900/50 text-green-400 px-2 py-1 rounded text-sm font-semibold">200</span>
                  <span className="text-gray-300">Success</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="bg-yellow-900/50 text-yellow-400 px-2 py-1 rounded text-sm font-semibold">400</span>
                  <span className="text-gray-300">Bad Request - Invalid parameters</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="bg-red-900/50 text-red-400 px-2 py-1 rounded text-sm font-semibold">401</span>
                  <span className="text-gray-300">Unauthorized - Invalid API key</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="bg-red-900/50 text-red-400 px-2 py-1 rounded text-sm font-semibold">404</span>
                  <span className="text-gray-300">Not Found - Resource doesn't exist</span>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="bg-red-900/50 text-red-400 px-2 py-1 rounded text-sm font-semibold">500</span>
                  <span className="text-gray-300">Internal Server Error</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}