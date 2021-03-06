
import os
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,session, abort, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from flask_login import login_user,logout_user,current_user
from forms import SignInForm, SignUpForm, CreateMoveForm, CitySearchForm, CommentForm
import datetime
import random
import sys
import requests

app = Flask(__name__)
app.secret_key = 'super secret key'
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

@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    form = SignInForm(csrf_enabled=False)
    if request.method == "GET":
        return render_template("signin.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("signin.html", form=form)
        else:
            result = g.conn.execute('''SELECT EXISTS (SELECT * FROM people
            WHERE email = '%s' AND password = '%s')''' % (form.email.data, form.password.data))
            row = result.fetchone()

            if row[0]:
              person = g.conn.execute('''(SELECT * FROM people WHERE email = '%s' AND password = '%s' LIMIT 1)''' % (form.email.data, form.password.data))
              person_id = (person.fetchone()[0])
              peeps = g.conn.execute('''(SELECT * FROM people WHERE email = '%s' AND password = '%s' LIMIT 1)''' % (form.email.data, form.password.data))
              person_name = (peeps.fetchone()[9])
              session['email'] = form.email.data
              session['person_id'] = person_id
              session['person_name'] = person_name
              return render_template("dashboard.html", form=form)
            else:
              return render_template("signin.html", form=form,session=session)


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm(csrf_enabled=False)

    if request.method == "GET":
        return render_template("signup.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("signup.html", form=form)
        else:
            num = g.conn.execute('''SELECT COUNT(person_id)
FROM people''')
            p_id = num.fetchone()[0]
            p_id = p_id + 1
            g.conn.execute('''INSERT INTO people
            (person_id, name, email, race, current_city, pronouns, password)
            VALUES ( (%s),(%s),(%s),(%s),(%s),(%s),(%s))''',
                                      p_id, form.name.data, form.email.data, form.race.data,
                                      form.city.data,form.pronouns.data, form.password.data)
            return render_template("dashboard.html", form=form)

@app.route("/dashboard/<type>")
def dashboard(type):
  moves = g.conn.execute('''(SELECT * FROM moves WHERE type = '%s')''' % type)
  return render_template("feed.html", feed = moves)

@app.route("/new", methods=["GET", "POST"])
def moves():
    form = CreateMoveForm(csrf_enabled=False)

    if request.method == "GET":
        return render_template("new.html", form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template("new.html", form=form)
        else:
            num = g.conn.execute('''SELECT COUNT(move_id) FROM moves''')
            m_id = num.fetchone()[0]
            m_id = m_id + 1
            today = datetime.date.today()
            g.conn.execute('''INSERT INTO moves
            (move_id, type, city, date, person_asked, move_text)
            VALUES ( (%s),(%s),(%s),(%s),(%s),(%s))''',
                                      m_id, form.move_type.data, form.city.data, today,
                                      session['person_name'], form.text.data)
            return redirect(url_for('feed'))

@app.route("/feed", methods=["GET", "POST"])
def feed():
  current_city = g.conn.execute('''SELECT current_city from people WHERE people.person_id =(%s)''', session['person_id'])
  city = current_city.fetchone()[0]
  feed_data = g.conn.execute('''SELECT * from moves WHERE moves.city = (%s) OR moves.person_asked= (%s)''', city, session['person_name'])
  return render_template("feed.html", feed=feed_data)

@app.route("/post/<move_id>", methods=["GET", "POST"])
def post(move_id):
    form = CommentForm(csrf_enabled=False)

    if request.method == "GET":
      move = g.conn.execute('''SELECT * from moves WHERE moves.move_id = (%s)''', move_id)
      fetch = move.fetchone()
      person = fetch[4]
      move = fetch[5]
      comments_data = g.conn.execute('''SELECT * from comments WHERE comments.move_id = (%s)''', move_id)
      return render_template("post.html", move=move, comments=comments_data, form=form, person=person)
    elif request.method == "POST":
        if not form.validate():
            return render_template("post.html", move=move, form=form)
        else:
            num = g.conn.execute('''SELECT COUNT(comment_id) FROM comments''')
            c_id = num.fetchone()[0]
            c_id = c_id + 201
            today = datetime.date.today()
            g.conn.execute('''INSERT INTO comments
            (comment_id, comment, comment_date, move_id, person)
            VALUES ( (%s),(%s),(%s),(%s),(%s))''',
                                      c_id, form.text.data, today, move_id, session['person_name'])
            return redirect(url_for('feed'))

@app.route("/template")
def template():
    return render_template("template.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
