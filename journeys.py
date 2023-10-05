from db import db
from sqlalchemy import text

def create_learning_journey(title, user_id):
    sql = "INSERT INTO learning_journeys (title, user_id) VALUES (:title, :user_id) RETURNING id"
    result = db.session.execute(text(sql),{"title": title, "user_id": user_id})
    db.session.commit()
    journey_id = result.fetchone()[0]
    return journey_id

def get_learning_journeys(user_id):
    sql = "SELECT id, title FROM learning_journeys WHERE user_id=:user_id"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()