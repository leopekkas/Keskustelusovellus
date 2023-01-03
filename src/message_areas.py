from db import db
from flask import session

def create_area(name, user_id):
    sql = "INSERT INTO message_areas(name, user_id) VALUES (:name, :user_id) RETURNING id"
    result = db.session.execute(sql, {"name":name, "user_id":user_id})
    area_id = result.fetchone()[0]
    db.session.commit()
    return area_id

def give_accessrights(area_id, user_id):
    sql = "INSERT INTO accessrights(message_area_id, user_id) VALUES (:message_area_id, :user_id)"
    db.session.execute(sql, {"message_area_id":message_area_id, "user_id":user_id}) 
    db.session.commit()
