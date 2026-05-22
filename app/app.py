from flask import Flask, request, escape
import sqlite3
import os

app = Flask(__name__)

# =====================================================
# CORRIGÉ 1 — Secret lu depuis les variables d'env
# =====================================================
DATABASE_PASSWORD = os.environ.get(" DATABASE_PASSWORD")
API_KEY = os.environ.get("API_KEY")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN")

# =====================================================
# CORRIGÉ 2 — Requête paramétrée (plus d'injection SQL)
# =====================================================
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SÉCURISÉ: paramètre bindé, pas de concaténation
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (username,))
    return cursor.fetchall()

@app.route("/user")
def user():
    username = request.args.get("username")
    results = get_user(username)
    return str(results)

# =====================================================
# CORRIGÉ 3 — Échappement XSS
# =====================================================
@app.route("/hello")
def hello():
    name = request.args.get("name", "World")
    safe_name = escape(name)
    return str(safe_name), 200, {"Content-Type": "text/plain"}
if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
