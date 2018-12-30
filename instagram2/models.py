from instagram2 import db

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

	def __repr__(self):
		return f"Post('{self.caption}')"

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
