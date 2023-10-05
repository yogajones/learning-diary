from app import app
from flask import render_template, request, redirect
import messages, users, journeys

@app.route("/")
def index():
    user_id = users.user_id()
    if user_id == 0:
            return render_template("index.html", count=0, messages=[])
    else:
        list = messages.get_list(user_id)
        return render_template("index.html", count=len(list), messages=list)

@app.route("/new")
def new():
    user_id = users.user_id()
    learning_journeys = journeys.get_learning_journeys(user_id)
    return render_template("new.html", learning_journeys=learning_journeys)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    user_id = users.user_id()
    learning_journey_id = request.form.get("learning_journey_id")
    new_journey_title = request.form.get("new_journey_title")
    if new_journey_title:
        learning_journey_id = journeys.create_learning_journey(new_journey_title, user_id)
    if messages.send(content, user_id, learning_journey_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")