# Frontend Architecture

## Overview

Vue 3 SPA application with draw.io integration for IDEF0 diagram editing. Clean architecture with separation of concerns: services, composables, and UI components.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── diagrams/
│   │   │   ├── DiagramToolbar.vue    # Toolbar UI component
│   │   │   └── DrawioFrame.vue       # Draw.io iframe wrapper
│   │   ├── DiagramEditor.vue         # Main orchestrator component (80 lines)
│   │   └── App.vue
│   │
│   ├── services/
│   │   ├── api/
│   │   │   ├── client.js             # HTTP client wrapper (fetch)
│   │   │   └── diagram.service.js    # Diagram API endpoints
│   │   └── drawio/
│   │       ├── drawio.service.js     # Draw.io iframe communication
│   │       └── messages.js           # Message type definitions
│   │
│   ├── composables/
│   │   └── useDiagram.js             # Diagram state & operations
│   │
│   ├── config/
│   │   ├── index.js                  # Configuration loader (reads .env)
│   │   └── constants.js              # Application constants
│   │
│   ├── utils/
│   │   └── logger.js                 # Environment-aware logging
│   │
│   └── main.js                       # Application entry point
│
├── .env.development                  # Dev environment config
├── .env.production                   # Prod environment config
├── .env.example                      # Template for team
├── vite.config.js                    # Vite config with path aliases
└── package.json
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     DiagramEditor.vue                        │
│                    (Orchestrator - 80 lines)                 │
│                                                              │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │ DiagramToolbar   │        │  DrawioFrame     │          │
│  │   (UI only)      │        │  (iframe wrap)   │          │
│  └──────────────────┘        └──────────────────┘          │
└────────┬─────────────────────────────┬───────────────────────┘
         │                             │
         │ uses                        │ uses
         ▼                             ▼
┌─────────────────────┐      ┌──────────────────────┐
│  useDiagram         │      │  DrawioService       │
│  (composable)       │◄─────│  (postMessage API)   │
│                     │      │                      │
│  • loadDiagram()    │      │  • init()            │
│  • exportDiagram()  │      │  • loadDiagram()     │
│  • isLoading        │      │  • exportDiagram()   │
│  • error            │      │  • on/once/off       │
└──────────┬──────────┘      └──────────────────────┘
           │
           │ uses
           ▼
┌──────────────────────┐      ┌──────────────────────┐
│  DiagramService      │◄─────│  ApiClient           │
│  (API endpoints)     │ uses │  (HTTP wrapper)      │
│                      │      │                      │
│  • getDiagram()      │      │  • request()         │
│  • healthCheck()     │      │  • get/post()        │
└──────────────────────┘      │  • error handling    │
                              └──────────────────────┘
           │
           │ calls
           ▼
┌──────────────────────────────────────────────────────┐
│              Backend API (FastAPI)                   │
│         http://127.0.0.1:8000/api/v1/diagram         │
└──────────────────────────────────────────────────────┘
```

## Data Flow

### Application Initialization

```
1. main.js creates Vue app
   └─> mounts App.vue
       └─> renders DiagramEditor.vue
           └─> creates DrawioService instance
           └─> renders DrawioFrame.vue
               └─> iframe loads draw.io
               └─> DrawioService.init() waits for 'init' event
                   └─> on 'init': auto-load diagram from API
                       └─> useDiagram.loadDiagram()
                           └─> DiagramService.getDiagram()
                               └─> ApiClient.get('/api/v1/diagram?variant=simple')
                                   └─> Backend returns XML
                           └─> DrawioService.loadDiagram(xml)
                               └─> postMessage to iframe
```

### User Loads Diagram (Button Click)

```
1. User clicks "Загрузить тест"
   └─> DiagramToolbar emits 'load-diagram'
       └─> DiagramEditor.handleLoadDiagram()
           └─> useDiagram.loadDiagram()
               └─> DiagramService.getDiagram('simple')
                   └─> ApiClient.get('/api/v1/diagram?variant=simple')
                       └─> Backend returns XML
               └─> DrawioService.loadDiagram(xml)
                   └─> postMessage({ action: 'load', xml: '...' })
                       └─> draw.io iframe receives & renders diagram
```

### User Saves Diagram

```
1. User clicks Save in draw.io (Ctrl+S)
   └─> draw.io sends postMessage({ event: 'save' })
       └─> DrawioService handles 'save' event
           └─> triggers registered handlers
               └─> DiagramEditor listener calls exportDiagram()
                   └─> DrawioService.exportDiagram('xml')
                       └─> postMessage({ action: 'export', format: 'xml' })
                           └─> draw.io sends postMessage({ event: 'export', data: 'xml...' })
                               └─> Promise resolves with XML
                                   └─> logger.info('Exported XML:', xml)
```

## Configuration System

### Environment Variables

Vite automatically loads `.env.[mode]` files:

| Command | Mode | File Loaded |
|---------|------|-------------|
| `npm run dev` | development | `.env.development` |
| `npm run build` | production | `.env.production` |

### Configuration Flow

```
.env.development
    │
    │ Vite reads at build time
    ▼
