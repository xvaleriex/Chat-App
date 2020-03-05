from flask import Flask, redirect,  render_template, session, url_for, request
from client import Client
NAME_KEY = 'name'

app = Flask(__name__)

app.secret_key = "hellomynameisvalandyouwontguessthis"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(request.form)
        session[NAME_KEY] = request.form["inputName1"]
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("home"))

    return render_template("index.html")


@app.route("/run")
def run():
    print ("Hello")
    return ("nothing")

if __name__ == "__main__":
    app.run(debug=True)
