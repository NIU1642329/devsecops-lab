import os
import random
import subprocess
import json

from flask import Flask, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-123"      # demo value, not a real secret
ADMIN_PASSWORD = "changeme"                       # demo value, not a real secret


@app.route("/rolldice")
def roll_dice():
    player = request.args.get("player", "anonymous")
    sides = int(request.args.get("sides", "6"))
    assert sides > 1
    result = random.randint(1, sides)
    return {"player": player, "sides": sides, "result": result}


@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return f"<h1>Hello {name}!</h1>"


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return {"host": host, "output": out.stdout}


@app.route("/admin")
def admin():
    if request.args.get("password") == ADMIN_PASSWORD:
        return {"status": "welcome admin"}
    return {"status": "denied"}, 403


@app.errorhandler(Exception)
def handle_error(exc):
    try:
        status = exc.code
    except:
        status = 500
    return {"error": str(exc), "type": type(exc).__name__}, status


def main():
    port = os.getenv("PORT", "8080")
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
