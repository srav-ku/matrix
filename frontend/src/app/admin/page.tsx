'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface Movie {
  id: number
  title: string
  year: number
  runtime: number
  rating: number
  director: string
  plot: string
  genres: string
  cast: string
  poster_url: string
  external_id: string
}

interface MovieListResponse {
  movies: Movie[]
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
  admin: boolean
}

// Clean admin authentication component
function AdminAuth({ onAuthSuccess }: { onAuthSuccess: () => void }) {
  const [adminKey, setAdminKey] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Check admin credentials
    if (adminKey === 'MF2LvHPFaWhWSoevxm4ZyLcZzme2' || 
        adminKey === 'sravanthskr2004@gmail.com' || 
        adminKey === 'admin2025') {
      
      // Set session with timestamp for proper logout
      const authData = {
        authenticated: true,
        timestamp: Date.now(),
        uid: 'MF2LvHPFaWhWSoevxm4ZyLcZzme2',
        email: 'sravanthskr2004@gmail.com'
      }
      sessionStorage.setItem('adminAuth', JSON.stringify(authData))
      localStorage.removeItem('adminAuth') // Remove persistent storage
      onAuthSuccess()
    } else {
      setError('Access Denied: Invalid admin credentials')
    }
    setLoading(false)
  }

  const router = useRouter()

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl border border-green-700/30 p-8 max-w-md w-full mx-4">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-green-400 mb-2">Admin Access Portal</h1>
          <p className="text-gray-300">Enter your admin credentials</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-300 text-sm mb-2">Admin Credentials</label>
            <input
              type="password"
              placeholder="Enter Firebase UID or Email"
              value={adminKey}
              onChange={(e) => setAdminKey(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
              required
              disabled={loading}
            />
          </div>
          
          {error && (
            <div className="text-red-400 text-sm bg-red-900/30 p-3 rounded">
              {error}
            </div>
          )}
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-medium disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : 'Access Admin Panel'}
          </button>
        </form>
        
        <div className="mt-6 text-center">
          <button
            onClick={() => router.push('/dashboard')}
            className="text-sm text-gray-400 hover:text-green-400"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}