import.meta.env.VITE_*
    │
    │ config/index.js reads
    ▼
config object (frozen)
    │
    │ imported by services & components
    ▼
Used throughout app
```

### Example Usage

```javascript
// .env.development
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LOG_LEVEL=debug

// config/index.js reads and validates
export const config = {
  api: { baseUrl: import.meta.env.VITE_API_BASE_URL },
  logging: { level: import.meta.env.VITE_LOG_LEVEL }
}

// services/api/client.js uses
import { config } from '@config'
const url = `${config.api.baseUrl}/api/v1/diagram`
```

## Key Components

### 1. DiagramEditor.vue (Orchestrator)

**Responsibility**: Coordinate child components and services

- Renders `DiagramToolbar` and `DrawioFrame`
- Creates `DrawioService` instance
- Uses `useDiagram` composable for state
- Sets up event listeners
- Auto-loads diagram on init

**Size**: 80 lines (down from 182 lines)

### 2. DiagramToolbar.vue

**Responsibility**: UI for user actions

- Displays buttons
- Emits events: `create-child`, `load-diagram`
- No business logic

### 3. DrawioFrame.vue

**Responsibility**: Manage iframe lifecycle

- Renders iframe with draw.io embed URL
- Initializes DrawioService with iframe ref
- Emits `ready` event when initialized
- Destroys service on unmount

## Key Services

### DrawioService

**Responsibility**: Communication with draw.io iframe via postMessage

**API**:
```javascript
// Initialization
await drawioService.init(iframeElement)

// Load diagram
drawioService.loadDiagram(xmlString)

// Export diagram
const xml = await drawioService.exportDiagram('xml')

// Event listeners
drawioService.on('load', (message) => { })
drawioService.once('save', (message) => { })
drawioService.off('export', handler)
```

**Features**:
- Promise-based init with timeout fallback
- Event-driven architecture (on/once/off)
- Automatic cleanup on destroy
- Message validation and parsing

### DiagramService

**Responsibility**: Backend API communication

**API**:
```javascript
// Fetch diagram by variant
const xml = await diagramService.getDiagram('simple')

// Health check
const isHealthy = await diagramService.healthCheck()
```

**Features**:
- Uses ApiClient for HTTP calls
- Structured logging
- Error handling and rethrowing

### ApiClient

**Responsibility**: Generic HTTP client wrapper

**API**:
```javascript
// GET request
const response = await apiClient.get('/api/v1/diagram?variant=simple')
const xml = await response.text()

// POST request
const response = await apiClient.post('/api/v1/data', { key: 'value' })
```

**Features**:
- Base URL configuration
- Default headers
- Custom ApiError class with helper methods
- Network error handling

## Key Composables

### useDiagram

**Responsibility**: Diagram state and operations

**API**:
```javascript
const { loadDiagram, exportDiagram, currentVariant, isLoading, error } = useDiagram(drawioService)

// Load diagram
await loadDiagram('simple')

// Export diagram
const xml = await exportDiagram('xml')

// Reactive state
watch(isLoading, (loading) => { })
if (error.value) { }
```

**Features**:
- Reactive state (Vue refs)
- Coordinates DiagramService + DrawioService
- Error handling
- Loading states

## Path Aliases

Configured in `vite.config.js`:

```javascript
'@'           → './src'
'@config'     → './src/config'
'@services'   → './src/services'
'@components' → './src/components'
'@composables'→ './src/composables'
```

**Usage**:
```javascript
import { config } from '@config'
import { diagramService } from '@services/api/diagram.service.js'
import { useDiagram } from '@composables/useDiagram.js'
```

## Logging System

Environment-aware structured logging:

```javascript
import { logger } from '@/utils/logger.js'

logger.debug('Detailed info')  // Only in dev (LOG_LEVEL=debug)
logger.info('General info')    // dev + staging
logger.warn('Warning')         // all except production
logger.error('Error')          // always logged
```

**Log levels** (configured via `VITE_LOG_LEVEL`):
- `debug` - All logs
- `info` - Info, warn, error
- `warn` - Warn, error
- `error` - Only errors
- `none` - No logs

## Deployment

### Development

```bash
# Uses .env.development
npm run dev

# Backend: http://127.0.0.1:8000
# Logs: debug level
```

### Production Build

```bash
# Set production API URL
export VITE_API_BASE_URL=https://api.production.com

# Build (uses .env.production)
npm run build

# Deploy dist/ folder to hosting
```

### Docker Example

```dockerfile
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Inject environment at build time
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

## Error Handling

### API Errors

```javascript
try {
  const xml = await diagramService.getDiagram('simple')
} catch (error) {
  if (error instanceof ApiError) {
    if (error.isNotFound()) { }
    if (error.isServerError()) { }
    if (error.isNetworkError()) { }
  }
}
```

### Draw.io Errors

