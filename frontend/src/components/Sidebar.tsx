'use client'

import { useState } from 'react'
import { 
  Home, 
  Settings, 
  HelpCircle,
  ChevronRight,
  CreditCard
} from 'lucide-react'
import Link from 'next/link'

interface SidebarProps {
  currentPage: string
}

export default function Sidebar({ currentPage }: SidebarProps) {
  const sidebarItems = [
    { 
      category: 'API Management',
      items: [
        { icon: Home, label: 'Overview', href: '/dashboard', id: 'dashboard' },
      ]
    },
    {
      category: 'Support',
      items: [
        { icon: HelpCircle, label: 'Support', href: '/support', id: 'support' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', href: '/settings', id: 'settings' },
        { icon: CreditCard, label: 'Pricing Plans', href: '/pricing', id: 'pricing' },
      ]
    }
  ]

  return (
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
              {section.items.map((item) => {
                const isActive = currentPage === item.id
                return (
                  <Link
                    key={item.label}
                    href={item.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      isActive
                        ? 'bg-green-900/50 text-green-400 border border-green-800'
                        : 'text-gray-300 hover:text-white hover:bg-gray-800'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.label}
                    {isActive && <ChevronRight className="ml-auto h-4 w-4" />}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </nav>
    </div>
  )
}