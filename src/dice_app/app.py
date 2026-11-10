import hmac
import ipaddress
import os
import random
import subprocess  # noqa: S404 - only called with a fixed argument list (see ping)

from flask import Flask, jsonify, request
from markupsafe import escape
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
# secrets come from the environment, never from the source code
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
PING = "/bin/ping"


@app.route("/rolldice")
def roll_dice():
    player = request.args.get("player", "anonymous")
    try:
        sides = int(request.args.get("sides", "6"))
    except ValueError:
        return {"error": "sides must be an integer"}, 400
    if sides < 2:
        return {"error": "a die needs at least 2 sides"}, 400
    # S311 is a false positive here: a dice game does not need a cryptographic RNG
    result = random.randint(1, sides)  # noqa: S311
    # explicit JSON response (Content-Type: application/json), never rendered as HTML
    return jsonify(player=player, sides=sides, result=result)


@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    # CodeQL py/reflective-xss: escape user input before it goes into HTML
    return f"<h1>Hello {escape(name)}!</h1>"


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    try:
        ip = ipaddress.ip_address(host)       # only a literal IP address is accepted
    except ValueError:
        return {"error": "host must be an IP address"}, 400
    # no shell, absolute path, validated argument -> reviewed, S603 accepted
    out = subprocess.run(  # noqa: S603
        [PING, "-c", "1", str(ip)], capture_output=True, text=True, timeout=5, check=False
    )
    return {"host": str(ip), "output": out.stdout}


@app.route("/admin")
def admin():
    supplied = request.args.get("password", "")
    if ADMIN_PASSWORD and hmac.compare_digest(supplied, ADMIN_PASSWORD):
        return {"status": "welcome admin"}
    return {"status": "denied"}, 403


@app.errorhandler(Exception)
def handle_error(exc):
    if isinstance(exc, HTTPException):
        return {"error": exc.name}, exc.code
    # never leak exception details to the client (OWASP A10:2025); log them instead
    app.logger.exception("unhandled error")
    return {"error": "internal server error"}, 500


def main():
    port = int(os.getenv("PORT", "8080"))
    debug = os.getenv("FLASK_DEBUG") == "1"
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=port, debug=debug)


if __name__ == "__main__":
    main()
