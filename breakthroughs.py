"""Module to handle breakthrough-related SQL queries"""
from sqlalchemy import text
from db import db


def exists(user_id, entry_id):
    sql = """SELECT EXISTS
             (SELECT 1 FROM breakthroughs B
             WHERE B.user_id = :user_id AND B.entry_id = :entry_id)"""
    result = db.session.execute(text(sql), {"user_id": user_id, "entry_id": entry_id})
    return result.scalar()


def get(user_id):
    sql = "SELECT entry_id FROM breakthroughs WHERE user_id = :user_id"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return [row[0] for row in result.fetchall()]


def attach(user_id, entry_id):
    sql = "INSERT INTO breakthroughs (user_id, entry_id)VALUES (:user_id, :entry_id)"
    db.session.execute(text(sql), {"user_id": user_id, "entry_id": entry_id})
    db.session.commit()


def delete(user_id, entry_id):
    sql = "DELETE FROM breakthroughs WHERE user_id = :user_id AND entry_id = :entry_id"
    db.session.execute(text(sql), {"user_id": user_id, "entry_id": entry_id})
    db.session.commit()


def process(user_id, entry_id, breakthrough):
    if breakthrough and not exists(user_id, entry_id):
        attach(user_id, entry_id)
    if not breakthrough and exists(user_id, entry_id):
        delete(user_id, entry_id)
