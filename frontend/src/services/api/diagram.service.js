import { apiClient } from './client.js'
import { config } from '@config'
import { logger } from '@/utils/logger.js'

/**
 * Diagram API Service
 * Handles all diagram-related API calls
 */
export class DiagramService {
  /**
   * Fetch diagram XML by variant
   * @param {string} variant - Diagram variant (simple, complex, empty)
   * @returns {Promise<string>} XML content
   */
  async getDiagram(variant = config.defaults.diagramVariant) {
    logger.info(`Fetching diagram: ${variant}`)

    const endpoint = `${config.api.endpoints.diagram}?variant=${variant}`

    try {
      const response = await apiClient.get(endpoint)
      const xml = await response.text()

      logger.debug(`Received diagram XML (${xml.length} bytes)`)
      return xml
    } catch (error) {
      logger.error(`Failed to fetch diagram: ${error.message}`, error)
      throw error
    }
  }

  /**
   * Health check
   * @returns {Promise<boolean>}
   */
  async healthCheck() {
    try {
      const response = await apiClient.get(config.api.endpoints.health)
      const data = await response.json()
      return data.status === 'ok'
    } catch (error) {
      logger.error(`Health check failed: ${error.message}`)
      return false
    }
  }
}

// Export singleton instance
export const diagramService = new DiagramService()
