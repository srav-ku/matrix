'use client'

import { useState, useEffect } from 'react'
import { 
  CheckCircle, 
  AlertCircle, 
  XCircle, 
  Info,
  X
} from 'lucide-react'

export interface NotificationProps {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

interface NotificationComponentProps extends NotificationProps {
  onClose: (id: string) => void
}

export function Notification({ id, type, title, message, duration = 5000, onClose }: NotificationComponentProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(id)
    }, duration)

    return () => clearTimeout(timer)
  }, [id, duration, onClose])

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-400" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-400" />
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-400" />
      case 'info':
        return <Info className="w-5 h-5 text-blue-400" />
    }
  }

  const getBorderColor = () => {
    switch (type) {
      case 'success':
        return 'border-green-500'
      case 'error':
        return 'border-red-500'
      case 'warning':
        return 'border-yellow-500'
      case 'info':
        return 'border-blue-500'
    }
  }

  const getBackgroundColor = () => {
    switch (type) {
      case 'success':
        return 'bg-green-900/20'
      case 'error':
        return 'bg-red-900/20'
      case 'warning':
        return 'bg-yellow-900/20'
      case 'info':
        return 'bg-blue-900/20'
    }
  }

  return (
    <div className={`${getBackgroundColor()} ${getBorderColor()} border rounded-lg p-4 shadow-lg backdrop-blur-sm animate-in slide-in-from-right-5 duration-300`}>
      <div className="flex items-start space-x-3">
        {getIcon()}
        <div className="flex-1">
          <h4 className="text-white font-semibold text-sm">{title}</h4>
          <p className="text-gray-300 text-sm mt-1">{message}</p>
        </div>
        <button
          onClick={() => onClose(id)}
          className="text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}

// Notification Manager Component
interface NotificationManagerProps {
  notifications: NotificationProps[]
  onClose: (id: string) => void
}

export function NotificationManager({ notifications, onClose }: NotificationManagerProps) {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-3 max-w-sm">
      {notifications.map((notification) => (
        <Notification
          key={notification.id}
          {...notification}
          onClose={onClose}
        />
      ))}
    </div>
  )
}

// Hook for managing notifications
export function useNotifications() {
  const [notifications, setNotifications] = useState<NotificationProps[]>([])

  const addNotification = (notification: Omit<NotificationProps, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 15)
    setNotifications(prev => [...prev, { ...notification, id }])
  }

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  return {
    notifications,
    addNotification,
    removeNotification
  }
}