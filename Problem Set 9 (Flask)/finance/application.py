import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #return apology("TODO")
    stocks = db.execute("SELECT stock, SUM(price), SUM(shares) AS totals FROM purchases WHERE user_id = :user_id GROUP BY stock", user_id=session.get("user_id"))
    #i = db.execute("SELECT COUNT(stock) FROM purchases WHERE user_id = :user_id GROUP BY stock", user_id=session.get("user_id"))
    #basically stocks is like a 2d array
    #new_portfolio = {}
    stock_value = 0
    for stock in stocks:
        INFO = lookup(stock["stock"])
        stock["stock"] = INFO["symbol"]
        stock["price"] = INFO["price"]
        stock["name"] = INFO["name"]
        stock_value += float(stock["price"]*stock["totals"])
        print(stock)


    row = db.execute("SELECT cash FROM users WHERE id = :id", id=session.get("user_id"))
    cash = float(row[0]["cash"])
    print("\n")
    #print("New Portfolio: ")
    #print(new_portfolio)
    print("Stonks: ")
    print(stocks)
    print("\n")
    return render_template("index.html", new_portfolio=stocks, cash=cash, stock_value = stock_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if lookup(request.form.get("symbol")) is None:
            return apology("invalid stock symbol", 400)

        elif request.form.get("shares") is None:
            return apology("invalid number of shares "+request.form.get("shares"), 400)

        else:
            shares_value = request.form.get("shares")

            try:
                num_shares = int(shares_value)
            except:
                return apology("please enter a numeric value", 400)

            if float(shares_value) != num_shares:
                return apology("Enter whole numbers only", 400)

            elif num_shares < 0:
                return apology("enter positive value", 400)

        INFORMATION = lookup(request.form.get("symbol"))
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        cash = float(row[0]["cash"])
        shares = float(request.form.get("shares"))
        pricetag = float(INFORMATION["price"])
        now = datetime.datetime.now()
        if (pricetag*shares) > cash:
            return apology("you're broke bitch", 403)

        else:
            #INFORMATION = lookup(request.form.get("symbol"))
            db.execute("INSERT INTO purchases (user_id,stock,price,date,shares) VALUES (?, ?, ?, ?, ?)",session["user_id"],INFORMATION["symbol"],pricetag,now,shares)


            currentcash = cash - shares*pricetag
            db.execute("UPDATE users SET cash= :cash WHERE id = :id", cash = currentcash, id = session["user_id"])
            return redirect("/")
            #return apology("bought {} shares at {} for a total purchase price of {}".format(shares,pricetag,round(shares*pricetag,2)),200)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT stock, price, shares, date FROM purchases WHERE user_id = :user_id", user_id=session.get("user_id"))

    for stock in stocks:
        INFO = lookup(stock["stock"])
        stock["name"] = INFO["name"]
        print(stock)

    row = db.execute("SELECT cash FROM users WHERE id = :id", id=session.get("user_id"))
    cash = float(row[0]["cash"])
    print("\n")
    #print("New Portfolio: ")
    #print(new_portfolio)
    print("Stonks: ")
    print(stocks)
    print("\n")
    return render_template("history.html", new_portfolio=stocks, cash=cash)


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
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if lookup(request.form.get("symbol")) is None:
            return apology("invalid stock symbol", 400)

        else:
            INFORMATION = lookup(request.form.get("symbol"))
            if INFORMATION is None:
                return apology("invalid stock symbol", 400)
            return render_template("quoted.html", information=INFORMATION)

    else:
        return render_template("quote.html")



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
            db.execute("INSERT INTO users (username,hash) VALUES (?, ?)",username,password)
        except ValueError as e:
            if "UNIQUE" in str(e):
                return apology("Record already exists",400)
            else:
                raise
        except:
            raise
        #db.execute("INSERT INTO users (username,hash) VALUES (?, ?)",username,password)
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if float(request.form.get("shares")) < 0:
            return apology("Please enter a positive number",400)

        stocks = db.execute("SELECT stock FROM purchases WHERE user_id = :user_id GROUP BY stock", user_id=session.get("user_id"))
        found = False
        for i in stocks:
            if request.form.get("symbol") == i["stock"]:
                found = True
                break

        if not found:
            return apology("Please enter the symbol of a stock you own", 400)

        #total_shares = db.execute("SELECT SUM(shares) FROM purchases WHERE user_id = :user_id AND stock = :stonk GROUP BY stock", user_id=session.get("user_id"), stonk=request.form.get("symbol"))
        stocks = db.execute("SELECT * FROM purchases WHERE user_id = :user_id AND stock =:stonk GROUP BY stock", user_id=session.get("user_id"), stonk=request.form.get("symbol"))
        total_shares = stocks[0]["shares"]
        if float(request.form.get("shares")) > total_shares:
            return apology("You don't own that many shares",400)

        #add new row with -3 (would still work in index lmfao)
        shares = float(request.form.get("shares"))

        new_amount = -1*shares
        INFORMATION = lookup(request.form.get("symbol"))
        pricetag = INFORMATION["price"]
        now = datetime.datetime.now()
        db.execute("INSERT INTO purchases (user_id,stock,price,date,shares) VALUES (?, ?, ?, ?, ?)",session["user_id"],INFORMATION["symbol"],pricetag,now,new_amount)
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        cash = float(row[0]["cash"])
        currentcash = cash + shares*INFORMATION["price"]
        db.execute("UPDATE users SET cash= :cash WHERE id = :id", cash = currentcash, id = session["user_id"])
        return redirect("/")

    else:
        stocks = db.execute("SELECT stock, SUM(price), SUM(shares) AS totals FROM purchases WHERE user_id = :user_id GROUP BY stock", user_id=session.get("user_id"))
        #i = db.execute("SELECT COUNT(stock) FROM purchases WHERE user_id = :user_id GROUP BY stock", user_id=session.get("user_id"))
        #basically stocks is like a 2d array
        #new_portfolio = {}
        stock_value = 0
        for stock in stocks:
            INFO = lookup(stock["stock"])
            stock["stock"] = INFO["symbol"]
            stock["price"] = INFO["price"]
            stock["name"] = INFO["name"]
            stock_value += float(stock["price"]*stock["totals"])
            print(stock)
            return render_template("sell.html",new_portfolio=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
