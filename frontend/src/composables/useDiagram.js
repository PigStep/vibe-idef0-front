import { ref } from 'vue'
import { diagramService } from '@services/api/diagram.service.js'
import { config } from '@config'
import { logger } from '@/utils/logger.js'

/**
 * Diagram composable
 * Manages diagram state and operations
 */
export function useDiagram(drawioService) {
  const currentVariant = ref(config.defaults.diagramVariant)
  const isLoading = ref(false)
  const error = ref(null)

  /**
   * Load diagram by variant
   */
  const loadDiagram = async (variant = currentVariant.value) => {
    isLoading.value = true
    error.value = null

    try {
      logger.info(`Loading diagram: ${variant}`)
      const xml = await diagramService.getDiagram(variant)

      drawioService.loadDiagram(xml)
      currentVariant.value = variant

      logger.info('Diagram loaded successfully')
    } catch (err) {
      logger.error('Failed to load diagram:', err)
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Export current diagram
   */
  const exportDiagram = async (format = 'xml') => {
    isLoading.value = true
    error.value = null

    try {
      const exported = await drawioService.exportDiagram(format)
      logger.info(`Diagram exported as ${format}`)
      return exported
    } catch (err) {
      logger.error('Failed to export diagram:', err)
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    currentVariant,
    isLoading,
    error,
    loadDiagram,
    exportDiagram,
  }
}
