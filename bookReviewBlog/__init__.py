import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# ###################################
# ##        DATABASE SETUP         ##
# ###################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

###################################
##             LOGIN             ##
###################################
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'users.login'

###################################
##             PAGES             ##
###################################
from bookReviewBlog.core.views import core
app.register_blueprint(core)

from bookReviewBlog.errorPages.handlers import error_pages
app.register_blueprint(error_pages)

from bookReviewBlog.users.views import users
app.register_blueprint(users)

from bookReviewBlog.bookPosts.views import bookPosts
app.register_blueprint(bookPosts)