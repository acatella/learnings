from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    #get all the users stocks 
    portfolio = db.execute("SELECT symbol, shares, name FROM portfolios WHERE user_id = :user_id",user_id=session["user_id"])
    portfolioValue = 0;
    
    # append additional info
    for stock in portfolio:
        stockState = lookup(stock['symbol'])
        stock['price'] = round(stockState['price'],2)
        stock['value'] = round(stock['price'] * stock['shares'],2)
        portfolioValue += stock['value']
    
    # prepare info for rendering
    cash = db.execute("SELECT cash FROM users WHERE id = :id",id=session["user_id"])
    totalValue = cash[0]['cash'] + portfolioValue    
    username = db.execute("SELECT username FROM users WHERE id = :id",id=session["user_id"])
        
        
    return render_template("index.html",username=username[0]['username'],cash=round(cash[0]['cash'],2),portfolioValue=round(portfolioValue,2),totalValue=round(totalValue,2), portfolio=portfolio)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    if request.method == "POST":
        stock = request.form.get("stock")
        stockInfo = lookup(stock)
        print(stockInfo)
        # ensure info was entered correctly
        if not stockInfo:
            return apology("Please use a valid","Stock ticker symbol")
        
        try:
            amount = int(request.form.get("amount"))
            if (amount <= 0):
                return apology("Please enter a valid","Number of shares")
        except ValueError:
            return apology("Please enter a valid","Number of shares")
        
        # ensure the money is right
        userMoney = db.execute("SELECT cash FROM users WHERE id = :id",id=session["user_id"])
        userMoney = userMoney[0]['cash']
        purchaseAmount = stockInfo["price"] * amount
        
        if (not userMoney or (userMoney < purchaseAmount )):
            return apology("You're too broke for this...")
            
        userMoney = userMoney - purchaseAmount
        
        # insert transaction into transactions table
        result = db.execute("INSERT INTO transactions (symbol, shares, isSale, user_id) VALUES(:symbol,:shares,:isSale,:user_id)", symbol=stockInfo["symbol"],shares=amount,isSale=0,user_id=session["user_id"])
        
        # update users money
        result = db.execute("UPDATE users SET cash = :userMoney WHERE id = :id",userMoney=userMoney, id=session["user_id"])
        print(f"2nd result is {result}")
        # update user portfolio
        currentShares = db.execute("SELECT shares FROM portfolios WHERE user_id = :user_id AND symbol = :symbol",user_id=session["user_id"], symbol=stockInfo["symbol"])
        
        if (not currentShares):
            db.execute("INSERT INTO portfolios (symbol,shares,price,name,user_id) VALUES(:symbol,:shares,:price,:name,:user_id)", symbol=stockInfo["symbol"],shares=amount,price=stockInfo["price"],name=stockInfo["name"],user_id=session["user_id"])
        
        else:
            updatedShares = amount + currentShares[0]["shares"]
            db.execute("UPDATE portfolios SET shares = :shares WHERE user_id = :user_id AND symbol = :symbol", shares=updatedShares, user_id=session["user_id"], symbol=stockInfo["symbol"] )
        
        return redirect(url_for("index"))
        
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    if request.method == "POST":
        return apology("How??")    
        
    else:
        # create dict of transactions
        transactions = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=session["user_id"])
        
        for transaction in transactions:
            stockInfo = lookup(transaction['symbol'])
            transaction['name'] = stockInfo['name']
            transaction['price'] = stockInfo['price']
            
            if transaction["isSale"]:
                transaction['css'] = "red"
                transaction['value'] = round(transaction['price'] * -1 * transaction['shares'],2)
            else:
                transaction['css'] = "green"
                transaction['value'] = round(transaction['price'] * transaction['shares'],2)
            
        return render_template("history.html",transactions=transactions)
            
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "POST":
        stock = request.form.get("stock")
        stockInfo = lookup(stock)
        
        if not stockInfo:
            return apology("Please use a valid","Stock ticker symbol")
            
        return render_template("quoted.html", stockInfo=stockInfo)
        
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # if user submits a form, do stuff to db
    if request.method == "POST":
        
        # make sure no fields are empty
        if not request.form.get("username"):
            return apology("You need a username")
            
        elif (not request.form.get("password") or not request.form.get("password-confirm")):
            return apology("Please enter and confirm your password")
            
        if (request.form.get("password") != request.form.get("password-confirm")):
            return apology("Your passwords must match")
        
        username = request.form.get("username")
        hash = pwd_context.hash(request.form.get("password"))
        
        result = db.execute("INSERT INTO users (username,hash) VALUES (:username,:hash)", username=username, hash=hash)
        
        if not result:
            return apology("That username is taken", "Lo siento")
        
        newUser = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        session["user_id"] = newUser[0]["id"]
        
        # redirect user to home page
        return redirect(url_for("index"))
        
    # else, load the page
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    if request.method == "POST":
        
        stockInfo = lookup(request.form.get("symbol"))

        # log a transaction
        db.execute("INSERT INTO transactions (symbol, shares, isSale, user_id) VALUES(:symbol,:shares,:isSale,:user_id)", symbol=stockInfo["symbol"],shares=request.form.get("shares"),isSale=1,user_id=session["user_id"])
        
        # update portfolio
        db.execute("DELETE FROM portfolios WHERE user_id = :id AND symbol = :symbol", id=session["user_id"],symbol=stockInfo["symbol"])
        
        # update cash
        price = stockInfo["price"]
        amount = int(request.form.get("shares"))
        saleValue = price * amount
        cash = db.execute("SELECT cash FROM users WHERE id = :id",id=session["user_id"])
        cash = cash[0]["cash"] + saleValue
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",cash=cash, id=session["user_id"])
        
        # re render index
        return redirect(url_for("index"))
        
    else:    
        return apology("Plz sell on home page")

@app.route("/getmoney", methods=["GET","POST"])
@login_required
def getmoney():
    """Adds $$$ to a users cash up to $1m"""
    
    if request.method == "POST":
        
        # get that money!
        money = request.form.get("request")
        money = int(money)
        cash = db.execute("SELECT cash FROM users WHERE id = :id",id=session["user_id"])[0]["cash"]
        
        if cash + money > 1000000 :
            return apology("I think you have enough...")
        
        cash = cash + money
        
        # log the loan
        db.execute("INSERT INTO loans (amount, user_id) VALUES (:amount, :user_id)", amount=money, user_id=session["user_id"])
        
        db.execute("UPDATE users SET cash = :cash", cash=cash)
        
        return redirect(url_for("index"))
    else:
        return render_template("getmoney.html")