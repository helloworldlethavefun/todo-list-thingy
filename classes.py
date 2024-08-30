from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import json
import os

choices = ['Remember Me?']

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
    remember = BooleanField('Remember Me?')
    submit = SubmitField()

class TodoList:
    def __init__(self, parentlistname):
        self.lists = {}
        self.filename = parentlistname + '.json'
    
    def createlist(self, listname):
      self.lists[listname] = []
    
    def additem(self, listname, item):
        self.lists[listname].append(item)
    
    def listitems(self, listname):
        print(self.lists[listname])

    def listsublists(self):
        print(self.lists.keys())

    def removeitem(self, listname, item):
        if item in self.lists[listname]:
            self.lists[listname].remove(item)

    def moveitem(self, list1, item, list2):
        if item in self.lists[list1]:
            self.lists[list2].append(item)
            self.removeitem(list1, item)

    def savelisttofile(self, user_id):
        jsonList = json.dumps(self.lists)
        user_directory = f'users/{user_id}'
        file_path = os.path.join(user_directory, self.filename)
        with open(file_path, 'w') as file:
            file.write(jsonList)
            file.close

    def loadlistfromfile(self):
        with open(self.filename, 'r') as file:
            jsonList = file.read()
            self.lists = json.loads(jsonList)
