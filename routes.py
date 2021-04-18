from app import app
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv


from db import db
import users
#app.secret_key = getenv("SECRET_KEY")



#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

#db = SQLAlchemy(app)



@app.route("/po")
def po():
        return "Etusivu! Kiva nähdä!"



@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"


@app.route("/test")
def test():
    content = ""
    for i in range(1,101):
        content += str(i)+" "
    return content

@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)



@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html",name=request.form["name"])



@app.route("/")
def index():
    return render_template("index.html")
    return redirect("/listingredients")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/listingredients")
def listingredients():
    result = db.session.execute("SELECT COUNT(*) FROM ingredients")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT ingredient FROM ingredients")
    ingredients = result.fetchall()
    return render_template("listingredients.html", count=count, ingredients=ingredients)

@app.route("/newingredient")
def newingredient():
    result = db.session.execute("select id, name from measureunit")
    units = result.fetchall()
    return render_template("newingredient.html", units = units)

@app.route("/sendingredient", methods=["POST"])
def sendingredient():
    ingredient = request.form["ingredient"]
    price = request.form["price"]
    amount = request.form["amount"]
    unit = request.form["unitradio"]
    sql = "INSERT INTO ingredients (ingredient, price, amount, measureunit_id) VALUES (:ingredient, :price, :amount, :unit)"
    db.session.execute(sql, {"ingredient":ingredient, "price":price, "amount":amount, "unit":unit })
    db.session.commit()
    return redirect("/listingredients")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    error_message = users.login(username, password)
    if error_message == "":
        return redirect("/")
    elif error_message == "No such user":
        users.register(username, password)
    else:
        return render_template("index.html", error=error_message)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")