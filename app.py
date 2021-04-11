from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///lasse"
db = SQLAlchemy(app)


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
    result = db.session.execute("SELECT COUNT(*) FROM messages")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("index.html", count=count, messages=messages)

#@app.route("/listingredients")
#def listingredients():
#    result = db.session.execute("SELECT COUNT(*) FROM ingredients")
#    count = result.fetchone()[0]
#    result = db.session.execute("SELECT ingredient FROM ingredient")
#    ingredients = result.fetchall()
#    return render_template("listingredients.html", count=count, ingredients=ingredients)

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
