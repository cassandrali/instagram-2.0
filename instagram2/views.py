from instagram2 import app, db
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
		flash('No file part')
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
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('index'))

@app.route("/<tag_name>")
def display_posts_with_specified_tag(tag_name):
	posts = Tag.query.filter_by(name=tag_name).first().owners
	return render_template('layout.html', posts=posts, tag_name_header=tag_name)

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

# returns JSON of all image posts
# @app.route('/api/posts')
# def retrieve_images():
# 	return json.dumps([p.as_dict() for p in Post.query.all()][::-1])
