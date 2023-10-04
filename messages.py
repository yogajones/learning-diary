from db import db
from sqlalchemy import text
import users

def get_list(user_id):
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND M.user_id=:user_id ORDER BY M.id"
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(text(sql), {"content":content, "user_id":user_id})
    db.session.commit()
    return True