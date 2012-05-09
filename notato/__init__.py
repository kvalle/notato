from flask import Flask
app = Flask(__name__)

SECRET_KEY = 'dev_key'
app.secret_key = SECRET_KEY

import notato.views
