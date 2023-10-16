from db import db
from sqlalchemy import text

def tag_exists(tag_name, user_id):
    sql = "SELECT id FROM tags WHERE name=:tag_name AND user_id=:user_id"
    result = db.session.execute(text(sql), {"tag_name": tag_name, "user_id": user_id})
    return result.scalar()

def create_tags(user_id, tag_names, entry_id):
    tags_list = [tag.strip() for tag in tag_names.split()]
    for tag_name in tags_list:
        if not tag_exists(tag_name, user_id):
            sql = "INSERT INTO tags (name, user_id) VALUES (:tag_name, :user_id) ON CONFLICT (name, user_id) DO NOTHING"
            db.session.execute(text(sql), {"tag_name": tag_name, "user_id": user_id})
            db.session.commit()

    for tag_name in tags_list:
        sql = "INSERT INTO entry_tags (entry_id, tag_id) SELECT :entry_id, T.id FROM tags T WHERE T.name=:tag_name AND T.user_id=:user_id"
        db.session.execute(text(sql), {"entry_id": entry_id, "tag_name": tag_name, "user_id": user_id})
    db.session.commit()
