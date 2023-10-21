"""Module to handle learning journey related SQL queries"""
from sqlalchemy import text
from db import db


def create(title, user_id):
    sql = "INSERT INTO learning_journeys (title, user_id) VALUES (:title, :user_id) RETURNING id"
    result = db.session.execute(text(sql), {"title": title, "user_id": user_id})
    db.session.commit()
    journey_id = result.fetchone()[0]
    return journey_id


def get_all(user_id):
    sql = "SELECT id, title FROM learning_journeys WHERE user_id=:user_id"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()


def get_one(learning_journey_id):
    sql = "SELECT id, title, user_id FROM learning_journeys WHERE id=:learning_journey_id"
    result = db.session.execute(text(sql), {"learning_journey_id": learning_journey_id})
    learning_journey = result.fetchone()
    return learning_journey
