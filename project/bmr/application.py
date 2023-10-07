import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/calculate", methods=["GET", "POST"])
@login_required
def calc():
    if request.method == "POST":
        gender = request.form.get("gender")
        now = datetime.datetime.now()
        if gender == 1:
            weight = float(request.form.get("weight"))
            height = float(request.form.get("height"))
            age = float(request.form.get("age"))
            BMR = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
            round(BMR,2)
            db.execute("INSERT INTO BMR (BMR,date,user_id) VALUES (?, ?, ?)",BMR,now,session["user_id"])
            return redirect("/user")

        else:
            weight = float(request.form.get("weight"))
            height = float(request.form.get("height"))
            age = float(request.form.get("age"))
            BMR = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
            round(BMR,2)
            db.execute("INSERT INTO BMR (BMR,date,user_id) VALUES (?, ?, ?)",BMR,now,session["user_id"])
            return redirect("/user")

    else:
        return render_template("calculate.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("users.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO users (username,password) VALUES (?, ?)",username,password)
        except ValueError as e:
            if "UNIQUE" in str(e):
                return apology("Record already exists",400)
            else:
                raise
        except:
            raise
        #db.execute("INSERT INTO users (username,hash) VALUES (?, ?)",username,password)
        return render_template("homepage.html")

    else:
        return render_template("register.html")


@app.route("/user", methods=["GET", "POST"])
@login_required
def display():

    #get the most recently calculated BMR
    BMR = db.execute("SELECT BMR FROM BMR WHERE user_id = :user_id ORDER BY date DESC LIMIT 1", user_id=session.get("user_id"))
    one = BMR[0]

    #get all the data for the user
    datathon = db.execute("SELECT date, BMR FROM BMR WHERE user_id = :user_id ORDER BY date ASC", user_id=session.get("user_id"))
    #display leData that leBron will not leFlop on
    labels = []
    values = []
    for row in datathon:
        labels.append(row["date"])
        values.append(row["BMR"])
    return render_template("users.html", BMR=one, labels=labels, values=values)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
