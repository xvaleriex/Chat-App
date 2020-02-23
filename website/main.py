from flask import Flask, redirect,  render_template, session, url_for

NAME_KEY = 'name'

app = Flask(__name__)

app.secret_key = "hellomynameisvalandyouwontguessthis"

session[NAME_KEY] = "val"
"""
@app.route("/login")
def login():
    return render_template("login.html")
"""

@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("home"))

    name = session[NAME_KEY]
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