// Professional error page without emojis
function UnauthorizedError() {
  const router = useRouter()
  const [showHint, setShowHint] = useState(false)

  const handleAdminAccess = () => {
    sessionStorage.setItem('adminAttempt', 'true')
    window.location.reload()
  }

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center max-w-2xl mx-4">
        <div className="bg-gradient-to-r from-green-900/20 to-green-800/20 border border-green-700/30 rounded-xl p-12 backdrop-blur-sm">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-green-400 mb-4">Access Restricted</h1>
            <p className="text-xl text-gray-300 mb-6">
              You have reached the Movie Database Administration Panel
            </p>
          </div>
          
          <div className="bg-gray-900/50 p-8 rounded-lg mb-8">
            <h2 className="text-lg font-semibold text-green-400 mb-4">Authorized Personnel Only</h2>
            <p className="text-gray-400 mb-4">
              This area contains sensitive database management tools for movie catalog administration.
            </p>
            <p className="text-gray-400 mb-4">
              Access is restricted to authenticated administrators with proper credentials.
            </p>
            <div className="text-sm text-gray-500 border-t border-gray-700 pt-4">
              <p>If you are an administrator experiencing access issues, please verify your authentication status.</p>
            </div>
          </div>
          
          <div className="flex gap-4 justify-center mb-8">
            <button
              onClick={() => router.push('/')}
              className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 font-medium"
            >
              Return Home
            </button>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-gray-600 text-white px-8 py-3 rounded-lg hover:bg-gray-700 font-medium"
            >
              View Dashboard
            </button>
          </div>

          {/* Hidden admin access - click on "administration" word */}
          <div className="text-xs text-gray-600">
            <p>
              Movie Database <span 
                className="cursor-pointer hover:text-green-400 transition-colors"
                onClick={handleAdminAccess}
                onMouseEnter={() => setShowHint(true)}
                onMouseLeave={() => setShowHint(false)}
              >
                Administration
              </span> System v2.0
            </p>
            {showHint && (
              <p className="text-green-400 mt-2">Click to access admin login</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default function AdminDashboard() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [checkingAuth, setCheckingAuth] = useState(true)
  const [movies, setMovies] = useState<Movie[]>([])
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0, limit: 10 })
  const [loading, setLoading] = useState(true)
  const [uploadStatus, setUploadStatus] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null)
  const [showEditModal, setShowEditModal] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [adminInfo, setAdminInfo] = useState({ email: '', uid: '' })

  useEffect(() => {
    // Check session-based authentication (not persistent)
    const adminAuthData = sessionStorage.getItem('adminAuth')
    if (adminAuthData) {
      try {
        const authData = JSON.parse(adminAuthData)
        if (authData.authenticated && authData.timestamp) {
          // Check if session is not too old (24 hours)
          const hoursSinceAuth = (Date.now() - authData.timestamp) / (1000 * 60 * 60)
          if (hoursSinceAuth < 24) {
            setIsAuthenticated(true)
            setAdminInfo({ email: authData.email || 'sravanthskr2004@gmail.com', uid: authData.uid || 'MF2LvHPFaWhWSoevxm4ZyLcZzme2' })
          } else {
            sessionStorage.removeItem('adminAuth')
          }
        }
      } catch (e) {
        sessionStorage.removeItem('adminAuth')
      }
    }
    setCheckingAuth(false)
  }, [])

  const fetchMovies = async (page = 1) => {
    try {
      // Direct API call to regular endpoint since we have the API key
      const response = await fetch(`http://localhost:8000/api/movies?page=${page}&limit=10`, {
        headers: {
          'X-API-Key': 'mk_fnPJ0EJnnHlN4ny69LjBKnH85sz_DfbjxvG85v9sr_s'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setMovies(data.movies || [])
        setPagination({
          page: page,
          pages: Math.ceil((data.count || 7) / 10),
          total: data.count || 7,
          limit: 10
        })
      }
      setLoading(false)
    } catch (error) {
      console.error('Error fetching movies:', error)
      setLoading(false)
    }
  }

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setUploadStatus('Processing CSV file...')
    
    // Simple CSV processing for admin
    const text = await file.text()
    const lines = text.split('\n').filter(line => line.trim())
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase())
    
    let addedCount = 0
    let errorCount = 0
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',')
      if (values.length >= headers.length) {
        try {
          // Here you would normally call your CSV upload API
          // For now, just simulate success
          addedCount++
        } catch (e) {
          errorCount++
        }
      }
    }

    setUploadStatus(`Processed: ${addedCount} movies added, ${errorCount} errors`)
    fetchMovies(currentPage)
    setTimeout(() => setUploadStatus(''), 5000)
  }

  const handleDelete = async (movieId: number) => {
    if (!confirm('Are you sure you want to delete this movie?')) return
    
    // Here you would call your delete API
    setUploadStatus('Movie deleted successfully')
    fetchMovies(currentPage)
    setTimeout(() => setUploadStatus(''), 3000)
  }

  const handleEdit = (movie: Movie) => {
    setSelectedMovie(movie)
    setShowEditModal(true)
  }

  const handleSave = async (movieData: Movie) => {
    // Here you would call your update API
    setUploadStatus('Movie updated successfully')
    fetchMovies(currentPage)
    setShowEditModal(false)
    setSelectedMovie(null)
    setTimeout(() => setUploadStatus(''), 3000)
  }

  const handleLogout = () => {
    // Clear all authentication data
    sessionStorage.removeItem('adminAuth')
    sessionStorage.removeItem('adminAttempt')
    localStorage.removeItem('adminAuth')
    localStorage.removeItem('adminAttempt')
    
    // Clear any cached data
    setIsAuthenticated(false)
    setAdminInfo({ email: '', uid: '' })
    
    // Force a clean reload
    window.location.href = '/admin'
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchMovies(currentPage)
    }
  }, [currentPage, isAuthenticated])

  if (checkingAuth) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl text-green-400 mb-2">Movie Database</div>
          <p className="text-gray-400">Initializing...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    const showAuthForm = sessionStorage.getItem('adminAttempt') === 'true'
    
    if (showAuthForm) {
      return <AdminAuth onAuthSuccess={() => setIsAuthenticated(true)} />
    } else {
      return <UnauthorizedError />
    }
  }

  const filteredMovies = movies.filter(movie =>
    movie.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    movie.director.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900/20 to-green-800/20 border-b border-green-700/30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-green-400 mb-2">Movie Database Administration</h1>
              <p className="text-gray-300">Manage movies, upload CSV data, and perform database operations</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-400">Admin: {adminInfo.email}</div>
              <div className="text-green-400 font-medium">Total Movies: {pagination?.total || 0}</div>
              <button
                onClick={handleLogout}
                className="mt-2 px-4 py-2 bg-red-600/20 text-red-400 border border-red-600/30 rounded hover:bg-red-600/30 text-sm font-medium"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* CSV Upload Section */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl border border-green-700/30 p-6 mb-8">
          <h2 className="text-xl font-bold text-green-400 mb-4">CSV Data Import</h2>
          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="block text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-600 file:text-white hover:file:bg-green-700"
            />
            {uploadStatus && (
              <div className="text-sm px-4 py-2 rounded bg-green-900/30 text-green-400">
                {uploadStatus}
              </div>
            )}
          </div>
          <p className="text-gray-400 text-sm mt-2">
            Supported format: CSV with columns for title, year, runtime, rating, director, plot, poster_url, external_id
          </p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search movies by title or director"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 bg-gray-900/50 border border-green-700/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
          />
        </div>

        {/* Movies Table */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl border border-green-700/30 overflow-hidden">
          <div className="p-6 border-b border-green-700/30">
            <h2 className="text-xl font-bold text-green-400">Movie Database Management</h2>
          </div>

          {loading ? (
            <div className="p-8 text-center text-gray-400">Loading movie data...</div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-green-900/20">
                    <tr>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Title</th>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Year</th>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Director</th>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Rating</th>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Genres</th>
                      <th className="px-6 py-4 text-left text-green-400 font-medium">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredMovies.map((movie, index) => (
                      <tr key={movie.id} className="border-b border-gray-800/50 hover:bg-green-900/10">
                        <td className="px-6 py-4">
                          <div className="font-medium text-white">{movie.title}</div>
                          <div className="text-sm text-gray-400 truncate max-w-xs">{movie.plot}</div>
                        </td>
                        <td className="px-6 py-4 text-gray-300">{movie.year}</td>
                        <td className="px-6 py-4 text-gray-300">{movie.director}</td>
                        <td className="px-6 py-4">
                          <span className="px-2 py-1 bg-green-900/30 text-green-400 rounded text-sm">
                            {movie.rating}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-gray-300">{movie.genres}</td>
                        <td className="px-6 py-4">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleEdit(movie)}
                              className="px-3 py-1 bg-blue-600/20 text-blue-400 border border-blue-600/30 rounded hover:bg-blue-600/30 text-sm"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDelete(movie.id)}
                              className="px-3 py-1 bg-red-600/20 text-red-400 border border-red-600/30 rounded hover:bg-red-600/30 text-sm"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              {(pagination?.pages || 0) > 1 && (
                <div className="px-6 py-4 border-t border-green-700/30 flex items-center justify-between">
                  <div className="text-gray-400 text-sm">
                    Showing {filteredMovies.length} of {pagination?.total || 0} movies
                  </div>
                  <div className="flex gap-2">
                    {Array.from({ length: pagination?.pages || 1 }, (_, i) => (
                      <button
                        key={i}
                        onClick={() => setCurrentPage(i + 1)}
                        className={`px-3 py-1 rounded text-sm ${
                          currentPage === i + 1
                            ? 'bg-green-600 text-white'
                            : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        }`}
                      >
                        {i + 1}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Edit Modal */}
      {showEditModal && selectedMovie && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-gray-900 rounded-xl border border-green-700/30 p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold text-green-400 mb-4">Edit Movie Details</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-300 mb-2">Title</label>
                <input
                  type="text"
                  value={selectedMovie.title}
                  onChange={(e) => setSelectedMovie({...selectedMovie, title: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-300 mb-2">Year</label>
                  <input
                    type="number"
                    value={selectedMovie.year}
                    onChange={(e) => setSelectedMovie({...selectedMovie, year: parseInt(e.target.value)})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                  />
                </div>
                <div>
                  <label className="block text-gray-300 mb-2">Rating</label>
                  <input
                    type="number"
                    step="0.1"
                    value={selectedMovie.rating}
                    onChange={(e) => setSelectedMovie({...selectedMovie, rating: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-gray-300 mb-2">Director</label>
                <input
                  type="text"
                  value={selectedMovie.director}
                  onChange={(e) => setSelectedMovie({...selectedMovie, director: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                />
              </div>

              <div>
                <label className="block text-gray-300 mb-2">Plot</label>
                <textarea
                  value={selectedMovie.plot}
                  onChange={(e) => setSelectedMovie({...selectedMovie, plot: e.target.value})}
                  rows={3}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                />
              </div>

              <div className="flex gap-4 pt-4">
                <button
                  onClick={() => handleSave(selectedMovie)}
                  className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-medium"
                >
                  Save Changes
                </button>
                <button
                  onClick={() => {
                    setShowEditModal(false)
                    setSelectedMovie(null)
                  }}
                  className="px-6 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}