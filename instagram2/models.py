from instagram2 import db

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column('id', db.Integer, primary_key=True)

	imagepath = db.Column('imagepath', db.Text, nullable=False)
	caption = db.Column('caption', db.Text, nullable=False)
	tags = db.Column('tags', db.Text) # save as a string 

	def __repr__(self):
		return f"Post('{self.caption}')"