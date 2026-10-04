# Cognitive Metrics

Monorepo for Cognitive Metrics containing the backend API service and the frontend client.

## Repository Structure

```
cognitive-metrics/
├── backend/    # FastAPI backend service
└── frontend/   # Vue 3 + Vite frontend application
```

## Getting Started

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
