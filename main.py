# Main file
# import needed libaries
import os
from flask import (
    Flask,
    render_template,
    url_for,
    redirect
)
from flask_login import (
    LoginManager, 
    UserMixin, 
    login_required,
    current_user,
    logout_user,
    login_user
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from argon2 import PasswordHasher

class Base(DeclarativeBase):
    pass

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

# define the user database as a class for flask to handle interacting with the database
# (adding/deleting users, checking passwords, emails etc)
class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    UserName: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    UserPassword: Mapped[str] = mapped_column(unique=True)

# define the form for the user to use to create an account.
class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    email = StringField('email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField()

# pretty much the same as the form defined above but for logging in.
# we will use an email for checking if the person has an account, hence why there is no name field.
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField()

# create a function for adding a user to the database
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
                print('user logged in')
                return redirect(url_for('test'))
            else:
                print('Your entered the wrong password')
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

@app.route('/test')
@login_required
def test():
    return f'Hello {current_user.UserName}!'

# define a page for the logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# checks that this isn't trying to be called from another file
# and runs the Flask application.
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
