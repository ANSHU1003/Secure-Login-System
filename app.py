from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")
conn.commit()

@app.route("/")
def home():
    if "user" in session:
        return f"Welcome {session['user']} <br><a href='/logout'>Logout</a>"
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )
        conn.commit()

        return redirect("/login")

    return '''
    <h2>Register</h2>
    <form method="post">
    Username:<input name="username"><br>
    Password:<input type="password" name="password"><br>
    <button>Register</button>
    </form>
    '''

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect("/")

    return '''
    <h2>Login</h2>
    <form method="post">
    Username:<input name="username"><br>
    Password:<input type="password" name="password"><br>
    <button>Login</button>
    </form>
    '''

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
