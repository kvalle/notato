from flask import Flask
from flask.ext import shelve
import config

app = Flask(__name__)
app.config.from_object(config)
shelve.init_app(app)

import notato.views
