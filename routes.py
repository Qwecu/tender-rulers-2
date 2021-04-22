from app import app
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv


from db import db
import users
import random
import math
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
    result = db.session.execute("\
        select CONCAT(ingredient, ' ', price::text, ' € (', priceperunit::NUMERIC(6, 2)::text, ' €/', measureunit.name, ')') \
        from ingredients \
        left join measureunit on measureunit.id = ingredients.measureunit_id \
        order by ingredient")
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

@app.route("/generaterecipe")
def generaterecipe():
    return render_template("generaterecipe.html")

@app.route("/generaterecipepost", methods=["POST"])
def generaterecipepost():
    budget = float(request.form["budget"])
    max_ingredient_amount = int(math.sqrt(random.random() * 80) + 1)
    #result = db.session.execute("SELECT COUNT(*) FROM ingredients")
    #count = result.fetchone()[0]
    strjoin = ""

    strj = "	INNER JOIN filter_ingredient a1 ON a1.ingredient_id = ingredients.id "

    stringsql = \
        "SELECT * " + \
        "FROM  ( " + \
        " SELECT DISTINCT 1 + trunc(random() *  " + \
        "   (select COUNT(*) from ingredients " + \
        strjoin + \
        "	) " + \
        " )::integer AS id " + \
        " FROM   generate_series(1, :max_ingredient_amount) g " + \
        " ) r " + \
        " JOIN    " + \
        "( " + \
        "select ROW_NUMBER () OVER (ORDER BY id) as id, ingredient, id as originalid, price from ingredients " + \
        strjoin + \
        ") validfoods " + \
        "USING (id); "
    
    recipe = db.session.execute(stringsql,{"max_ingredient_amount": max_ingredient_amount})

    
    weights = []
    weightsum = 0

    rowcount = recipe.rowcount

    #return str(rowcount)


    
    for r in range(rowcount):
        weight = random.randint(1,10)
        weights.append(weight)
        weightsum += weight

    modifier = 1 / (weightsum * 1.0 / budget)

    totalprice = 0
    cheapestindex = 0
    cheapestprice = 0
    weighedrecipe = []

    #return "weightsum " + str(weightsum) + " reco " + str(reco) + " modifier " + str(modifier)
    test = "TEST: "

    currentindex = 0
    for food in recipe:
        if food[3] < cheapestprice or cheapestprice == 0:
            cheapestprice = food[3]
            cheapestindex = currentindex

        individualbudget = modifier * weights[currentindex]
        count = int(individualbudget / float(food[3]))
        totalprice += count * food[3]
        weighedrecipe.append([food[0], food[1], food[2], food[3], count])
        #test += (str(food[0]) + " " + str(food[1]) + " " + str(food[2]) + " " + str(food[3]) + " " + str(count) + "\n")


        currentindex = currentindex + 1
        
    #return test + " currentindex : " + str(currentindex)

    return render_template("showrecipe.html", items = weighedrecipe, totalprice = totalprice)
    #return str(ingredient_amount)