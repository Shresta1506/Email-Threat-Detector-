from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = {
    "admin": {"password": "admin123"}
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users and users[u]["password"] == p:
            session["username"] = u
            return redirect(url_for("index"))
        flash("Invalid username or password", "error")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users:
            flash("Username already taken", "error")
        else:
            users[u] = {"password": p}
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        u = request.form["username"]
        if u in users:
            flash("Password reset link sent (mock)", "success")
        else:
            flash("Username not found", "error")
    return render_template("forgot.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html", username=session["username"])

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
    data = request.get_json()
    email = data.get("email", "").lower()
    words = ["urgent", "password", "click", "login", "verify"]
    found = [w for w in words if w in email]
    lvl = "None"
    if len(found) >= 3:
        lvl = "High"
    elif len(found) == 2:
        lvl = "Medium"
    elif len(found) == 1:
        lvl = "Low"
    pct = len(found) * 25
    return jsonify({
        "threat_level": lvl,
        "threat_percentage": pct,
        "suspicious_words": found,
        "message": "Analysis done"
    })


if __name__ == '__main__':
    app.run(debug=True)
