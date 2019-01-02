from instagram2 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# one user can have MANY posts
class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column('id', db.Integer, primary_key=True)
	username = db.Column(db.String(), unique=True, nullable=False)
	email = db.Column(db.String(), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	# sql alchemy will load the data as necessary in one go

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

# MANY TO MANY RELATIONSHIP

# association table between Post and Tag 
assoc = db.Table('assoc',
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
	)

# one post can have MANY tags
class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column('id', db.Integer, primary_key=True)
	imagepath = db.Column('imagepath', db.Text, nullable=False) # images/ + filename
	caption = db.Column('caption', db.Text, nullable=False)
	tags = db.relationship('Tag', secondary=assoc, backref=db.backref('owners', lazy='dynamic')) # owner of tag - pseudo column
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # id of user who posts the post 
	#user = db.relationship('User')

# each tag can have MANY posts
class Tag(db.Model):
	__table__name = 'tag'
	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.Text)


# NOTE TO SELF 
# add all posts to table 
# add all tags to table 
# tag.owners.append(post1) updating the model
# tag.owners.append(post2)
