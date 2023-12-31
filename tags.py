"""Module to handle tag-related SQL queries"""
from sqlalchemy import text
from db import db


def exists(tag_name, user_id):
    sql = "SELECT id FROM tags WHERE name=:tag_name AND user_id=:user_id"
    result = db.session.execute(text(sql), {"tag_name": tag_name, "user_id": user_id})
    return result.scalar()


def add(user_id, tag_name):
    sql = """INSERT INTO tags (name, user_id) VALUES (:tag_name, :user_id)
             ON CONFLICT (name, user_id) DO NOTHING"""
    db.session.execute(text(sql), {"tag_name": tag_name, "user_id": user_id})
    db.session.commit()


def delete(tag_id):
    sql = "DELETE FROM tags WHERE id = :tag_id"
    db.session.execute(text(sql), {"tag_id": tag_id})
    db.session.commit()


def link_to_entry(user_id, entry_id, tag_name):
    sql = """INSERT INTO entry_tags (entry_id, tag_id)
             SELECT :entry_id, T.id FROM tags T
             WHERE T.name=:tag_name AND T.user_id=:user_id"""
    db.session.execute(text(sql), {"entry_id": entry_id, "tag_name": tag_name, "user_id": user_id})


def unlink_from_entry(entry_id, tag_id):
    sql = "DELETE FROM entry_tags WHERE entry_id = :entry_id AND tag_id = :tag_id"
    db.session.execute(text(sql), {"entry_id": entry_id, "tag_id": tag_id})
    db.session.commit()


def create_tags_from_string(user_id, tag_names, entry_id):
    # interface to entries.py
    tags_list = [tag.strip() for tag in tag_names.split()]
    for tag_name in tags_list:
        if not exists(tag_name, user_id):
            add(user_id, tag_name)
        link_to_entry(user_id, entry_id, tag_name)
    db.session.commit()


def get(entry_id):
    # interface to routes.py
    sql = """SELECT T.name FROM tags T JOIN entry_tags ET ON T.id = ET.tag_id
             WHERE ET.entry_id=:entry_id"""
    result = db.session.execute(text(sql), {"entry_id": entry_id})
    return [row[0] for row in result.fetchall()]


def update(user_id, tag_names, entry_id):
    # interface to routes.py
    existing_tags = set(get(entry_id))
    new_tags = set(tag_names.split())

    tags_to_add = new_tags - existing_tags
    tags_to_remove = existing_tags - new_tags

    create_tags_from_string(user_id, " ".join(tags_to_add), entry_id)

    for tag_name in tags_to_remove:
        tag_name = tag_name.strip()
        tag_id = exists(tag_name, user_id)
        if tag_id:
            unlink_from_entry(entry_id, tag_id)

    db.session.commit()
