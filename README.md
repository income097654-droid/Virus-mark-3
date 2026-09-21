# Virus Mark 3 Backend

Deploy-ready starter backend for Virus Mark 3.

## Endpoints

- `GET /` — backend info
- `GET /health` — health check
- `GET /api/status` — Mark 3 status
- `POST /api/command` — send a command
- `POST /api/chat` — send a chat message

### Example request

POST `/api/command`

```json
{
  "command": "hello virus",
  "session_id": "demo-1"
}
```

Response:

```json
{
  "ok": true,
  "type": "command",
  "reply": "হ্যালো Sahadat! আমি Virus Mark 3. কী করতে পারি?",
  "session_id": "demo-1"
}
```

## Local test

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Deployment

This package includes `Procfile` and `render.yaml` for a simple Render deployment.

After deployment, the frontend should call:

`https://YOUR-BACKEND-DOMAIN/api/command`

or

`https://YOUR-BACKEND-DOMAIN/api/chat`

Set `VIRUS_API_KEY` in the hosting provider if you want API-key protection, then send the same key in the `X-API-Key` header.

## Important

This is the Mark 3 backend foundation. Home Assistant, persistent memory, real AI model integration, reminders, authentication/database, and device controls can be added as separate modules without changing the basic API structure.
