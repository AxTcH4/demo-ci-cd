from flask import Flask, request
import sqlite3

app = Flask(__name__)

# =====================================================
# FAILLE 1 — Secret hardcodé (détecté par SAST)
# =====================================================
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = "sk-prod-abc123secretkey9876"
SECRET_TOKEN = "ghp_realTokenHardcoded1234567890abcdef"

# =====================================================
# FAILLE 2 — Injection SQL (détecté par SAST)
# =====================================================
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # VULNERABLE: concaténation directe sans paramètre
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

@app.route("/user")
def user():
    username = request.args.get("username")
    results = get_user(username)
    return str(results)

# =====================================================
# FAILLE 3 — XSS (Cross-Site Scripting)
# =====================================================
@app.route("/hello")
def hello():
    name = request.args.get("name", "World")
    # VULNERABLE: retourne du HTML sans échappement
    return "<h1>Hello, " + name + "!</h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
