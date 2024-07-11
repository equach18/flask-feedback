from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """form for registrating a new user"""
    username = StringField("Username", validators=[InputRequired(message="Must include username."), Length(max=20, message="Username has a max of 20 characters.")])
    password = PasswordField("Password", validators=[InputRequired(message="Must include password.")])
    email = StringField("Email", validators=[InputRequired(message="Must include email."), Length(max=50, message="Email has a a max of 50 characters.")])
    first_name = StringField("First Name",validators=[InputRequired(message="Must include first name."), Length(max=30)])
    last_name = StringField("Last Name",validators=[InputRequired(message="Must include last name."),Length(max=30, message="Last name has a max of 30 characters.")])
    
class LoginForm(FlaskForm):
    """form for user to login"""
    username = StringField("Username", validators=[InputRequired(message="Must include username"), Length(max=20, message="Username has a max of 20 characters.")])
    password = PasswordField("Password", validators=[InputRequired(message="Must include password.")])
    
class FeedbackForm(FlaskForm):
    """form for new and editing feedback"""
    title = StringField("Title", validators=[InputRequired(message="Must include title"), Length(max=100)])
    content = TextAreaField("Content", validators=[InputRequired(message="Must include content")])
    
