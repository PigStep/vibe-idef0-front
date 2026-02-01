import { config } from '@config'

/**
 * Logging utility
 * Environment-aware logging with configurable levels
 */
const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
  none: 4,
}

class Logger {
  constructor() {
    this.level = LOG_LEVELS[config.logging.level] ?? LOG_LEVELS.info
  }

  debug(message, ...args) {
    if (this.level <= LOG_LEVELS.debug) {
      console.log(`[DEBUG] ${message}`, ...args)
    }
  }

  info(message, ...args) {
    if (this.level <= LOG_LEVELS.info) {
      console.info(`[INFO] ${message}`, ...args)
    }
  }

  warn(message, ...args) {
    if (this.level <= LOG_LEVELS.warn) {
      console.warn(`[WARN] ${message}`, ...args)
    }
  }

  error(message, ...args) {
    if (this.level <= LOG_LEVELS.error) {
      console.error(`[ERROR] ${message}`, ...args)
    }
  }
}

export const logger = new Logger()
