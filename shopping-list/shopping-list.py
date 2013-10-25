import flask
import flask.views

from views import *
from extensions import db


app = flask.Flask(__name__)
app.secret_key = "lepetitbonhomeenmousse"
users = {'test': 'test'}

## DATABASES
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)
db.app = app
db.create_all()


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