import { config } from '@config'

/**
 * HTTP Client wrapper
 * Provides configured fetch with base URL, headers, and error handling
 */
class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`

    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, { ...defaultOptions, ...options })

      if (!response.ok) {
        throw new ApiError(
          `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          url
        )
      }

      return response
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      // Network error or other fetch failure
      throw new ApiError(
        `Network error: ${error.message}`,
        0,
        url,
        error
      )
    }
  }

  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' })
  }

  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    })
  }
}

/**
 * Custom API Error class
 */
export class ApiError extends Error {
  constructor(message, status, url, originalError = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.url = url
    this.originalError = originalError
  }

  isNotFound() {
    return this.status === 404
  }

  isServerError() {
    return this.status >= 500
  }

  isNetworkError() {
    return this.status === 0
  }
}

// Export singleton instance
export const apiClient = new ApiClient(config.api.baseUrl)
