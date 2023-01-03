from db import db
from flask import session

def create_conversation(topic, message_area_id, owner_id):
    sql = "INSERT INTO topics(topic, owner_id, message_area_id, created_at) \
        VALUES (:topic, :owner_id, :message_area_id, NOW()) RETURNING id"
    result = db.session.execute(sql, {"topic":topic, "owner_id":owner_id, "message_area_id":message_area_id})
    topic_id = result.fetchone()[0]
    db.session.commit()
    return topic_id

def send_message(content, user_id, topic_id, visibility):
    sql = "INSERT INTO messages(content, user_id, topic_id, visibility, sent_at) \
            VALUES (:content, :user_id, :topic_id, :visibility, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id, "topic_id":topic_id, "visibility":1})
    db.session.commit()

def delete_message(message_id):
    sql = "UPDATE messages SET visibility=0 WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    db.session.commit()
