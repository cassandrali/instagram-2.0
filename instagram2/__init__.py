'''where we initialize our application and bring together diff components'''
'''__init___ tells python that instagramML is a package'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# must import views AFTER the app in initialized 
from views import *