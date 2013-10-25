
from extensions import db


class ShoppingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    checked = db.Column(db.Integer(1))
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'))
    shopping_list = db.relationship('ShoppingList', backref=db.backref('item_list', lazy='dynamic'))

    def __init__(self, name, shopping_list):
        self.name = name
        self.checked = False
        self.shopping_list = shopping_list

    def __repr__(self):
        return '<Item %r>' % self.name


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<ShoppingList %r>' % self.id
