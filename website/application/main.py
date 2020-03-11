from flask import Flask, redirect, render_template, session, url_for, request
from client import Client
from person import Person

NAME_KEY = 'name'
client = None
app = Flask(__name__)

app.secret_key = "hellomynameisvalandyouwontguessthis"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(request.form)
        session[NAME_KEY] = request.form["inputName1"]
        return redirect(url_for("home"))

    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home/")
def home():
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))

    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login": True, "session": session})


@app.route("/run/", methods=["GET"])
def run(url=None):
    global client
    msg = request.args.get("val")
    print(msg)
    if client != None:
        client.send_message(msg)

    return "none"


if __name__ == "__main__":
    app.run(debug=True)
