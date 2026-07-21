import os
import requests
from flask import Flask, request, redirect, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET", "")

# Шаблон HTML, который передаёт токен обратно в админку Decap CMS и закрывает всплывающее окно
POST_MESSAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Authorizing...</title>
</head>
<body>
  <p>Авторизация успешна. Закрываем окно...</p>
  <script>
    (function() {
      function recieveMessage(e) {
        window.opener.postMessage(
          'authorization:github:success:{{ token_data | tojson }}',
          e.origin
        );
      }
      window.addEventListener("message", recieveMessage, false);
      window.opener.postMessage("authorizing:github", "*");
    })();
  </script>
</body>
</html>
"""

@app.route("/api/auth", methods=["GET"])
def auth():
    """1. Старт авторизации: отправляем пользователя на GitHub."""
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&scope=repo,user"
    )
    return redirect(github_auth_url)


@app.route("/api/auth/callback", methods=["GET"])
def callback():
    """2. Callback: GitHub возвращает пользователя сюда с параметром code."""
    code = request.args.get("code")
    if not code:
        return "Missing code parameter from GitHub", 400

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

    # Возвращаем HTML, который передаст токен в Decap CMS через postMessage
    payload = {
        "token": access_token,
        "provider": "github"
    }
    return render_template_string(POST_MESSAGE_TEMPLATE, token_data=payload)


@app.route("/", methods=["GET"])
def health():
    """Health check."""
    return jsonify({"status": "ok", "client_id_configured": bool(CLIENT_ID)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)