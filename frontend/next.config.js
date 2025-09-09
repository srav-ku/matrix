/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure for Replit proxy environment
  trailingSlash: false,
  async rewrites() {
    const backendHost = 'http://localhost:8000';
    
    return [
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