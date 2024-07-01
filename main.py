# Main file
# import needed libaries
from flask import (
    Flask,
    render_template
)
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import logging

class Base(DeclarativeBase):
    pass

# initiate some stuff for the app
app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Flask@localhost/users/users'
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: mapped[str] = mapped_column()
    password: mapped[str] = mapped_column(unique=True)

# define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# define the route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

# define a route for the register page
@app.route('/register')
def register():
    pass

# define a page for the logout page
@app.route('/logout')
def logout():
    pass

# if run as a script, run the server
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
