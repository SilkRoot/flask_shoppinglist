from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import timedelta

app = Flask(__name__)
DB_NAME = "database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# db.init_app(app)
# db = SQLAlchemy()
db = SQLAlchemy(app)


#class Element(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    element = db.Column(db.String(1000))

#    def __init__(self, id, element):
#        self.id = id
#        self.element = element


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(1000))
    type = db.Column(db.String(1000))

    def __init__(self, id, item, type):
        self.id = id
        self.item = item
        self.type = type

class Shoppinglist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(1000))
    amount = db.Column(db.Integer)
    item_ref = db.Column(db.Integer)

    def __init__(self, item, amount, item_ref):
        self.item = item
        self.amount = amount
        self.item_ref = item_ref


foo = [
    Item(1001, "Apfel", "Obst"),
    Item(1002, "Avocado", "Obst"),
    Item(1003, "Banane", "Obst"),
    Item(1004, "Birne", "Obst"),
    Item(2001, "Lauch", "Gemüse"),
    Item(2002, "Mais", "Gemüse"),
    Item(2003, "Karotte", "Gemüse"),
    Item(2004, "Sellerie", "Gemüse"),
    Item(3001, "Brot", "Gebäck"),
    Item(3002, "Croissant", "Gebäck"),
    Item(3003, "Waffeln", "Gebäck"),
    Item(3004, "Brötchen", "Gebäck"),
    Item(4001, "Frischmilch", "Molkereiprodukte"),
    Item(4001, "Brie", "Molkereiprodukte"),
    Item(4001, "Käse", "Molkereiprodukte"),
    Item(4001, "Butter", "Molkereiprodukte"),
    Item(5001, "Lachs", "Fleisch und Fisch"),
    Item(5002, "Bratwurst", "Fleisch und Fisch"),
    Item(5003, "Hering", "Fleisch und Fisch"),
    Item(5004, "Bacon", "Fleisch und Fisch"),
    Item(6001, "Nori", "Zutaten und Gewürze"),
    Item(6002, "Pfeffer", "Zutaten und Gewürze"),
    Item(6003, "Salz", "Zutaten und Gewürze"),
    Item(6004, "Rosmarin", "Zutaten und Gewürze"),
    Item(7001, "Bandnudeln", "Getreideprodukte"),
    Item(7002, "Lasagneplatten", "Getreideprodukte"),
    Item(7003, "Weizenmehl", "Getreideprodukte"),
    Item(7004, "Tofu", "Getreideprodukte"),
]

for i in foo:
    print(i)
    if Item.query.filter_by(id=i.id).first() is None:
        db.session.add(i)
db.session.commit()

#    date = db.Column(db.DateTime(timezone=True), default=func.now())
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route("/")
def home():
    #	return "Hello! This is the home page <h1>HELLO</h1>"
    items = ["Apfel", "Birne", "Banane"]
    return render_template("index.html", items=items)


@app.route("/test")
def test():
    return render_template("test.html", name="test")


@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        user = request.form["nm"]
        print(user)
        return redirect(url_for("test"))
    else:
        return render_template("form.html")


#@app.route("/write_db", methods=["POST", "GET"])
#def write_db():
#    elements = []
#    if request.method == "POST":
#        # write to database
#        new_element = Element(element=request.form["element"], id=request.form["id"])
#        db.session.add(new_element)
#        db.session.commit()
#        elements = Element.query.filter_by().all()
#        print(elements)
#        return render_template("write_db.html", elements=elements)
#    else:
#        test = Element.query.filter_by().all()
#        for i in test:
#            print(i.element)
#        elements = Element.query.filter_by().all()
#        return render_template("write_db.html", elements=elements)

@app.route("/add_food", methods=["POST", "GET"])
def add_food():
    shoppinglist = Shoppinglist.query.filter_by().all()
    if request.method == "POST":
        print(request.args.get('hidden_element'))
        print(request.form)
        print(request.get_json())
        if 'submit_button_shoppinglist' in request.form:
            print("pressed button from Shoppinglist and deleting it: " + request.form['submit_button_shoppinglist'])
            Shoppinglist.query.filter_by(item=request.form['submit_button_shoppinglist']).delete()
            db.session.commit()

        if 'submit_button_itemlist' in request.form:
            print("pressed button from Itemlist: " + request.form['submit_button_itemlist'])
            shoppinglist_element = Shoppinglist(request.form['submit_button_itemlist'], 1, 1)
            db.session.add(shoppinglist_element)
            db.session.commit()
        items = Item.query.filter_by().all()
        shoppinglist = Shoppinglist.query.filter_by().all()
        return render_template("add_food.html", items=items, shoppinglist=shoppinglist)
    else:
        items = Item.query.filter_by().all()
        shoppinglist = Shoppinglist.query.filter_by().all()
        return render_template("add_food.html", items=items, shoppinglist=shoppinglist)




if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
# app.run()
