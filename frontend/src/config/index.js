/**
 * Application configuration
 * Reads from environment variables set by Vite
 */

const requiredEnvVars = [
  'VITE_API_BASE_URL',
  'VITE_DRAWIO_EMBED_URL',
]

// Validate required environment variables
requiredEnvVars.forEach((varName) => {
  if (!import.meta.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`)
  }
})

export const config = {
  api: {
    baseUrl: import.meta.env.VITE_API_BASE_URL,
    endpoints: {
      diagram: '/api/v1/diagram',
      health: '/health',
    },
  },
  drawio: {
    embedUrl: import.meta.env.VITE_DRAWIO_EMBED_URL,
    initTimeout: Number(import.meta.env.VITE_DRAWIO_INIT_TIMEOUT) || 3000,
  },
  defaults: {
    diagramVariant: import.meta.env.VITE_DEFAULT_DIAGRAM_VARIANT || 'simple',
  },
  logging: {
    level: import.meta.env.VITE_LOG_LEVEL || 'info',
  },
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
}

// Freeze config to prevent runtime modifications
Object.freeze(config)
