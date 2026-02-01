import { DRAWIO_EVENTS, DRAWIO_ACTIONS } from '@config/constants.js'

/**
 * Draw.io message creators
 */
export const createMessage = (action, data = {}) => {
  return JSON.stringify({ action, ...data })
}

export const parseMessage = (messageData) => {
  try {
    return JSON.parse(messageData)
  } catch (e) {
    return null
  }
}

/**
 * Message validators
 */
export const isDrawioEvent = (message) => {
  return message && typeof message.event === 'string'
}

export const getEventType = (message) => {
  return message?.event || null
}
