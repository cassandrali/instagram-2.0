from instagram2 import app, db
from models import Post
from flask import render_template, request, redirect, url_for, jsonify, json, flash
from werkzeug import secure_filename
import os
from objectdetection import *
from collections import OrderedDict

'''route decorators, root page'''
@app.route("/")
def index():
	posts = Post.query.all()

	return render_template('layout.html', posts=posts)

# allow pictuers only
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
	# check if the post request has the file part
	if 'inputFile' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['inputFile']
	# if user doesa not select file, browser also
	# submit a empty part without filename
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		''' secure_filename: never trust user input '''

		# saves image to statc/images folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))) # save to static/images

		add_to_database(file)

		return redirect(url_for('index'))

# endpoint to delete an image 
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('index'))

def add_to_database(file):
	# add FILEPATH, CAPTION, and TAGS to database
	imagepath = 'images/' + file.filename

	# caption
	caption = request.form['caption']

	# tags
	absolute_image_path = '/Users/admin/Documents/instagramML/instagram2/static/images/' + file.filename
	image = Image.open(absolute_image_path)
	image_np = load_image_into_numpy_array(image)
	output_dict = run_inference_for_single_image(image_np, detection_graph)

	tags = []
	for j in range(len(output_dict['detection_classes'])):
		if (output_dict['detection_scores'][j] > 0.5):
			tags.append("#" + category_index.get(output_dict['detection_classes'][j]).get('name'))

	unique_tags = list(OrderedDict.fromkeys(tags).keys())

	tags = ''
	for tag in unique_tags:
		tags += tag + " "

	# add to database
	post = Post(imagepath=imagepath, caption=caption, tags=tags)
	db.session.add(post)
	db.session.commit()

# returns JSON of all image posts
# @app.route('/api/posts')
# def retrieve_images():
# 	return json.dumps([p.as_dict() for p in Post.query.all()][::-1])
