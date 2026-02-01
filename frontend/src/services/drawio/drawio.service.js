import { config } from '@config'
import { DRAWIO_EVENTS, DRAWIO_ACTIONS } from '@config/constants.js'
import { createMessage, parseMessage, isDrawioEvent, getEventType } from './messages.js'
import { logger } from '@/utils/logger.js'

/**
 * Draw.io Service
 * Manages communication with embedded draw.io iframe
 */
export class DrawioService {
  constructor() {
    this.iframe = null
    this.isReady = false
    this.eventHandlers = new Map()
    this.messageHandler = this.handleMessage.bind(this)
    this.initTimeout = null
  }

  /**
   * Initialize service with iframe element
   * @param {HTMLIFrameElement} iframeElement
   * @returns {Promise<void>} Resolves when draw.io is ready
   */
  init(iframeElement) {
    if (!iframeElement) {
      throw new Error('Iframe element is required')
    }

    this.iframe = iframeElement
    window.addEventListener('message', this.messageHandler)

    return new Promise((resolve, reject) => {
      // Listen for init event
      this.once(DRAWIO_EVENTS.INIT, () => {
        this.isReady = true
        clearTimeout(this.initTimeout)
        logger.info('Draw.io initialized successfully')
        this.configure()
        resolve()
      })

      // Timeout fallback
      this.initTimeout = setTimeout(() => {
        if (!this.isReady) {
          logger.warn('Draw.io init timeout - forcing ready state')
          this.isReady = true
          resolve()
        }
      }, config.drawio.initTimeout)
    })
  }

  /**
   * Handle incoming messages from draw.io iframe
   * @private
   */
  handleMessage(event) {
    if (event.source !== this.iframe?.contentWindow) return

    const message = parseMessage(event.data)
    if (!message || !isDrawioEvent(message)) return

    const eventType = getEventType(message)
    logger.debug(`Draw.io event: ${eventType}`, message)

    // Trigger registered handlers
    const handlers = this.eventHandlers.get(eventType) || []
    handlers.forEach((handler) => handler(message))
  }

  /**
   * Send message to draw.io iframe
   * @private
   */
  sendMessage(action, data = {}) {
    if (!this.iframe) {
      logger.error('Cannot send message: iframe not initialized')
      return
    }

    const message = createMessage(action, data)
    this.iframe.contentWindow.postMessage(message, '*')
    logger.debug(`Sent message to draw.io: ${action}`, data)
  }

  /**
   * Configure draw.io after initialization
   * @private
   */
  configure() {
    logger.info('Draw.io configured and ready for diagram loading')
    // No default diagram - will be loaded from API
  }

  /**
   * Load diagram XML into draw.io
   * @param {string} xml - Diagram XML content
   */
  loadDiagram(xml) {
    if (!this.isReady) {
      throw new Error('Draw.io is not ready')
    }

    logger.info('Loading diagram into draw.io')
    this.sendMessage(DRAWIO_ACTIONS.LOAD, { xml })
  }

  /**
   * Request diagram export
   * @param {string} format - Export format (xml, svg, png)
   * @returns {Promise<string>} Exported content
   */
  exportDiagram(format = 'xml') {
    if (!this.isReady) {
      throw new Error('Draw.io is not ready')
    }

    return new Promise((resolve) => {
      this.once(DRAWIO_EVENTS.EXPORT, (message) => {
        resolve(message.data)
      })
      this.sendMessage(DRAWIO_ACTIONS.EXPORT, { format })
    })
  }

  /**
   * Register event handler
   * @param {string} eventType - Event type to listen for
   * @param {Function} handler - Handler function
   */
  on(eventType, handler) {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, [])
    }
    this.eventHandlers.get(eventType).push(handler)
  }

  /**
   * Register one-time event handler
   * @param {string} eventType - Event type to listen for
   * @param {Function} handler - Handler function
   */
  once(eventType, handler) {
    const wrappedHandler = (message) => {
      handler(message)
      this.off(eventType, wrappedHandler)
    }
    this.on(eventType, wrappedHandler)
  }

  /**
   * Unregister event handler
   * @param {string} eventType - Event type
   * @param {Function} handler - Handler to remove
   */
  off(eventType, handler) {
    const handlers = this.eventHandlers.get(eventType) || []
    const index = handlers.indexOf(handler)
    if (index > -1) {
      handlers.splice(index, 1)
    }
  }

  /**
   * Cleanup and destroy service
   */
  destroy() {
    window.removeEventListener('message', this.messageHandler)
    clearTimeout(this.initTimeout)
    this.eventHandlers.clear()
    this.iframe = null
    this.isReady = false
    logger.info('Draw.io service destroyed')
  }
}
