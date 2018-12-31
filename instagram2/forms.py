from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

# class PostForm(FlaskForm):
# 	caption = TextField('caption')
# 	url = TextField('url')

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	email = StringField('email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])