from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from models import User

# class PostForm(FlaskForm):
# 	caption = TextField('caption')
# 	url = TextField('url')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
	submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
	email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=40)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
	submit = SubmitField('Register')

	def validate_username(self, username):

		user = User.query.filter_by(username=username.data).first()

		if user:
			print('USERNAME ALREADY TAKEN')
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()

		if user:
			print('EMAIL ALREADY TAKEN')
			raise ValidationError('That email is taken. Please choose a different one.')