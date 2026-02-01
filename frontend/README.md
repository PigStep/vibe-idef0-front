# IDEF0 Diagram Editor - Frontend

Vue 3 SPA with draw.io integration for creating and editing IDEF0 diagrams.

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env.development

# Start development server
npm run dev
```

Application will be available at `http://localhost:5173`

## Prerequisites

- Node.js 20+
- Backend API running at `http://127.0.0.1:8000` (configurable)

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (uses `.env.development`) |
| `npm run build` | Build for production (uses `.env.production`) |
| `npm run preview` | Preview production build locally |

## Environment Configuration

Configuration is managed via `.env` files:

- **`.env.development`** - Development settings (local backend, debug logs)
- **`.env.production`** - Production settings (injected API URL, error-only logs)
- **`.env.example`** - Template for team (copy to get started)

### Key Environment Variables

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000              # Backend API URL
VITE_DRAWIO_EMBED_URL=https://embed.diagrams.net/... # Draw.io iframe URL
VITE_LOG_LEVEL=debug                                 # debug|info|warn|error
VITE_DEFAULT_DIAGRAM_VARIANT=simple                  # simple|complex|empty
```

All environment variables must be prefixed with `VITE_` to be accessible in the browser.

## Project Structure

```
src/
├── components/       # Vue components (UI)
├── services/         # Business logic & API calls
├── composables/      # Reusable composition functions
├── config/           # Configuration loader
└── utils/            # Utilities (logger, etc.)
```

## Features

- ✅ Draw.io integration via iframe
- ✅ Auto-load diagram from backend API
- ✅ Environment-based configuration
- ✅ Structured logging with levels
- ✅ Clean service layer architecture
- ✅ Path aliases for clean imports

## Architecture

This project follows clean architecture principles with separation of concerns:

- **Components** - UI presentation layer
- **Services** - Business logic and external communication
- **Composables** - Reusable reactive state and operations
- **Config** - Environment configuration management

For detailed architecture documentation, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

## Development Workflow

1. **Start Backend**
   ```bash
   cd ../backend
   uv run uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend**
   ```bash
   npm run dev
   ```

3. **Open Browser**
   Navigate to `http://localhost:5173`

4. **Diagram loads automatically** from backend API

## Path Aliases

Clean imports using configured aliases:

```javascript
import { config } from '@config'                    // src/config
import { diagramService } from '@services/api/...'  // src/services
import { useDiagram } from '@composables/...'       // src/composables
import MyComponent from '@components/...'           // src/components
```

## Deployment

### Build for Production

```bash
# Set production API URL
export VITE_API_BASE_URL=https://api.production.com

# Build
npm run build

# Output in dist/ folder
```

### Docker Deployment

```dockerfile
# Build stage
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Inject API URL at build time
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```bash
docker build --build-arg VITE_API_BASE_URL=https://api.production.com -t idef0-frontend .
docker run -p 80:80 idef0-frontend
```

## Troubleshooting

### Backend Connection Failed

**Problem**: "Network error" when loading diagram

**Solution**:
1. Verify backend is running: `curl http://127.0.0.1:8000/health`
2. Check `VITE_API_BASE_URL` in `.env.development`
3. Verify CORS is configured in backend `main.py`

### Draw.io Not Loading

**Problem**: "Draw.io init timeout" message

**Solution**:
1. Check internet connection (draw.io loads from CDN)
2. Increase timeout: `VITE_DRAWIO_INIT_TIMEOUT=5000`
3. Restart dev server after `.env` changes

### Environment Changes Not Applied

**Problem**: Changes to `.env` file not reflecting

**Solution**: Vite caches env vars - restart dev server (Ctrl+C, then `npm run dev`)

### Import Path Errors

**Problem**: Module not found errors

**Solution**: Path aliases configured in `vite.config.js` - ensure imports use `@` prefix

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Draw.io (diagrams.net)** - Embedded diagram editor

## Browser Support

- Modern browsers with ES6+ support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Contributing

1. Create feature branch from `main`
2. Make changes following existing architecture patterns
3. Test manually (checklist in ARCHITECTURE.md)
4. Create PR with description

## Key Files

- **`src/main.js`** - Application entry point
- **`src/App.vue`** - Root component
- **`src/components/DiagramEditor.vue`** - Main editor orchestrator
- **`src/config/index.js`** - Configuration loader
- **`vite.config.js`** - Vite build configuration

## API Integration

Backend API endpoints used:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/diagram?variant={variant}` | GET | Fetch diagram XML |

## Logging

Structured logging with environment-aware levels:

```javascript
import { logger } from '@/utils/logger.js'

logger.debug('Detailed debugging info')  // Only in development
logger.info('General information')       // Dev + staging
logger.warn('Warning message')           // All non-prod
logger.error('Error occurred')           // Always logged
```

Log level controlled by `VITE_LOG_LEVEL` environment variable.

## License

(Add your license here)

## Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Draw.io Integration Guide](https://www.diagrams.net/doc/faq/embed-mode)
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Detailed architecture documentation
