'use client'

import { useState } from 'react'
import { 
  Home, 
  Settings, 
  BookOpen, 
  ChevronRight,
  User,
  Search,
  MessageCircle,
  Mail,
  Phone,
  FileText,
  ExternalLink,
  Send,
  CheckCircle,
  AlertCircle,
  Clock,
  Star,
  HelpCircle,
  Zap,
  Shield,
  Globe
} from 'lucide-react'
import Link from 'next/link'

export default function Support() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [ticketForm, setTicketForm] = useState({
    category: '',
    subject: '',
    message: '',
    priority: 'medium'
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
      category: 'Support',
      items: [
        { icon: HelpCircle, label: 'Support', active: true, href: '/support' },
      ]
    },
    {
      category: 'Account',
      items: [
        { icon: Settings, label: 'Settings', href: '/settings' },
      ]
    }
  ]

  const faqData = [
    {
      category: 'authentication',
      question: 'How do I get an API key?',
      answer: 'You can create API keys from your dashboard. Go to the API Keys section and click "New API Key" to generate one instantly.'
    },
    {
      category: 'authentication',
      question: 'My API key is not working',
      answer: 'Ensure you\'re including the API key in the X-API-Key header. Check that the key is active in your dashboard and hasn\'t been deleted.'
    },
    {
      category: 'limits',
      question: 'What are the rate limits?',
      answer: 'The default rate limit is 100 requests per day. You can view your current usage and upgrade your plan for higher limits.'
    },
    {
      category: 'billing',
      question: 'How does billing work?',
      answer: 'Billing is based on your API usage and plan. You can see detailed usage statistics in your dashboard and upgrade or downgrade at any time.'
    },
    {
      category: 'technical',
      question: 'What movie data is available?',
      answer: 'Our database includes 50+ classic movies from 1936-2014 with complete metadata including title, year, director, cast, genres, ratings, and plot summaries.'
    },
    {
      category: 'technical',
      question: 'How do I search for movies?',
      answer: 'Use the /api/search endpoint with a query parameter. You can search by title, director, or plot content.'
    }
  ]

  const filteredFAQ = selectedCategory === 'all' 
    ? faqData 
    : faqData.filter(item => item.category === selectedCategory)

  const searchedFAQ = searchQuery
    ? filteredFAQ.filter(item => 
        item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.answer.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : filteredFAQ

  const submitTicket = () => {
    if (!ticketForm.category || !ticketForm.subject || !ticketForm.message) {
      alert('Please fill in all required fields')
      return
    }
    alert('Support ticket submitted successfully! We\'ll get back to you within 24 hours.')
    setTicketForm({ category: '', subject: '', message: '', priority: 'medium' })
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
            <h1 className="text-2xl font-bold text-white">Support Center</h1>
            <p className="text-gray-400 text-sm">Get help with The Matrix API platform</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-black" />
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          {/* Contact Options */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-blue-900/50 rounded-lg flex items-center justify-center">
                  <Mail className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Email Support</h3>
                  <p className="text-gray-400 text-sm">24-48 hour response</p>
                </div>
              </div>
              <p className="text-gray-300 text-sm mb-4">Send us a detailed message about your issue</p>
              <div className="text-green-400 text-sm font-medium">support@matrix.to</div>
            </div>

            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-green-900/50 rounded-lg flex items-center justify-center">
                  <MessageCircle className="w-5 h-5 text-green-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Live Chat</h3>
                  <p className="text-gray-400 text-sm">Mon-Fri 9AM-5PM EST</p>
                </div>
              </div>
              <p className="text-gray-300 text-sm mb-4">Real-time assistance from our team</p>
              <button className="text-green-400 text-sm font-medium hover:text-green-300 transition-colors">
                Start Chat →
              </button>
            </div>

            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-purple-900/50 rounded-lg flex items-center justify-center">
                  <Phone className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-white font-semibold">Priority Support</h3>
                  <p className="text-gray-400 text-sm">Enterprise customers</p>
                </div>
              </div>
              <p className="text-gray-300 text-sm mb-4">Dedicated support line for urgent issues</p>
              <div className="text-purple-400 text-sm font-medium">+1 (555) 123-4567</div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6 mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <button className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors text-left">
                <Shield className="w-5 h-5 text-green-400" />
                <div>
                  <div className="text-white font-medium text-sm">Reset API Key</div>
                  <div className="text-gray-400 text-xs">Generate new key</div>
                </div>
              </button>
              <button className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors text-left">
                <Zap className="w-5 h-5 text-yellow-400" />
                <div>
                  <div className="text-white font-medium text-sm">Usage Report</div>
                  <div className="text-gray-400 text-xs">View API usage</div>
                </div>
              </button>
              <button className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors text-left">
                <Globe className="w-5 h-5 text-blue-400" />
                <div>
                  <div className="text-white font-medium text-sm">Service Status</div>
                  <div className="text-gray-400 text-xs">Check uptime</div>
                </div>
              </button>
              <button className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg hover:bg-gray-700/50 transition-colors text-left">
                <FileText className="w-5 h-5 text-purple-400" />
                <div>
                  <div className="text-white font-medium text-sm">API Docs</div>
                  <div className="text-gray-400 text-xs">View documentation</div>
                </div>
              </button>
            </div>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* FAQ Section */}
            <div>
              <h2 className="text-2xl font-semibold text-white mb-6">Frequently Asked Questions</h2>
              
              {/* Search */}
              <div className="mb-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search FAQ..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Category Filter */}
              <div className="flex flex-wrap gap-2 mb-6">
                {['all', 'authentication', 'limits', 'billing', 'technical'].map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      selectedCategory === category
                        ? 'bg-green-500 text-black'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </button>
                ))}
              </div>

              {/* FAQ Items */}
              <div className="space-y-4">
                {searchedFAQ.map((item, index) => (
                  <div key={index} className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
                    <h4 className="text-white font-medium mb-2">{item.question}</h4>
                    <p className="text-gray-300 text-sm">{item.answer}</p>
                    <div className="mt-2">
                      <span className={`inline-block px-2 py-1 rounded text-xs ${
                        item.category === 'authentication' ? 'bg-blue-900/50 text-blue-400' :
                        item.category === 'limits' ? 'bg-orange-900/50 text-orange-400' :
                        item.category === 'billing' ? 'bg-green-900/50 text-green-400' :
                        'bg-purple-900/50 text-purple-400'
                      }`}>
                        {item.category}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Support Ticket Form */}
            <div>
              <h2 className="text-2xl font-semibold text-white mb-6">Submit Support Ticket</h2>
              
              <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Category *</label>
                    <select
                      value={ticketForm.category}
                      onChange={(e) => setTicketForm(prev => ({ ...prev, category: e.target.value }))}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="">Select a category</option>
                      <option value="technical">Technical Issue</option>
                      <option value="billing">Billing Question</option>
                      <option value="feature">Feature Request</option>
                      <option value="security">Security Concern</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Priority</label>
                    <select
                      value={ticketForm.priority}
                      onChange={(e) => setTicketForm(prev => ({ ...prev, priority: e.target.value }))}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Subject *</label>
                    <input
                      type="text"
                      value={ticketForm.subject}
                      onChange={(e) => setTicketForm(prev => ({ ...prev, subject: e.target.value }))}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Brief description of your issue"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Message *</label>
                    <textarea
                      rows={4}
                      value={ticketForm.message}
                      onChange={(e) => setTicketForm(prev => ({ ...prev, message: e.target.value }))}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
                      placeholder="Detailed description of your issue or question"
                    />
                  </div>

                  <button
                    onClick={submitTicket}
                    className="w-full bg-green-500 hover:bg-green-400 text-black px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center"
                  >
                    <Send className="w-4 h-4 mr-2" />
                    Submit Ticket
                  </button>
                </div>
              </div>

              {/* Response Time Info */}
              <div className="mt-6 bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                <h4 className="text-blue-400 font-medium mb-2 flex items-center">
                  <Clock className="w-4 h-4 mr-2" />
                  Expected Response Times
                </h4>
                <div className="space-y-1 text-sm text-gray-300">
                  <div className="flex justify-between">
                    <span>Urgent:</span>
                    <span>2-4 hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span>High:</span>
                    <span>4-8 hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Medium:</span>
                    <span>24 hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Low:</span>
                    <span>48-72 hours</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}