# Main file
# import needed libaries
import os
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    abort
)
from flask_login import (
    LoginManager, 
    login_required,
    current_user,
    logout_user,
    login_user
)
from classes import (
    User,
    Base,
    RegisterForm,
    LoginForm,
    TodoList
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_cors import CORS
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from argon2 import PasswordHasher
import json
import ast

# initiate some stuff for the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Flask@localhost/users'
db.init_app(app)
CORS(app)


# create the password hasher to hash the passwords. Uses argon2 hashing algorithim
ph = PasswordHasher()

def list_kanban_boards(user):
    id = user

# basically takes the users name, email and hashed password and enters it into the database
def add_user_to_db(name, email, password):
    user = User(UserName=name, email=email, UserPassword=password)
    db.session.add(user)
    db.session.commit()
    os.mkdir(f'users/{user.id}')

# query the database to see if the user exists
def query_user_database(email):
    return db.session.execute(db.select(User).filter_by(email=email)).scalar_one()

# define the login manager using flask_login to handle users loggning in and out
@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, int(user_id))
    return user

# define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# define the route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # grab the login form
    form = LoginForm()

    if form.validate_on_submit():
        # store the form data in some variables
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        # try to query the user database for the user
        # if that user exists then check the users password hash against the 
        # entered password
        # if that succeeds login the user
        # if something goes wrong print the error, will add an abort 500 later
        try:
            user = query_user_database(email)
            if ph.verify(user.UserPassword, password):
                login_user(user, remember=remember)
                return redirect(url_for('index'))
        except Exception as e:
            print(e)

    return render_template('login.html', form=form)

# define a route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    # if the form is submitted and posted over http (or https) take the users data,
    # hash the password then add it to the database. 
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        unhashed_password = form.password.data
        
        password = ph.hash(unhashed_password)

        add_user_to_db(name, email, password)

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# uses flask login to pop the sessions to logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/board')
@login_required
def boards():
    user_id = current_user.id
    path = f'users/{user_id}'
    lists = os.listdir(path)
    return render_template('board.html', lists=lists, user_id=current_user.id)

@app.route('/list-api/v1')
def list_api_v1():
    return 'This is where the apis live'

@app.route('/list-api/v1/create-board', methods=['POST'])
def create_board():
    if current_user.is_authenticated == True:
        user_id = current_user.id
    encoded_boardname = request.get_data()
    boardname = encoded_boardname.decode('utf-8')
    list = TodoList(boardname)
    try:
        list.savelisttofile(user_id)
        return 'List Successfully Created', 204
    except Exception as e:
        print(e)
        abort(500)

@app.route('/list-api/v1/create-list', methods=['POST'])
def create_list():
    try:
        data = request.get_json()
        list = TodoList(data['SelectedList'])
        list.loadlistfromfile(data['UserId'])
        list.createlist(data['ListName'])
        list.savelisttofile(data['UserId'])
        return 'success', 204
    except Exception as e:
        print(e)
        return 'failed', 500

@app.route('/list-api/v1/additem', methods=['POST'])
def additem():
    data = request.get_json()
    list = TodoList(data['SelectedList'])
    list.loadlistfromfile(data['UserId'])
    list.additem(data['currentList'], data['item'])
    list.savelisttofile(data['UserId'])
    return 'success', 204

@app.route('/list-api/v1/get-list', methods=['POST'])
def getlist():
    liststuff = request.get_data().decode('utf-8')
    liststuff = ast.literal_eval(liststuff)
    list = TodoList(liststuff[0])
    list.loadlistfromfile(liststuff[1])
    lists = list.listsublists()
    lists = json.dumps(lists)
    return lists, 200

@app.route('/list-api/v1/removeitem', methods=['POST'])
def remitem():
    data = request.get_json()
    list = TodoList(data['SelectedList'])
    list.loadlistfromfile(data['UserId'])
    list.removeitem(data['currentList'], data['item'])
    list.savelisttofile(data['UserId'])
    return 'success', 204


# checks that this isn't trying to be called from another file
# and runs the Flask application.
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
