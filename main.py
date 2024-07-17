# Main file
# import needed libaries
import os
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request
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
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from argon2 import PasswordHasher

# initiate some stuff for the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Flask@localhost/users'
db.init_app(app)

# create the password hasher to hash the passwords. Uses argon2 hashing algorithim
ph = PasswordHasher()

def list_kanban_boards(user):
    id = user

# basically takes the users name, email and hashed password and enters it into the database
def add_user_to_db(name, email, password):
    user = User(UserName=name, email=email, UserPassword=password)
    db.session.add(user)
    db.session.commit()

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
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = query_user_database(email)
            if ph.verify(user.UserPassword, password):
                login_user(user)
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
    return render_template('board.html')

@app.route('/list-api/v1')
def list_api_v1():
    return 'This is where the apis live'

@app.route('/list-api/v1/create-board', methods=['POST'])
def create_board():
    encoded_boardname = request.get_data()
    boardname = encoded_boardname.decode('utf-8')
    list = TodoList(boardname)
    list.savelisttofile()
    return 'List Successfully Created', 204

# checks that this isn't trying to be called from another file
# and runs the Flask application.
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
