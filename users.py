"""Module to handle user-related queries"""
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy import text
from db import db


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token
        return True
    return False


def logout():
    del session["user_id"]
    del session["csrf_token"]


def username_available(username):
    sql = "SELECT 1 FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {"username": username})
    return result.fetchone() is None


def register_user(username, password1, password2):
    if not username:
        return "Username cannot be empty"
    if not username_available(username):
        return "Username is already taken"
    if password1 != password2:
        return "Passwords don't match"
    if len(password1) < 8:
        return "Password must contain at least 8 characters"
    if len(password1) > 40:
        return "Password cannot contain more than 40 characters"

    hash_value = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return "Unknown error: Failed to create account"

    return None


def get_user_id():
    return session.get("user_id", 0)


def get_username(user_id):
    sql = "SELECT username FROM users WHERE id = :user_id"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchone()[0]


def delete_account(user_id):
    sql = "DELETE FROM users WHERE id = :user_id"
    try:
        db.session.execute(text(sql), {"user_id": user_id})
        db.session.commit()
        return True
    except:
        return False
