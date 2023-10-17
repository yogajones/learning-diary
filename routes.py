"""Module to handle routes"""
from flask import abort, render_template, request, redirect, flash, session
from app import app
import entries
import users
import journeys
import tags

@app.before_request
def check_authentication():
    if request.endpoint not in ["login", "/", "register"]:
        user_id = users.get_user_id()
        if user_id == 0:
            flash("Please log in to continue", "User not found")
            return redirect("/login")

@app.route("/")
def index():
    user_id = users.get_user_id()
    if user_id == 0:
        return redirect("/login")

    entry_list = entries.get_list(user_id)
    return render_template("index.html", count=len(entry_list), entries=entry_list)


@app.route("/new")
def new():
    user_id = users.get_user_id()
    learning_journeys = journeys.get_learning_journeys(user_id)
    return render_template("new.html", learning_journeys=learning_journeys)


@app.route("/send", methods=["POST"])
def send():
    user_id = users.get_user_id()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    content = request.form["content"]
    learning_journey_id = request.form.get("learning_journey_id")
    tags_input = request.form.get("tags")
    new_journey_title = request.form.get("new_journey_title")
    if new_journey_title:
        learning_journey_id = journeys.create_learning_journey(
            new_journey_title, user_id
        )

    if entries.send(content, user_id, learning_journey_id, tags_input):
        return redirect("/")
    flash("Failed to submit entry", "Error")
    return redirect("/send")


@app.route("/edit_entry/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    user_id = users.get_user_id()
    entry = entries.get_entry_by_id(entry_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")

    current_learning_journey = journeys.get_learning_journey_by_id(entry.learning_journey_id)
    entry_tags = ", ".join(tags.get_tags_by_entry_id(entry_id))

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_content = request.form["content"]
        new_learning_journey_id = request.form.get("learning_journey_id")
        new_journey_title = request.form.get("new_journey_title")
        new_tags = request.form["tags"]

        if new_learning_journey_id == "":
            new_learning_journey_id = None

        if new_journey_title:
            new_learning_journey_id = journeys.create_learning_journey(new_journey_title, user_id)

        entries.update_entry_content(entry_id, new_content)
        entries.update_entry_learning_journey(entry_id, new_learning_journey_id)
        tags.update_tags(user_id, new_tags, entry_id)

        return redirect("/")

    learning_journeys = journeys.get_learning_journeys(user_id)
    return render_template(
        "edit_entry.html",
        entry=entry,
        entry_id=entry_id,
        entry_content=entry.content,
        learning_journeys=learning_journeys,
        entry_learning_journey=current_learning_journey,
        entry_tags=entry_tags,
    )


@app.route("/delete_entry/<int:entry_id>")
def delete_entry(entry_id):
    user_id = users.get_user_id()
    entry = entries.get_entry_by_id(entry_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")

    entry_tags = tags.get_tags_by_entry_id(entry_id)

    return render_template(
        "delete_entry.html",
        entry=entry,
        entry_id=entry_id,
        entry_tags=entry_tags
    )


@app.route("/confirm_delete/<int:entry_id>", methods=["POST"])
def confirm_delete(entry_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_id = users.get_user_id()
    entry = entries.get_entry_by_id(entry_id)

    if not entry:
        flash("Entry not found", "Error")
        return redirect("/")
    if entry.user_id != user_id:
        flash("Unauthorized access", "Error")
        return redirect("/")

    entries.delete_entry(entry_id)
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
    entry_list = entries.get_list(user_id)

    return render_template(
        "profile.html",
        username=username,
        entry_count=len(entry_list)
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
