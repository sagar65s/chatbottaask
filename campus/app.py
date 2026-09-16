import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai
from config import *

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-in-production")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
client = genai.Client(api_key=api_key) if api_key else None

def build_prompt(message):
    history = session.get("history", [])[-12:]
    lines = [SYSTEM_PROMPT, "", "Recent conversation:"]
    for item in history:
        lines.append(f"{item['role']}: {item['text']}")
    lines += ["", f"user: {message}", "", "assistant:"]
    return "\n".join(lines)

@app.route("/")
def index():
    return render_template("index.html", config={
        "title": CHATBOT_TITLE, "domain": DOMAIN, "welcome": WELCOME_MESSAGE,
        "theme": UI_THEME, "primary": PRIMARY_COLOR, "accent": ACCENT_COLOR
    })

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please enter a message."}), 400
    if not client:
        return jsonify({"error": "GEMINI_API_KEY is not configured. Add it to .env."}), 500

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=build_prompt(message),
            config={"temperature": 0.4, "max_output_tokens": 800}
        )
        answer = response.text or "I could not generate a response."
        history = session.get("history", [])
        history.extend([{"role": "user", "text": message},
                        {"role": "assistant", "text": answer}])
        session["history"] = history[-20:]
        session.modified = True
        return jsonify({"answer": answer})
    except Exception as exc:
        return jsonify({"error": f"Gemini request failed: {exc}"}), 502

@app.post("/clear")
def clear():
    session.pop("history", None)
    session.modified = True
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
