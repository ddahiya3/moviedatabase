from flask.helpers import url_for
from app import app
from flask import render_template, request, redirect
from app import database as db_helper

@app.route('/', methods =["GET", "POST"])
def homepage():
    if request.method == "POST" :
        uname = request.form.get("uname") 
        password = request.form.get("pwd") 
        correct = db_helper.check_login_details(uname, password)
        if correct == 1 :
            return redirect(url_for('profile', username = uname))

    return render_template("loginpage.html")

@app.route('/profile/<username>', methods = ["GET", "POST"])
def profile(username) :
    if request.method == "POST" :
        if request.form["submit"] == "movieSearch" :
            moviename = request.form.get("userInput")
            return redirect(url_for('search_movie', movieName = moviename))   
        elif request.form["submit"] == "ratings" :
            pass
            #do something
        elif request.form["submit"] == "recommend" :
            pass
            #do something           
    return render_template("index.html", username = username)

@app.route('/search/<movieName>')          #TODO implement from here
def search_movie(movieName) :
    #need to implement search with sql query
    #return render_template
    col = ['name', 'idx']
    rows = db_helper.fake_movies()
    return render_template("table.html", columns = col, items = rows)
