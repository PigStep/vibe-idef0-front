# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an IDEF0 diagram editor application with a FastAPI backend and Vue 3 frontend. The application integrates with draw.io (diagrams.net) for diagram editing and provides an API to serve diagram XML files.

## Repository Structure

The repository is organized as a monorepo with two separate applications:

- `backend/` - FastAPI server that serves diagram XML files
- `frontend/` - Vue 3 + Vite application with draw.io integration
- `tasks/` - Task-related files (not part of the main applications)

## Backend (FastAPI)

### Technology Stack
- Python 3.10+
- FastAPI for API framework
- Pydantic for data validation and settings management
- Uvicorn as ASGI server
- UV for dependency management

### Setup and Development

Navigate to the backend directory for all backend operations:
```bash
cd backend
```

**Install dependencies:**
```bash
uv sync
```

**Run the development server:**
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000` with auto-reload enabled.

**Access API documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Architecture

**Entry Point:** `main.py` contains the FastAPI application with CORS middleware configured for cross-origin requests (currently set to `allow_origins=["*"]` for development).

**Configuration:** Settings are managed through `config.py` using Pydantic Settings. The `get_settings()` function returns a singleton instance that reads from environment variables or `.env` file. Key setting:
- `DATA_DIR` - Directory containing diagram XML files (defaults to `data/`)

**API Schemas:** Defined in `schemas.py` using Pydantic models and Enums. The `DiagramVariantEnum` defines available diagram types (simple, complex, empty).

**API Endpoints:**
- `GET /health` - Health check endpoint
- `GET /api/v1/diagram?variant={variant}` - Retrieve diagram XML file by variant

**Data Storage:** Diagram XML files are stored in `backend/data/` directory. The API returns these files as FileResponse with `application/xml` media type.

**Logging:** Structured logging is configured with timestamp, name, level, filename, line number, and message format.

## Frontend (Vue 3)

### Technology Stack
- Vue 3 with `<script setup>` composition API
- Vite as build tool and dev server
- Embedded draw.io (diagrams.net) for diagram editing

### Setup and Development

Navigate to the frontend directory for all frontend operations:
```bash
cd frontend
```

**Install dependencies:**
```bash
npm install
```

**Run development server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
```

**Preview production build:**
```bash
npm run preview
```

### Architecture

**Application Entry:** `src/main.js` creates and mounts the Vue application to `#app` in `index.html`.

**Root Component:** `src/App.vue` is a simple wrapper that renders the `DiagramEditor` component.

**DiagramEditor Component:** `src/components/DiagramEditor.vue` is the main component that:
- Embeds draw.io via iframe (`https://embed.diagrams.net/?embed=1&ui=atlas&spin=1&proto=json`)
- Communicates with draw.io using postMessage API
- Manages diagram loading from the backend API
- Handles draw.io lifecycle events (init, load, save, export)

**Draw.io Integration:**
- Communication happens via `window.postMessage` and message event listeners
- The component listens for events: `init`, `load`, `export`, `save`
- Messages are sent using `sendMessage(action, data)` helper function
- The iframe is ready when the `init` event is received (with 3-second timeout fallback)

**API Integration:**
- Backend API is hardcoded to `http://127.0.0.1:8000/api/v1/diagram` in DiagramEditor.vue:103
- Fetches XML diagrams and loads them into draw.io
- When modifying API calls, ensure the backend CORS settings allow the frontend origin

## Git Workflow

The repository uses feature branches with pull requests:
- Main branch: `main`
- Current working branch: `claude-code-infra`
- Recent commits show integration work for frontend (Vue) and backend initialization

## Important Notes

**Backend Server URL:** The frontend component has a hardcoded backend URL `http://127.0.0.1:8000`. When working on API integration, ensure:
1. Backend is running on port 8000
2. CORS is properly configured in `backend/main.py`

**Draw.io Integration:** The DiagramEditor component uses the postMessage protocol to communicate with the embedded draw.io iframe. When debugging issues:
1. Check browser console for draw.io events
2. Verify the iframe source URL is accessible
3. Ensure message handlers are properly registered before sending messages

**Configuration Files:**
- Backend uses `.env` file for environment-specific settings (not tracked in git)
- Python version is pinned to 3.10 in `backend/.python-version`
- No test suite currently exists (no pytest configuration or test files)

**Diagram Variants:** The backend currently supports three diagram variants defined in `schemas.py`:
- `simple` - maps to `simple.xml`
- `complex` - maps to `complex.xml`
- `empty` - maps to `empty.xml`

When adding new diagram types, update both the `DiagramVariantEnum` in `schemas.py` and add corresponding XML files to `backend/data/`.
