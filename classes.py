from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Base(DeclarativeBase):
    pass

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

class TodoList:
    def __init__(self):
        self.lists = {}
    
    def createlist(self, listname):
        self.lists[listname] = []
    
    def addtolist(self, listname, item):
        self.lists[listname] = [item]
    
    def listitems(self, listname):
        print(self.lists[listname])

