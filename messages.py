from db import db
from sqlalchemy import text
import users

def get_list(user_id):
    sql = "SELECT M.content, U.username, M.sent_at, LJ.title, M.id FROM messages M JOIN users U ON M.user_id = U.id LEFT JOIN learning_journeys LJ ON M.learning_journey_id = LJ.id WHERE M.user_id = :user_id ORDER BY M.sent_at DESC"
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

def get_entry_by_id(entry_id):
    sql = "SELECT * FROM messages M WHERE id=:entry_id"
    result = db.session.execute(text(sql), {"entry_id": entry_id})
    entry = result.fetchone()
    return entry

def update_entry_content(entry_id, new_content):
    sql = "UPDATE messages SET content=:new_content WHERE id=:entry_id"
    db.session.execute(text(sql), {"new_content": new_content, "entry_id": entry_id})
    db.session.commit()

def update_entry_learning_journey(entry_id, new_learning_journey_id):
    sql = "UPDATE messages SET learning_journey_id=:new_learning_journey_id WHERE id=:entry_id"
    db.session.execute(text(sql), {"new_learning_journey_id": new_learning_journey_id, "entry_id": entry_id})
    db.session.commit()
