/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    allowedOrigins: ['*'],
  },
  // Essential for Replit: Disable host header checks for proxy environments
  // Configure for Replit proxy environment
  trailingSlash: false,
  async rewrites() {
    const backendHost = process.env.REPLIT_DEV_DOMAIN 
      ? `https://${process.env.REPLIT_DEV_DOMAIN}:8000`
      : 'http://localhost:8000';
    
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