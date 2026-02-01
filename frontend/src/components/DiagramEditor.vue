<template>
  <div class="diagram-editor-container">
    <div class="toolbar">
      <button @click="handleCreateChild" :disabled="!isDrawioReady">
        Create Child Diagram
      </button>
      <button @click="loadDiagram" :disabled="!isDrawioReady">
        Загрузить тест
      </button>
    </div>
    <iframe
      ref="iframeRef"
      src="https://embed.diagrams.net/?embed=1&ui=atlas&spin=1&proto=json"
      allowFullScreen
      frameborder="0"
    ></iframe>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const iframeRef = ref(null)
const isDrawioReady = ref(false)

const handleMessage = (event) => {
  // Проверка источника сообщения
  if (event.source !== iframeRef.value?.contentWindow) return

  try {
    const message = JSON.parse(event.data)

    switch(message.event) {
      case 'init':
        isDrawioReady.value = true
        console.log('draw.io ready')
        configureDrawio()
        break
      case 'load':
        console.log('Diagram loaded')
        break
      case 'export':
        console.log('Diagram exported (XML):', message.data)
        break
      case 'save':
        console.log('Diagram saved - запрашиваем экспорт XML...')
        // Запрашиваем экспорт диаграммы в формате XML
        sendMessage('export', { format: 'xml' })
        break
      default:
        console.log('draw.io event:', message.event)
    }
  } catch (e) {
    // Игнорируем не-JSON сообщения
  }
}

const sendMessage = (action, data = {}) => {
  if (!iframeRef.value) return

  const message = JSON.stringify({ action, ...data })
  iframeRef.value.contentWindow.postMessage(message, '*')
}

const configureDrawio = () => {
  // Настройка draw.io после инициализации
  console.log('Configuring draw.io...')

  // Отправляем пустую диаграмму для инициализации
  const emptyDiagram = `<mxfile host="embed.diagrams.net">
  <diagram name="Page-1" id="1">
    <mxGraphModel dx="800" dy="450" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>`

  sendMessage('load', { xml: emptyDiagram })
}

const handleCreateChild = () => {
  if (!isDrawioReady.value) {
    alert('draw.io is not ready yet')
    return
  }

  // Показываем alert для проверки интеграции
  alert('Create Child Diagram clicked! Integration works!')
  console.log('Create Child Diagram functionality will be implemented in next sprint')
}

const loadDiagram = async () => {
  if (!isDrawioReady.value) {
    alert('draw.io is not ready yet')
    return
  }

  try {
    console.log('Загрузка тестовой диаграммы...')
    const response = await fetch('http://127.0.0.1:8000/api/v1/diagram')

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const xml = await response.text()
    console.log('Получен XML от бэкенда:', xml)

    // Отправляем XML в iframe
    sendMessage('load', { xml: xml })
    console.log('Диаграмма отправлена в iframe')
  } catch (error) {
    console.error('Ошибка при загрузке диаграммы:', error)
    alert(`Ошибка загрузки: ${error.message}`)
  }
}

onMounted(() => {
  window.addEventListener('message', handleMessage)

  // Добавляем таймаут на случай если событие init не придет
  setTimeout(() => {
    if (!isDrawioReady.value) {
      console.warn('draw.io init event timeout - forcing ready state')
      isDrawioReady.value = true
    }
  }, 3000)
})

onUnmounted(() => {
  window.removeEventListener('message', handleMessage)
})
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

.toolbar {
  display: flex;
  gap: 8px;
  padding: 8px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.toolbar button {
  padding: 6px 12px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.toolbar button:hover:not(:disabled) {
  background-color: #0052a3;
}

.toolbar button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

iframe {
  flex: 1;
  width: 100%;
  border: none;
  display: block;
}
</style>
