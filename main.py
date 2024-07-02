# Main file
# import needed libaries
from flask import (
    Flask,
    render_template
)
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import logging

class Base(DeclarativeBase):
    pass

# initiate some stuff for the app
app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Flask@localhost/users'
db.init_app(app)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column(unique=True)

def test_add(id, name, email, password):
    user = User(id=id, name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

def create_db_all():
    with app.app_context():
        db.create_all()

# define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# define the route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        test_add(1, 'Seb', 'seb@seb.seb', 'Password')
        return 'it worked'
    except error as e:
        print(e)
        return 'There was an error'

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
    app.run(debug=True, port=80, host='0.0.0.0')
