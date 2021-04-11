__version__ = "0.1.0"
__author__ = "Andreas Rabenstein"
__author_email__ = "andreas@rabenstein-page.de"

from flask import Flask

from .blueprints.cv.routes import blueprint as cv_blueprint

app = Flask(__name__)
app.register_blueprint(cv_blueprint, url_prefix="/cv")
