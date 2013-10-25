import flask
import flask.views
import functools
from flask.ext.sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.secret_key = "lepetitbonhomeenmousse"
users = {'test':'test'}

## DATABASES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


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

db.init_app(app)
db.create_all()

## MISC
def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('index'))
    return wrapper


## VIEWS
class MainView(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    
    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'password']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        password = flask.request.form['password']
        if username in users and users[username] == password:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))


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


## Routing
app.add_url_rule('/',
                 view_func=MainView.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/shopping/list/',
                 view_func=ShoppingListView.as_view('shoppingList'),
                 methods=["GET"])
app.add_url_rule('/shopping/add/',
                 view_func=AddItemView.as_view('addItem'),
                 methods=["POST"])
app.add_url_rule('/shopping/delete/',
                 view_func=DeleteItemView.as_view('deleteItem'),
                 methods=["POST"])
app.add_url_rule('/shopping/check/',
                 view_func=CheckItemView.as_view('checkItem'),
                 methods=["POST"])

app.debug = True
app.run()