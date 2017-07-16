
import os
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,session, abort, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from flask_login import login_user,logout_user,current_user
from . import forms
import datetime
import random
import sys
import requests

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@104.196.135.151/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://tcweiqzaibybtr:0fa949e74472ae8a71a9c1fe09ba5237fa82339e376f43929a54b402b016fa7d@ec2-107-20-255-96.compute-1.amazonaws.com/db9p4jqu1kncao"
#
DATABASEURI = "postgresql://tcweiqzaibybtr:0fa949e74472ae8a71a9c1fe09ba5237fa82339e376f43929a54b402b016fa7d@ec2-107-20-255-96.compute-1.amazonaws.com/db9p4jqu1kncao"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def sign_in():
    form = SignInForm(csrf_enabled=False)

    if request.method == "GET":
        return render_template("signin.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("signin.html", form=form)
        else:
            # new_user =
            render_template("dashboard.html", form=form)

@app.route("/signup")
def sign_up():
    form = SignUpForm(csrf_enabled=False)

    if request.method == "GET":
        return render_template("signup.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("signup.html", form=form)
        else:
            # new_user =
            render_template("dashboard.html", form=form)

@app.route("/profile")
def dashboard():
	return render_template("dashboard.html")

@app.route("/moves")
def moves():
    form = CreateMoveForm(csrf_enabled=False)

    if request.method == "GET":
        return render_template("moves.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("moves.html", form=form)
        else:
            return render_template("feed.html", form=form)


@app.route("/template")
def template():
    return render_template("template.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0")
