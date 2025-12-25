from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helper import login_required
import webbrowser
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET", "POST"])
def index():
    return redirect("/login")

@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return render_template('index.html', message = "must enter username")

        # Ensure password was submitted
        elif not password:
            return render_template('index.html', message = "must enter password")

        # Query database for username
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        conn.commit()
        conn.close()

        try:
            # Ensure username exists and password is correct
            if row != None and check_password_hash(row[0][2], password):

                # Remember which user has logged in
                session["user_id"] = row[0][0]

                # Redirect user to home page
                return redirect("/play")
            else:
                return render_template('index.html', message = "wrong username or password")
        except IndexError:
            return render_template('index.html', message = "wrong username or password")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('index.html')



@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return render_template("register.html", message = "must enter username")

        # Ensure password was submitted
        elif not password:
            return render_template('register.html', message = "mus enter password")

        elif not confirmation:
            return render_template('register.html', message = "must enter confirmation")

        elif password != confirmation:
            return render_template('register.html', message = "passwords do not match")


        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, user_password) VALUES (?, ?)", (username, generate_password_hash(password)))
            conn.commit()
            conn.close()

        except ValueError:
            return render_template('index.html', message = "username exist")
        return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")

@app.route('/play', methods=["GET", "POST"])
@login_required
def play():
    if request.method == "POST":
        data = request.get_json()
        time = data['time']
        # Process the time data here
        output = abs(time - 5)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        row = c.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchall()
        conn.commit()
        conn.close()
        score = row[0][3]

        if (score == None):
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("UPDATE users SET score = ?, time = ? WHERE id = ?", (output, time, session["user_id"]))
            conn.commit()
            conn.close()
        elif (output < score):
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("UPDATE users SET score = ?, time = ? WHERE id = ?", (output, time, session["user_id"]))
            conn.commit()
            conn.close()

        return render_template("play.html")


    else:
        return render_template("play.html")

@app.route('/leaderboard', methods=["GET"])
@login_required
def leaderboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    leaderboard_data = c.execute("SELECT username, time, score FROM users ORDER BY score ASC").fetchall()
    conn.commit()
    conn.close()
    ranked_data = [(rank + 1, username, time, score) for rank, (username, time, score) in enumerate(leaderboard_data) if (time != None)]
    return render_template("leaderboard.html", leaderboard_data = ranked_data)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    # The 'WERKZEUG_RUN_MAIN' check prevents opening two tabs when using debug mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open('http://127.0.0.1:5000')
    
    app.run(debug=True)