from db import db
from sqlalchemy import text
import users

def get_list(user_id):
    sql = "SELECT M.content, U.username, M.sent_at, LJ.title FROM messages M JOIN users U ON M.user_id = U.id LEFT JOIN learning_journeys LJ ON M.learning_journey_id = LJ.id WHERE M.user_id = :user_id ORDER BY M.sent_at DESC"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()

def send(content, user_id, learning_journey_id=None):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not learning_journey_id:
        learning_journey_id = None
    sql = "INSERT INTO messages (content, user_id, learning_journey_id, sent_at) VALUES (:content, :user_id, :learning_journey_id, NOW())"
    db.session.execute(text(sql), {"content": content, "user_id": user_id, "learning_journey_id": learning_journey_id})
    db.session.commit()
    return True
