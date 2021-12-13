from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
     return render_template("index.html")

@app.route("/bonus", methods=["GET","POST"])
def bonus():





    return render_template("bonus.html", original="test1", found = "test2")
