"""Stock Portal App"""

import os
from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
from keys import SECRET_KEY
from models import db, connect_db, User, Stock, TrackedStock
from forms import SignUpForm, LoginForm, UserEditForm

API_BASE_URL = "https://financialmodelingprep.com/api/v3"

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///stocks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

def request_stock_list():
    """Return list of all stocks"""

    url = f"{API_BASE_URL}/stock/list?apikey={SECRET_KEY}"

    response = requests.get(url)
    r = response.json()

    return r

def add_stocks_to_db():
    r = request_stock_list()
    for i in range(len(r)):
        stock = Stock(
           symbol=r[i]['symbol'],
           name=r[i]['name'],
           exchange=r[i]['exchange'],
           type=r[i]['type'])
        
        db.session.add(stock)
        db.session.commit()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None
        

@app.route('/')
def welcome():
    """Show Welcome Page"""
    if g.user:
        return redirect('/homepage')

    return render_template('home.html')


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            new_user = User.signup(
                username=form.username.data, 
                password=form.password.data, 
                first_name=form.first_name.data, 
                last_name=form.last_name.data, 
                email=form.email.data)

            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(new_user)

        return redirect(f"/homepage")

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, 
                                 form.password.data) 
        if user:
            do_login(user)
            flash(f"Hello, {user.first_name}!", "success")
            return redirect('/homepage')

        flash("Invalid credentials.", 'danger')

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


@app.route('/profile', methods=["GET", 'POST'])
def edit_profile():
    """Show profile details and handle edit profile form submission."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data

            db.session.commit()
            flash("Profile Edited", "success")
            return redirect('/portal')

        flash("Password incorrect, please try again", "danger")

    return render_template('/edit.html', form=form, user_id=user.id)

@app.route('/homepage')
def home_page():
    """Render Stock Portal Home Page"""
    
    if g.user:

        return render_template('portal.html')

    else:
        return redirect('/login')


@app.route('/stock-search')
def search_for_stock():
    """Handle form submission and request stock details."""

    search = request.args.get('q').upper()
    if not search:
        flash("Please enter a valid stock ticker!")
    else:
        url = f"{API_BASE_URL}/quote/{search}?apikey={SECRET_KEY}"
        response = requests.get(url)
        r = response.json()

    return render_template('search_results.html', stock=r[0])


@app.route('/track-stock', methods=["GET", "POST"])
def track_a_stock():
    """Add a stock to tracked_stocks table"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    stock = request.args.get('tracked-stock')

    tracked_stock = TrackedStock(user_id=g.user.id, stock_symbol=stock)
    db.session.add(tracked_stock)
    db.session.commit()

    flash("Stock Tracked", "success")
    return redirect('/homepage')

@app.route('/stock-info/<stock_symbol>')
def Tracked_stock_info(stock_symbol):
    """Show tracked stock information"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        url = f"{API_BASE_URL}/quote/{stock_symbol}?apikey={SECRET_KEY}"
        response = requests.get(url)
        r = response.json()

    return render_template('stock_info.html', stock=r[0])


@app.route('/tickers-list')
def show_list_of_tickers():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        stocks = Stock.query.order_by(Stock.symbol).all()
    
    return render_template('tickers_list.html', stocks=stocks)


@app.route('/untrack-stock', methods=["GET", "POST"])
def untrack_stock():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        stock = request.args.get('tracked-stock')
        tracked_stock = TrackedStock.query.filter_by(user_id=g.user.id, stock_symbol=stock)
        db.session.delete(tracked_stock[0])
        db.session.commit()

        flash("Stock Untracked", "info")
        return redirect('/homepage')








