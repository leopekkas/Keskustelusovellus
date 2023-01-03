from app import app
from db import db
from flask import render_template, request, redirect, session
import messages, users

@app.route("/")
def index():
    list = messages.get_list()
    sql = "SELECT id, name FROM message_areas"
    result = db.session.execute(sql)
    areas = result.fetchall()
    return render_template("index.html", count=len(list), messages=list, message_areas=areas)

@app.route("/new")
def new():
    return render_template("new.html")

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
