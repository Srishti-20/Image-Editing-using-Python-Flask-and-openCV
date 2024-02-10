# Flask, HTML file, Bootstrap
from flask import Flask,  render_template

app = Flask(__name__)

# WSGI Application
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

app.run(debug=True, port = 5002)