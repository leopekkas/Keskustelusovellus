
from app import app
from db import db
from flask import render_template, request, redirect, session
import users, conversation

@app.route("/")
def index():
    sql = "SELECT name, id, user_id FROM message_areas WHERE user_id IS NULL"
    result = db.session.execute(sql)
    message_areas = result.fetchall()
    result = db.session.execute("SELECT id, topic, message_area_id FROM topics ORDER BY id DESC")
    topics = result.fetchall()
    admin = users.admin()
    user_id = users.user_id()
    sql = "SELECT message_areas.name, message_areas.id, message_areas.user_id FROM message_areas, access_rights \
        WHERE access_rights.user_id=:user_id AND access_rights.message_area_id=message_areas.id"
    result = db.session.execute(sql, {"user_id":user_id})
    private_areas = result.fetchall()
    if private_areas == None:
        private_areas = []
    return render_template("index.html", message_areas=message_areas, topics=topics, admin=admin, private_area=private_areas)

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

@app.route("/create_topic", methods=["POST"])
def create():
    topic = request.form["topic"]
    if topic == "":
        return render_template("error.html", message = "Specify a topic")
    area_id = request.form["id"]
    starter_id = users.user_id()
    topic_id = conversation.create_conversation(topic, area_id, starter_id)
    message = request.form["message"]
    if message != "":
        conversation.send_message(message, starter_id, topic_id, 1)
    return redirect("/")

@app.route("/create_area")
def create_area():
    return render_template("create_area.html")

@app.route("/create_private_area", methods=["POST"])
def create_private():
    name = request.form["theme"]
    if name == "":
        return render_template("error.html", message = "Please name your messaging area")
    user_id = users.user_id()
    area_id = areas.create_area(name, user_id)
    areas.give_accessrights(area_id, user_id)
    return redirect("add_users/"+str(area_id))

@app.route("/add_users/<int:id>")
def add_users(id):
    return render_template("add_users.html", id = id)


@app.route("/add", methods=["POST"])
def add():
    username = request.form["username"]
    if username == "" or username == None:
        return render_template("error.html", message = "Please specify a valid username")
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    name = result.fetchone()
    if name == None or name == "":
        return render_template("error.html", message = "No specified user found")
    message_area_id = request.form["id"]
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    if users.check_rights(user_id, message_area_id):
        return render_template("add_users.html", id=message_area_id, message="The user already has access")
    areas.give_accessrights(message_area_id, user_id)
    return render_template("add_users.html", id = message_area_id)
