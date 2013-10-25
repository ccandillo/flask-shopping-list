import flask
import flask.views
import functools

from models import *
from extensions import db


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('index'))
    return wrapper


class ShoppingListView(flask.views.MethodView):
    @login_required
    def get(self):
        shopping_list = ShoppingList.query.first()

        if shopping_list is None:
            db.session.add(ShoppingList())
            db.session.commit()
        return flask.render_template('shoppingList.html', shoppingList=shopping_list)


class AddItemView(flask.views.MethodView):
    @login_required
    def post(self):
        item = ShoppingItem(flask.request.form['name'], ShoppingList.query.first())

        db.session.add(item)
        db.session.commit()
        flask.flash("Item added")

        return flask.redirect(flask.url_for('shoppingList'))


class DeleteItemView(flask.views.MethodView):
    @login_required
    def post(self):
        item = ShoppingItem.query.filter_by(id=flask.request.form['id']).first()

        db.session.delete(item)
        db.session.commit()

        flask.flash("Item deleted")
        return flask.redirect(flask.url_for('shoppingList'))


class CheckItemView(flask.views.MethodView):
    @login_required
    def post(self):
        item = ShoppingItem.query.filter_by(id=flask.request.form['id']).first()
        item.checked = True
        db.session.commit()
        flask.flash("Item checked")
        return flask.redirect(flask.url_for('shoppingList'))