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


class FoodType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String(1000))

    def __init__(self, id, food_type):
        self.id = id
        self.food_type = food_type


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(1000))
    food_type_id = db.Column(db.Integer)

    def __init__(self, id, item, food_type_id):
        self.id = id
        self.item = item
        self.food_type_id = food_type_id


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(1000))
    amount = db.Column(db.Integer)
    comment = db.Column(db.String(1000))
    food_item_id = db.Column(db.Integer)

    def __init__(self, item, amount, comment, food_item_id):
        self.item = item
        self.amount = amount
        self.comment = comment
        self.food_item_id = food_item_id


foo = [
    FoodItem(1001, "Apfel", 1),
    FoodItem(1002, "Avocado", 1),
    FoodItem(1003, "Banane", 1),
    FoodItem(1004, "Birne", 1),
    FoodItem(2001, "Lauch", 2),
    FoodItem(2002, "Mais", 2),
    FoodItem(2003, "Karotte", 2),
    FoodItem(2004, "Sellerie", 2),
    FoodItem(2005, "Brokkoli", 2),
    FoodItem(2006, "Champignons", 2),
    FoodItem(2007, "Cherrytomaten", 2),
    FoodItem(2008, "Gurke", 2),
    FoodItem(2009, "Kürbis", 2),
    FoodItem(2010, "Grapefruit", 2),
    FoodItem(3001, "Brot", 3),
    FoodItem(3002, "Croissant", 3),
    FoodItem(3003, "Waffeln", 3),
    FoodItem(3004, "Brötchen", 3),
    FoodItem(4001, "Frischmilch", 4),
    FoodItem(4001, "Brie", 4),
    FoodItem(4001, "Käse", 4),
    FoodItem(4001, "Butter", 4),
    FoodItem(5001, "Lachs", 5),
    FoodItem(5002, "Bratwurst", 5),
    FoodItem(5003, "Hering", 5),
    FoodItem(5004, "Bacon", 5),
    FoodItem(6001, "Nori", 6),
    FoodItem(6002, "Pfeffer", 6),
    FoodItem(6003, "Salz", 6),
    FoodItem(6004, "Rosmarin", 6),
    FoodItem(7001, "Bandnudeln", 7),
    FoodItem(7002, "Lasagneplatten", 7),
    FoodItem(7003, "Weizenmehl", 7),
    FoodItem(7004, "Tofu", 7),
]

bar = [
    FoodType(1, "Obst"),
    FoodType(2, "Gemüse"),
    FoodType(3, "Gebäck"),
    FoodType(4, "Molkereiprodukte"),
    FoodType(5, "Fleisch und Fisch"),
    FoodType(6, "Zutaten und Gewürze"),
    FoodType(7, "Getreideprodukte")
]

for i in foo:
    print(i)
    if FoodItem.query.filter_by(id=i.id).first() is None:
        db.session.add(i)
db.session.commit()

for i in bar:
    print(i)
    if FoodType.query.filter_by(id=i.id).first() is None:
        db.session.add(i)
db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_food", methods=["POST", "GET"])
def add_food():
    all_foodtype = FoodType.query.filter_by().all()
    all_fooditem = FoodItem.query.filter_by().all()
    if request.method == "POST":
        pressed_id = (list(request.form.keys()))[0]
        pressed_value = (list(request.form.values()))[0]
        print(f"ID of pressed button: {pressed_id}")
        print(f"Text of the pressed button: {pressed_value}")
        if pressed_id is not None:
            if ShoppingList.query.filter_by(food_item_id=pressed_id).first() \
                    or ShoppingList.query.filter_by(item=pressed_value).first():
                print("Element found in shoppinglist, pop it from shoppinglist")
                ShoppingList.query.filter_by(food_item_id=pressed_id).delete()
                ShoppingList.query.filter_by(item=pressed_value).delete()
                db.session.commit()
            else:
                print("Element was NOT found in shoppinglist, add it to shoppinglist")
                if FoodItem.query.filter_by(id=pressed_id).first():
                    food_id = pressed_id
                else:
                    food_id = None
                shoppinglist_element = ShoppingList(pressed_value, None, None, food_id)
                db.session.add(shoppinglist_element)
                db.session.commit()

        cur_shoppinglist = ShoppingList.query.filter_by().all()
        return render_template("add_food.html",
                               all_foodtype=all_foodtype,
                               all_fooditem=all_fooditem,
                               cur_shoppinglist=cur_shoppinglist)
    else:
        cur_shoppinglist = ShoppingList.query.filter_by().all()
        return render_template("add_food.html",
                               all_foodtype=all_foodtype,
                               all_fooditem=all_fooditem,
                               cur_shoppinglist=cur_shoppinglist)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
# app.run()
