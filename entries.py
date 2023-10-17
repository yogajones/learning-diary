"""Module to handle learning diary entry related SQL queries"""
from sqlalchemy import text
from db import db
import users
import tags


def get_list(user_id):
    sql = """SELECT E.content, U.username, E.sent_at, LJ.title, E.id, array_agg(T.name) AS tags
             FROM entries E
             JOIN users U ON E.user_id = U.id
             LEFT JOIN learning_journeys LJ ON E.learning_journey_id = LJ.id
             LEFT JOIN entry_tags ET ON E.id = ET.entry_id
             LEFT JOIN tags T ON ET.tag_id = T.id
             WHERE E.user_id = :user_id
             GROUP BY E.id, U.username, LJ.title
             ORDER BY E.sent_at DESC"""
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()


def send(content, user_id, learning_journey_id=None, tag_names=None):
    user_id = users.get_user_id()
    if user_id == 0:
        return False

    sql = """INSERT INTO entries (content, user_id, learning_journey_id, sent_at)
             VALUES (:content, :user_id, :learning_journey_id, NOW())
             RETURNING id"""
    result = db.session.execute(
        text(sql),
        {
            "content": content,
            "user_id": user_id,
            "learning_journey_id": learning_journey_id,
        },
    )

    if tag_names:
        entry_id = result.scalar()
        tags.create_tags_from_string(user_id, tag_names, entry_id)

    db.session.commit()
    return True


def get_entry_by_id(entry_id):
    sql = """SELECT id, content, user_id, learning_journey_id, sent_at
             FROM entries WHERE id=:entry_id"""
    result = db.session.execute(text(sql), {"entry_id": entry_id})
    entry = result.fetchone()
    return entry


def update_entry_content(entry_id, new_content):
    sql = "UPDATE entries SET content=:new_content WHERE id=:entry_id"
    db.session.execute(text(sql), {"new_content": new_content, "entry_id": entry_id})
    db.session.commit()


def update_entry_learning_journey(entry_id, new_learning_journey_id):
    sql = "UPDATE entries SET learning_journey_id=:new_learning_journey_id WHERE id=:entry_id"
    db.session.execute(
        text(sql),
        {"new_learning_journey_id": new_learning_journey_id, "entry_id": entry_id},
    )
    db.session.commit()


def delete_entry(entry_id):
    sql = "SELECT tag_id FROM entry_tags WHERE entry_id = :entry_id"
    db.session.execute(text(sql), {"entry_id": entry_id}).fetchall()

    sql = "DELETE FROM entry_tags WHERE entry_id = :entry_id"
    db.session.execute(text(sql), {"entry_id": entry_id})

    sql = "DELETE FROM entries WHERE id = :entry_id"
    db.session.execute(text(sql), {"entry_id": entry_id})

    db.session.commit()
