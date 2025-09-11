/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure for Replit proxy environment
  trailingSlash: false,
  // Essential for Replit: Allow all hosts for proxy environment
  experimental: {
    allowedHosts: true,
  },
  async rewrites() {
    const backendHost = 'http://localhost:8000';
    
    return [
      {
        source: '/api/auth/:path*',
        destination: `${backendHost}/auth/:path*`,
      },
      {
        source: '/api/:path*',
        destination: `${backendHost}/api/:path*`,
      },
    ]
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig