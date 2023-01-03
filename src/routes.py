from app import app
from db import db
from flask import render_template, request, redirect, session
import messages, users

@app.route("/")
def index():
    list = messages.get_list()
    # Fetch all message areas
    sql = "SELECT id, name FROM message_areas"
    result = db.session.execute(sql)
    message_areas = result.fetchall()
    # Fetch access rights and private messaging areas (plus admin rights)
    admin = users.admin()
    user_id = users.user_id()
    sql = "SELECT message_areas.name, message_areas.id, message_areas.user_id FROM message_areas, access_rights \
        WHERE access_rights.user_id=:user_id AND access_rights.message_area_id=message_areas.id"
    result = db.session.execute(sql, {"user_id":user_id})
    private_areas = result.fetchall()
    if private_areas == None:
        private_areas = []
    return render_template("index.html", count=len(list), message_areas=message_areas, admin=admin, private_areas=private_areas)

@app.route("/new/<int:id>")
def new(id):
    sql = "SELECT name FROM message_areas WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    message_area = result.fetchone()[0]
    return render_template("new.html", id=id, message_area=message_area)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Unable to send a message")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = request.form.get("admin")
        if password1 != password2:
            return render_template("error.html", message="Passwords differ!")
        if users.register(username, password1, admin):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Unable to register the account")

@app.route("/area/<int:id>")
def area(input_id):
    sql = "SELECT id, name from areas WHERE id=:id"
    result = db.session.execute(sql, {"id":input_id})
    area = result.fetchone()
    if area == None:
        return render_template("error.html", message="Message area not found")
    sql = "SELECT messages.id, messages.content \
            FROM messages WHERE visibility=1"
    result = db.session.execute(sql)
    message_list = result.fetchall()
    return render_template("area.html", messages=message_list)
