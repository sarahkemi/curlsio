from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def sign_in():
	return "Your Name"

@app.route("/signup")
def sign_up():
	return render_template("signup.html")

@app.route("/profile")
def dashboard():
	return render_template("dashboard.html")

@app.route("/moves")
def moves():
	return render_template("moves.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0")
