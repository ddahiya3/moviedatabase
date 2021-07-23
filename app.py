from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, g, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import os
import json
import datetime
import pandas as pd
import numpy as np

import database as db_helper
import sqlalchemy
from yaml import load, Loader


login_manager = LoginManager()

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(uname):
    if not db_helper.check_existing_user(uname):
        return None

    user = User()
    user.id = uname
    return user

@login_manager.request_loader
def request_loader(request):
    uname = request.form.get("uname") 
    password = request.form.get("pwd") 
    can_login = db_helper.check_login_details(uname, password)
    if not can_login:
        return None

    user = User()
    user.id = uname
    user.is_authenticated = True # TODO: maybe unecessary
    return user

app  = Flask(__name__)

login_manager.init_app(app)

def init_connect_engine() :
    if os.environ.get("GAE_ENV") != 'standard' :
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables :
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername = 'mysql+pymysql',
            username = os.environ.get('MYSQL_USER'),
            password = os.environ.get('MYSQL_PASSWORD'),
            database = os.environ.get('MYSQL_DB'),
            host = os.environ.get('MYSQL_HOST')
        )
    )
    return pool

db = init_connect_engine()

@app.route('/')
@login_required
def index():
    # return "Hello World"
    return render_template("index.html", username=current_user.id)


@app.route('/login', methods =["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    uname = request.form.get("uname") 
    password = request.form.get("pwd") 
    can_login = db_helper.check_login_details(uname, password)
    if can_login:
        user = User()
        user.id = uname
        login_user(user, remember=False)
        return render_template("index.html", username=uname)
    else:
        return render_template("login.html")

    # TODO: add message for bad password uname combiation

@app.route("/signup", methods =["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    uname = request.form.get("uname") 
    password = request.form.get("pwd") 
    #TODO: ADD CONFIRM PASSWORD MAYBE

    existing_user = db_helper.check_existing_user(uname)
    if existing_user:
        flash("Account with username " + str(uname) + " already exists. Login to continue!") #TODO: see alternate OF FLASH
    else:
        db_helper.add_new_user(uname, password)
        flash("Account with username " + str(uname) + " created. Login to continue!")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@app.route('/aq1', methods =["GET", "POST"])
@login_required
def aq1():
    if request.method == "GET":
        return render_template("aq1.html")

    director_letter1 = request.form.get("dl1")
    director_letter2 = request.form.get("dl2")

    req_result = db_helper.advanced_query_1(director_letter1, director_letter2)
    df = pd.DataFrame(req_result, columns=["Movie Name", "Director"])
    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/aq2', methods =["GET", "POST"])
@login_required
def aq2():
    if request.method == "GET":
        return render_template("aq2.html")

    director_name = request.form.get("dname")

    req_result = db_helper.advanced_query_2(director_name)
    df = pd.DataFrame(req_result, columns=["Movie Name", "Director", "Duration"])
    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/ratings', methods =["GET"])
@login_required
def ratings():
    user_ratings = db_helper.user_ratings(current_user.id)
    return render_template("ratings.html", ratings=user_ratings)

@app.route('/delete_rating/<movie_name>')
@login_required
def delete_rating(movie_name):
    db_helper.delete_rating_query(current_user.id, str(movie_name))
    return redirect(url_for('ratings'))

@app.route('/update_rating/<movie_name>', methods =["GET", "POST"])
@login_required
def update_rating(movie_name):
    if request.method == "GET":
        return render_template("update_rating.html", movie=movie_name)

    new_rating = request.form.get("new_rating")
    db_helper.update_rating_query(current_user.id, movie_name, new_rating)
    return redirect(url_for('ratings'))




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    # app.debug = False
    app.run(debug=True)