```javascript
try {
  await drawioService.init(iframe)
} catch (error) {
  logger.error('Draw.io init failed:', error)
}

// Timeout fallback automatically handles init delays
```

## Testing Strategy

### Manual Testing Checklist

- [ ] Dev server starts without errors
- [ ] Diagram auto-loads on initialization
- [ ] "Загрузить тест" button reloads diagram
- [ ] "Create Child Diagram" shows alert
- [ ] Console shows structured logs with levels
- [ ] Change `VITE_API_BASE_URL` → uses new URL
- [ ] Production build succeeds
- [ ] No hardcoded URLs in code

### Future: Unit Tests

```javascript
// Example: DiagramService test
describe('DiagramService', () => {
  it('should fetch diagram by variant', async () => {
    const xml = await diagramService.getDiagram('simple')
    expect(xml).toContain('<mxfile')
  })
})

// Example: DrawioService test (mocked)
describe('DrawioService', () => {
  it('should initialize and wait for ready event', async () => {
    const iframe = document.createElement('iframe')
    await drawioService.init(iframe)
    expect(drawioService.isReady).toBe(true)
  })
})
```

## Migration Notes

### Before (Old Architecture)

- **DiagramEditor.vue**: 182 lines, did everything
- Hardcoded backend URL: `http://127.0.0.1:8000`
- Hardcoded draw.io URL
- No environment configuration
- `console.log` everywhere
- Inline postMessage logic
- Not deployable to other environments

### After (New Architecture)

- **DiagramEditor.vue**: 80 lines, orchestration only
- Backend URL from `.env` files
- All URLs configurable
- Full environment system
- Structured logging with levels
- Services for separation of concerns
- Deployable to any environment

### Benefits

1. **Production-Ready**: Can deploy to staging/production with different configs
2. **Maintainable**: Each service has single responsibility
3. **Testable**: Services can be mocked and tested independently
4. **Scalable**: Easy to add new features (new services/composables)
5. **Clean**: 55% reduction in main component size
6. **Type-Safe**: JSDoc comments for IDE autocomplete

## Common Tasks

### Add New API Endpoint

1. Add to `config/index.js`:
   ```javascript
   endpoints: { newEndpoint: '/api/v1/new' }
   ```

2. Add method to `diagram.service.js`:
   ```javascript
   async getNewData() {
     const endpoint = `${config.api.endpoints.newEndpoint}`
     const response = await apiClient.get(endpoint)
     return response.json()
   }
   ```

### Add New Draw.io Event Handler

```javascript
// In DiagramEditor.vue
const setupDrawioListeners = () => {
  drawioService.on('newEvent', (message) => {
    logger.info('New event received:', message.data)
  })
}
```

### Add New Environment Variable

1. Add to `.env.development` and `.env.production`:
   ```bash
   VITE_NEW_FEATURE_FLAG=true
   ```

2. Add to `config/index.js`:
   ```javascript
   export const config = {
     features: {
       newFeature: import.meta.env.VITE_NEW_FEATURE_FLAG === 'true'
     }
   }
   ```

3. Use in code:
   ```javascript
   import { config } from '@config'
   if (config.features.newFeature) { }
   ```

## Troubleshooting

### Issue: "Missing required environment variable"

**Cause**: `.env` file missing or variable not prefixed with `VITE_`

**Fix**: Check `.env.development` exists and all vars start with `VITE_`

### Issue: "Draw.io init timeout"

**Cause**: Slow network or iframe blocked

**Fix**: Increase `VITE_DRAWIO_INIT_TIMEOUT` in `.env`

### Issue: "Network error" when loading diagram

**Cause**: Backend not running or wrong URL

**Fix**:
1. Check backend is running: `http://127.0.0.1:8000/health`
2. Verify `VITE_API_BASE_URL` in `.env.development`

### Issue: Changes to `.env` not reflecting

**Cause**: Vite caches env vars, needs restart

**Fix**: Stop dev server (Ctrl+C) and restart `npm run dev`

## Performance Considerations

- **Lazy Loading**: Could split services into async imports
- **Code Splitting**: Vite automatically splits chunks
- **Bundle Size**: No heavy dependencies (native fetch, Vue only)
- **Runtime**: Services are singletons (one instance)

## Security Considerations

- **VITE_ prefix**: Only vars with prefix exposed to browser
- **CORS**: Backend must allow frontend origin
- **postMessage**: Validates message source (iframe contentWindow)
- **No secrets**: Never put API keys in `.env` (they're in client bundle!)

## Next Steps (Future Enhancements)

- [ ] Add TypeScript for type safety
- [ ] Add unit tests (Vitest)
- [ ] Add E2E tests (Playwright)
- [ ] Add error boundaries
- [ ] Add toast notifications (replace alerts)
- [ ] Add loading spinners
- [ ] Add i18n for multilingual support
- [ ] Add Pinia if state complexity grows
- [ ] Add diagram save functionality to backend
- [ ] Implement "Create Child Diagram" feature
