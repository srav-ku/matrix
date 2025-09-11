'use client'

import { useState } from 'react'
import { 
  User,
  Check,
  Star,
  Zap,
  Shield,
  Globe,
  Clock
} from 'lucide-react'
import Sidebar from '../../components/Sidebar'
import ProfileDropdown from '../../components/ProfileDropdown'
import { useNotifications, NotificationManager } from '../../components/Notification'

export default function Pricing() {
  const [currentPlan, setCurrentPlan] = useState('free')
  const { notifications, addNotification, removeNotification } = useNotifications()

  const upgradeToPremium = () => {
    addNotification({
      type: 'info',
      title: 'Upgrade Coming Soon',
      message: 'Premium plan upgrade functionality will be available soon. Contact support for early access.'
    })
  }

  const downgradeToFree = () => {
    addNotification({
      type: 'warning',
      title: 'Downgrade Plan',
      message: 'Are you sure you want to downgrade to the free plan? You will lose premium features.'
    })
  }

  const plans = [
    {
      id: 'free',
      name: 'Free Plan',
      price: '$0',
      period: '/month',
      description: 'Perfect for getting started with movie data',
      features: [
        '100 API requests per day',
        'Basic movie database access',
        'Standard support',
        'API key management',
        'Basic rate limiting'
      ],
      limitations: [
        'Limited to 100 requests/day',
        'No priority support',
        'Basic features only'
      ],
      buttonText: currentPlan === 'free' ? 'Current Plan' : 'Downgrade',
      buttonAction: currentPlan === 'free' ? null : downgradeToFree,
      popular: false
    },
    {
      id: 'premium',
      name: 'Premium Plan',
      price: '$29',
      period: '/month',
      description: 'For developers who need more power and flexibility',
      features: [
        '1,000 API requests per day',
        'Complete movie database access',
        'Priority support',
        'Advanced API key management',
        'Custom rate limiting',
        'Usage analytics',
        'Webhook support',
        'Beta feature access',
        'Priority customer support'
      ],
      limitations: [],
      buttonText: currentPlan === 'premium' ? 'Current Plan' : 'Upgrade Now',
      buttonAction: currentPlan === 'premium' ? null : upgradeToPremium,
      popular: true
    }
  ]

  return (
    <div className="flex h-screen bg-black text-white">
      <NotificationManager 
        notifications={notifications} 
        onClose={removeNotification} 
      />
      
      {/* Sidebar */}
      <Sidebar currentPage="pricing" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-black border-b border-gray-800 px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Pricing Plans</h1>
            <p className="text-gray-400 text-sm">Choose the perfect plan for your movie data needs</p>
          </div>
          <div className="flex items-center space-x-4">
            <ProfileDropdown />
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          {/* Current Usage */}
          <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6 mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Current Usage</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-gray-800/50 border border-gray-600 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-300">API Requests Today</span>
                  <Clock className="w-5 h-5 text-blue-400" />
                </div>
                <div className="text-2xl font-bold text-white">47/100</div>
                <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '47%' }}></div>
                </div>
              </div>
              
              <div className="bg-gray-800/50 border border-gray-600 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-300">Current Plan</span>
                  <Star className="w-5 h-5 text-yellow-400" />
                </div>
                <div className="text-2xl font-bold text-white capitalize">{currentPlan}</div>
                <div className="text-gray-400 text-sm mt-1">
                  {currentPlan === 'free' ? '100 requests/day' : '1,000 requests/day'}
                </div>
              </div>
              
              <div className="bg-gray-800/50 border border-gray-600 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-300">Status</span>
                  <Shield className="w-5 h-5 text-green-400" />
                </div>
                <div className="text-2xl font-bold text-green-400">Active</div>
                <div className="text-gray-400 text-sm mt-1">All systems operational</div>
              </div>
            </div>
          </div>

          {/* Pricing Plans */}
          <div className="grid md:grid-cols-2 gap-8">
            {plans.map((plan) => (
              <div
                key={plan.id}
                className={`relative bg-gray-900/50 border rounded-xl p-8 ${
                  plan.popular 
                    ? 'border-green-500 ring-2 ring-green-500/20' 
                    : 'border-gray-700'
                } ${
                  currentPlan === plan.id ? 'bg-green-900/10' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <span className="bg-green-500 text-black px-3 py-1 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}
                
                {currentPlan === plan.id && (
                  <div className="absolute -top-3 right-4">
                    <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                      Current Plan
                    </span>
                  </div>
                )}

                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <p className="text-gray-400 text-sm mb-4">{plan.description}</p>
                  <div className="flex items-baseline justify-center">
                    <span className="text-4xl font-bold text-white">{plan.price}</span>
                    <span className="text-gray-400 ml-1">{plan.period}</span>
                  </div>
                </div>

                <div className="space-y-4 mb-6">
                  <h4 className="text-white font-semibold">Features included:</h4>
                  <ul className="space-y-2">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center text-gray-300">
                        <Check className="w-4 h-4 text-green-400 mr-3 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  {plan.limitations.length > 0 && (
                    <div className="mt-4">
                      <h4 className="text-white font-semibold mb-2">Limitations:</h4>
                      <ul className="space-y-1">
                        {plan.limitations.map((limitation, index) => (
                          <li key={index} className="text-gray-400 text-sm">
                            • {limitation}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <button
                  onClick={plan.buttonAction || undefined}
                  disabled={!plan.buttonAction}
                  className={`w-full py-3 rounded-lg font-semibold transition-all ${
                    currentPlan === plan.id
                      ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                      : plan.popular
                      ? 'bg-green-500 hover:bg-green-400 text-black'
                      : 'bg-gray-700 hover:bg-gray-600 text-white'
                  }`}
                >
                  {plan.buttonText}
                </button>
              </div>
            ))}
          </div>

          {/* FAQ Section */}
          <div className="mt-12 bg-gray-900/50 border border-gray-700 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Frequently Asked Questions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-white font-semibold mb-2">What happens when I reach my rate limit?</h3>
                <p className="text-gray-300">When you reach your daily request limit, you'll receive a notification and your API calls will return a rate limit error. Your limit resets at midnight UTC.</p>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-2">Can I upgrade or downgrade at any time?</h3>
                <p className="text-gray-300">Yes! You can change your plan at any time. Upgrades take effect immediately, while downgrades take effect at the start of your next billing cycle.</p>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-2">Do unused requests roll over?</h3>
                <p className="text-gray-300">No, unused API requests do not roll over to the next day. Each day you get a fresh allocation based on your current plan.</p>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-2">Is there a free trial for Premium?</h3>
                <p className="text-gray-300">We offer a generous free plan to get you started. Contact our support team if you need to evaluate Premium features before upgrading.</p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}