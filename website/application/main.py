import time
from threading import Thread

from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from client import Client
from person import Person

NAME_KEY = 'name'
messages = []
client = None
app = Flask(__name__)

app.secret_key = "hellomynameisvalandyouwontguessthis"


def disconnect():
    """
    Call this before client disconnet from server
    :return:
    """
    global client
    if client:
        client.disconnect()


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Displays login page and saves name in session
    :return:
    """
    if request.method == "POST":
        print(request.form)
        session[NAME_KEY] = request.form["inputName1"]
        return redirect(url_for("home"))

    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    """
        Displays logout page
        :return:
        """
    session.pop(NAME_KEY, None)
    disconnect()
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home/")
def home():
    """
    Displays home page if logged in
    :return:
    """
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))

    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login": True, "session": session})


@app.route("/send_message", methods=["GET"])
def send_message():
    """
    Called from JQuery to send messages
    :param url:
    :return:
    """
    global client
    msg = request.args.get("val")
    print(msg)
    if client:
        client.send_message(msg)

    return "none"


def update_messages():
    global messages
    run = True
    while run:
        time.sleep(0.1)
        if not client: continue
        new_msgs = client.get_messages()
        messages.extend(new_msgs)

        for msg in new_msgs:
            print(msg)
            if msg == "quit":
                run = False
                break


@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)

