'use client'

import { useState } from 'react'
import { 
  User,
  ChevronDown,
  LogOut
} from 'lucide-react'

export default function ProfileDropdown() {
  const [showProfileDropdown, setShowProfileDropdown] = useState(false)

  const handleLogout = () => {
    localStorage.clear()
    window.location.href = '/'
  }

  return (
    <div className="relative">
      <button
        onClick={() => setShowProfileDropdown(!showProfileDropdown)}
        className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-800 transition-colors"
      >
        <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
          <User className="w-5 h-5 text-black" />
        </div>
        <ChevronDown className="w-4 h-4 text-gray-400" />
      </button>
      
      {/* Profile Dropdown */}
      {showProfileDropdown && (
        <div className="absolute right-0 mt-2 w-48 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50">
          <div className="p-3 border-b border-gray-700">
            <p className="text-white font-medium">Developer</p>
            <p className="text-gray-400 text-sm">developer@example.com</p>
          </div>
          <div className="py-2">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-3" />
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  )
}