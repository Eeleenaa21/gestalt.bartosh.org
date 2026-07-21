import os
import requests
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET", "")

# Разрешённые origin (откуда могут приходить запросы от Decap CMS)
ALLOWED_ORIGINS = [
    "https://eeleenaa21.github.io",
    "http://127.0.0.1:1313",
    "http://localhost:1313",
]


@app.route("/api/auth", methods=["GET", "POST"])
def auth():
    """GitHub OAuth callback endpoint."""
    if request.method == "GET":
        # Decap CMS перенаправляет браузер на этот URL после GitHub OAuth
        # GET-запрос приходит от GitHub с code в query params
        code = request.args.get("code")
        if not code:
            return "Missing code parameter", 400

        # Обмениваем code на access_token
        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        if resp.status_code != 200:
            return f"Failed to get access token: {resp.text}", 500

        token_data = resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return f"No access_token in response: {token_data}", 500

        # Перенаправляем обратно в Decap CMS с токеном
        redirect_url = request.args.get("redirect") or "/admin/"
        return redirect(f"{redirect_url}?access_token={access_token}")

    elif request.method == "POST":
        # Decap CMS делает POST с code (альтернативный способ)
        data = request.json or {}
        code = data.get("code")
        if not code:
            return jsonify({"error": "Missing code"}), 400

        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        if resp.status_code != 200:
            return jsonify({"error": resp.text}), 500

        token_data = resp.json()
        return jsonify(token_data)


@app.route("/", methods=["GET"])
def health():
    """Health check."""
    return jsonify({"status": "ok", "client_id_configured": bool(CLIENT_ID)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)