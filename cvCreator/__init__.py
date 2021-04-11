from flask import Flask

from . import __metadata__
from .blueprints.cv.routes import blueprint as cv_blueprint

app = Flask(__name__)
app.register_blueprint(cv_blueprint, url_prefix="/cv")

