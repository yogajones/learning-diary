"""Module to handle routes"""
from flask import abort, render_template, request, redirect, flash, session
from app import app
import entries
import users
import journeys
import tags
import breakthroughs


@app.before_request
def check_authentication():
    if request.endpoint not in ["login", "/", "register"]:
        user_id = users.get_user_id()
        if user_id == 0:
            flash("Please log in to continue", "User not found")
            return redirect("/login")


@app.route("/", methods=['GET', 'POST'])
def index():
    user_id = users.get_user_id()
    learning_journeys = journeys.get_all(user_id)
    entry_list = entries.get_all(user_id)

    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        selected_journey_title = request.form.get("selected_journey")
        if selected_journey_title:
            entry_list = entries.get_all_by_learning_journey(user_id, selected_journey_title)

    return render_template('index.html', count=len(entry_list),entries=entry_list, learning_journeys=learning_journeys)

@app.route("/new")
def new():
    user_id = users.get_user_id()
    learning_journeys = journeys.get_all(user_id)
    return render_template("new.html", learning_journeys=learning_journeys)


@app.route("/send", methods=["POST"])
def send():
    user_id = users.get_user_id()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    content, learning_journey_id, tags_input, new_journey_title, breakthrough = (
        request.form.get("content"),
        request.form.get("learning_journey_id"),
        request.form.get("tags"),
        request.form.get("new_journey_title"),
        request.form.get("breakthrough"),
    )
    if new_journey_title:
        learning_journey_id = journeys.create(
            new_journey_title, user_id
        )
    if learning_journey_id == "":
        learning_journey_id = None

    if entries.send(content, user_id, learning_journey_id, tags_input, breakthrough):
        flash("Entry created!", "Success")
        return redirect("/")
    flash("Failed to submit entry", "Error")
    return redirect("/send")


@app.route('/edit_journey/<journey_title>', methods=['GET', 'POST'])
def edit_journey(journey_title):
    user_id = users.get_user_id()

    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_journey_title = request.form.get("new_journey_title")
        if journeys.rename(user_id, journey_title, new_journey_title):
            flash("Journey renamed!", "Success")
            return redirect("/")
        flash("Something went wrong. Perhaps you already have a journey with that name?", "Error")
        return redirect("/")
    return render_template('edit_journey.html', journey_title=journey_title)


@app.route("/edit_entry/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):

    ### move this to entries.py and return an Entry object
    user_id = users.get_user_id()
    entry = entries.get_one(entry_id)
    current_learning_journey = journeys.get_one(entry.learning_journey_id)
    entry_tags = " ".join(tags.get(entry_id))
    entry_breakthrough = breakthroughs.exists(user_id, entry_id)
    learning_journeys = journeys.get_all(user_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")
    ###

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_content, new_learning_journey_id, new_journey_title, new_tags = (
            request.form.get("content"),
            request.form.get("learning_journey_id"),
            request.form.get("new_journey_title"),
            request.form.get("tags"),
        )
        new_breakthrough = "new_breakthrough" in request.form

        if not entries.process_update(
            user_id,
            entry_id,
            new_content,
            new_journey_title,
            new_learning_journey_id,
            new_tags,
            new_breakthrough
        ):
            flash("Something went wrong", "Error")
            return redirect("/")
        flash("Entry updated!", "Success")
        return redirect("/")

    return render_template(
        "edit_entry.html",
        entry=entry,
        entry_id=entry_id,
        entry_content=entry.content,
        learning_journeys=learning_journeys,
        entry_learning_journey=current_learning_journey,
        entry_tags=entry_tags,
        entry_breakthrough=entry_breakthrough,
    )


@app.route("/delete_entry/<int:entry_id>")
def delete_entry(entry_id):
    user_id = users.get_user_id()
    entry = entries.get_one(entry_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")

    entry_tags = tags.get(entry_id)
    entry_breakthrough = breakthroughs.exists(user_id, entry_id)

    return render_template(
        "delete_entry.html",
        entry=entry,
        entry_id=entry_id,
        entry_tags=entry_tags,
        entry_breakthrough=entry_breakthrough,
    )


@app.route("/confirm_delete/<int:entry_id>", methods=["POST"])
def confirm_delete(entry_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_id = users.get_user_id()
    entry = entries.get_one(entry_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")

    entries.delete_entry(entry_id)
    flash("Entry deleted!", "Success")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        flash("Incorrect username or password", "Error")
        return render_template("login.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        validation_error = users.register_user(username, password1, password2)
        if validation_error:
            flash(validation_error, "Error")
            return render_template("register.html")

        if users.login(username, password1):
            flash("Account succesfully created", "Success")
            return redirect("/")


@app.route("/profile")
def profile():
    user_id = users.get_user_id()
    username = users.get_username(user_id)
    entry_list = entries.get_all(user_id)

    return render_template(
        "profile.html", username=username, entry_count=len(entry_list)
    )


@app.route("/delete_account")
def delete_account():
    return render_template("delete_account.html")


@app.route("/confirm_delete_account", methods=["POST"])
def confirm_delete_account():
    user_id = users.get_user_id()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if users.delete_account(user_id):
        flash("Account deleted", "Success")
        return redirect("/login")
    flash("Unknown error: Failed to delete account", "Error")
    return redirect("/")
