<template>
  <div class="diagram-editor-container">
    <DiagramToolbar
      :is-ready="isDrawioReady"
      @create-child="handleCreateChild"
      @load-diagram="handleLoadDiagram"
    />
    <DrawioFrame
      :drawio-service="drawioService"
      @ready="handleDrawioReady"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DiagramToolbar from './diagrams/DiagramToolbar.vue'
import DrawioFrame from './diagrams/DrawioFrame.vue'
import { useDiagram } from '@/composables/useDiagram.js'
import { DrawioService } from '@services/drawio/drawio.service.js'
import { DRAWIO_EVENTS } from '@config/constants.js'
import { logger } from '@/utils/logger.js'

const drawioService = new DrawioService()
const isDrawioReady = ref(false)
const { loadDiagram, isLoading, error } = useDiagram(drawioService)

const handleDrawioReady = async () => {
  isDrawioReady.value = true
  logger.info('DiagramEditor: Draw.io ready')

  // Setup event listeners
  setupDrawioListeners()

  // Auto-load default diagram from API
  try {
    await loadDiagram()
    logger.info('Default diagram auto-loaded successfully')
  } catch (err) {
    logger.error('Failed to auto-load diagram:', err)
  }
}

const setupDrawioListeners = () => {
  drawioService.on(DRAWIO_EVENTS.LOAD, () => {
    logger.info('Diagram loaded')
  })

  drawioService.on(DRAWIO_EVENTS.SAVE, async () => {
    logger.info('Diagram saved - requesting XML export')
    const xml = await drawioService.exportDiagram('xml')
    logger.info('Exported XML:', xml)
  })
}

const handleCreateChild = () => {
  if (!isDrawioReady.value) {
    alert('draw.io is not ready yet')
    return
  }
  alert('Create Child Diagram clicked! Integration works!')
  logger.info('Create Child Diagram functionality will be implemented in next sprint')
}

const handleLoadDiagram = async () => {
  if (!isDrawioReady.value) {
    alert('draw.io is not ready yet')
    return
  }

  try {
    await loadDiagram()
  } catch (err) {
    alert(`Loading error: ${err.message}`)
  }
}
</script>

<style scoped>
.diagram-editor-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}
</style>
