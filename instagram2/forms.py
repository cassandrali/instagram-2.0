from flask_wtf import FlaskForm
from wtforms import TextField

class PostForm(FlaskForm):
	caption = TextField('caption')
	url = TextField('url')