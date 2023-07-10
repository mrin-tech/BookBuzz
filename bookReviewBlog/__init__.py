from flask import Flask
app = Flask(__name__)

from bookReviewBlog.core.views import core
app.register_blueprint(core)

from bookReviewBlog.errorPages.handlers import error_pages
app.register_blueprint(error_pages)