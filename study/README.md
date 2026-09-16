# Study Buddy

A Flask + Gemini 3.1 Flash-Lite domain-specific chatbot.

## Files
- `app.py` — Flask server and Gemini request handling
- `config.py` — title, domain, system prompt, behavior, welcome message, UI colors, model and PORT
- `.env` — Gemini API key and Flask session secret
- `requirements.txt` — dependencies
- `templates/index.html` — responsive UI

## Local setup
1. Install Python 3.11+.
2. Create a virtual environment.
3. Run `pip install -r requirements.txt`.
4. Put your Gemini API key in `.env` as `GEMINI_API_KEY=...`.
5. Run `python app.py`.
6. Open `http://127.0.0.1:10000`.

## Render
Build command:
`pip install -r requirements.txt`

Start command:
`gunicorn app:app`

Set environment variable:
`GEMINI_API_KEY=your_key`

Render supplies `PORT` automatically; `config.py` reads it.

## Privacy / session behavior
Conversation history is stored only in Flask's signed browser session cookie for that browser session. It is not stored in a shared global list or database. Do not put sensitive information into the chatbot. For production use, set a strong `FLASK_SECRET_KEY` and HTTPS.

## Domain restriction
The system prompt instructs Gemini to answer only the configured domain. This is an application-level instruction, not a guaranteed security boundary; keep prompts and API access under your control.
