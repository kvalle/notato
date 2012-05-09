from flask import Flask
from notato import config
app = Flask(__name__)
app.config.from_object(config)
import notato.views
