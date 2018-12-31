from instagram2 import app, db
from forms import LoginForm, RegisterForm
from models import Post, Tag
from flask import render_template, request, redirect, url_for, jsonify, json, flash
from werkzeug import secure_filename
import os
from objectdetection import *
from collections import OrderedDict

@app.route("/")
@app.route("/home")
def index():
	posts = Post.query.all()

	return render_template('layout.html', posts=posts)

@app.route('/upload', methods=['POST'])
def upload():
	# check if the post request has the file part
	if 'inputFile' not in request.files:
		flash('No file input')
		return redirect(url_for('index'))
	file = request.files['inputFile']
	# if user does not select file, browser also
	# submit a empty part without filename
	if file.filename == '':
		flash('No selected file')
		return redirect(url_for('index'))
	if file and allowed_file(file.filename):
		path = 'images/' + file.filename

		# if image already exists - avoid duplicate uploads 
		if Post.query.filter_by(imagepath=path).first() != None:
			flash('Image is already in feed')
			return redirect(url_for('index'))

		# saves image to static/images folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))) # save to static/images

		add_to_database(file)

		return redirect(url_for('index'))

# endpoint to delete an image 
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
	post = Post.query.get(id) #TODO: DELETE CORRESPONDING TAGS

	delete_tags(post)

	db.session.delete(post) # deletes the post
	db.session.commit()
	return redirect(url_for('index'))

# endpoint to edit an image's caption and tags
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
	# query for post to be edited 
	post = Post.query.get(id)

	delete_tags(post)

	# get new caption and tags 
	new_caption = request.form['caption']
	print('NEW CAPTION: ' + new_caption)
	new_tags = request.form['tags'] # assume that it's a string in the format #dog#cat#whatever
	print('NEW TAGS: ' + new_tags)
	new_tags = "".join(new_tags.split()) # remove all whitespace, string type
	print('NEW TAGS WITH WHITESPACE REMOVED: ' + new_tags)
	new_tag_list = new_tags.split('#')

	for new_tag in new_tag_list:
		print('TAG IN NEW TAG LIST: ' + new_tag)
		if new_tag:
			print (new_tag + ' IS NOT EMPTY')
			new_tag_object = Tag.query.filter_by(name=new_tag).first()
			if new_tag_object == None:
				new_tag_object = Tag(name=new_tag)
				db.session.add(new_tag_object)
				print("DB DOES NOT CONTAIN " + new_tag + ". ADD IT TO DB")

			new_tag_object.owners.append(post) # associate each NEW tag with the post 

	# update post's caption in database 
	post.caption = new_caption

	db.session.commit()

	return redirect(url_for('index'))

@app.route("/<tag_name>")
def display_posts_with_specified_tag(tag_name):
	posts = Tag.query.filter_by(name=tag_name).first().owners
	return render_template('layout.html', posts=posts, tag_name_header=tag_name)

@app.route("/login")
def login():
	form = LoginForm()

	if form.validate_on_submit():
		return render_template('login.html', form=form) # PLACEHOLDER

	return render_template('login.html', form=form)

@app.route("/register")
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		return render_template('login.html', form=form) #PLACEHOLDER

	return render_template('register.html', form=form)

# allow images only
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_to_database(file):
	# add post to database
	imagepath = 'images/' + file.filename
	caption = request.form['caption']
	post = Post(imagepath=imagepath, caption=caption)
	db.session.add(post)

	# get tags using object detection model
	absolute_image_path = '/Users/admin/Documents/instagramML/instagram2/static/images/' + file.filename
	image = Image.open(absolute_image_path)
	image_np = load_image_into_numpy_array(image)
	output_dict = run_inference_for_single_image(image_np, detection_graph)

	tags = []
	for j in range(len(output_dict['detection_classes'])):
		if (output_dict['detection_scores'][j] > 0.5):
			tags.append(category_index.get(output_dict['detection_classes'][j]).get('name'))

	unique_tags = list(OrderedDict.fromkeys(tags).keys())

	# add tags to database
	for tag in unique_tags:
		tag_object = Tag.query.filter_by(name=tag).first()
		
		if tag_object == None:
			print('TAG: ' + tag) 
			tag_object = Tag(name=tag)
			db.session.add(tag_object)

		tag_object.owners.append(post) # associate each tag with a post 

	db.session.commit()

# delete these 
def delete_tags(post):
	tags_to_be_deleted = post.tags.copy() #challenge 
	for i in range(len(tags_to_be_deleted)):
		tag_to_be_deleted = tags_to_be_deleted[i]
		tag_to_be_deleted.owners.remove(post) # remove association between Tag and Post
		if tag_to_be_deleted.owners.first() == None: # deletes Tag objects which have no posts
			db.session.delete(tag_to_be_deleted)
