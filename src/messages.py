from db import db
from flask import session
import users

def get_list():
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND visibility=1 ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def delete(message_id):
    sql = "UPDATE messages SET visibility=0 WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    db.session.commit()

def search(input):
    sql = "SELECT messages:message, users.username FROM messages WHERE visibility=:visibility AND messages.user_id=users.id AND messages.message LIKE :input"
    result = db.session.execute(sql, {"visibility":1, "input":"%" + input + "%"})
    matches = resul.fetchall()
    return matches
