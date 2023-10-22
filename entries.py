"""Module to handle learning diary entry related SQL queries"""
from sqlalchemy import text
from db import db
import users
import tags
import breakthroughs
import journeys


def get_all(user_id):
    sql = """SELECT E.content, U.username, E.sent_at, LJ.title, E.id,
             array_agg(T.name) as tags,
             B.entry_id IS NOT NULL as has_breakthrough
             FROM entries E
             JOIN users U ON E.user_id = U.id
             LEFT JOIN learning_journeys LJ ON E.learning_journey_id = LJ.id
             LEFT JOIN entry_tags ET ON ET.entry_id = E.id
             LEFT JOIN tags T ON ET.tag_id = T.id
             LEFT JOIN LATERAL (
                SELECT entry_id FROM breakthroughs B
                WHERE B.user_id = :user_id AND B.entry_id = E.id
                ) B ON true
             WHERE E.user_id = :user_id
             GROUP BY E.id, U.username, LJ.title, B.entry_id
             ORDER BY E.sent_at DESC"""
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()


def get_all_by_learning_journey(user_id, learning_journey_title):
    sql = """SELECT E.content, U.username, E.sent_at, LJ.title, E.id,
             array_agg(T.name) as tags,
             B.entry_id IS NOT NULL as has_breakthrough
             FROM entries E
             JOIN users U ON E.user_id = U.id
             LEFT JOIN learning_journeys LJ ON E.learning_journey_id = LJ.id
             LEFT JOIN entry_tags ET ON ET.entry_id = E.id
             LEFT JOIN tags T ON ET.tag_id = T.id
             LEFT JOIN LATERAL (
                SELECT entry_id FROM breakthroughs B
                WHERE B.user_id = :user_id AND B.entry_id = E.id
                ) B ON true
             WHERE E.user_id = :user_id AND LJ.title = :learning_journey_title
             GROUP BY E.id, U.username, LJ.title, B.entry_id
             ORDER BY E.sent_at DESC"""
    result = db.session.execute(
        text(sql),
        {"user_id": user_id, "learning_journey_title": learning_journey_title},
    )
    return result.fetchall()


def send(
    content, user_id, learning_journey_id=None, tag_names=None, breakthrough=False
):
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

    entry_id = result.scalar()

    if tag_names:
        tags.create_tags_from_string(user_id, tag_names, entry_id)

    if breakthrough:
        breakthroughs.process(user_id, entry_id, breakthrough)

    db.session.commit()
    return True


def get_one(entry_id):
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


def process_update(
    user_id,
    entry_id,
    new_content,
    new_journey_title,
    new_learning_journey_id,
    new_tags,
    new_breakthrough,
):
    try:
        if new_learning_journey_id == "":
            new_learning_journey_id = None

        if new_journey_title:
            new_learning_journey_id = journeys.create(new_journey_title, user_id)
        update_entry_content(entry_id, new_content)
        update_entry_learning_journey(entry_id, new_learning_journey_id)
        tags.update(user_id, new_tags, entry_id)
        breakthroughs.process(user_id, entry_id, new_breakthrough)
        return True
    except:
        return False
