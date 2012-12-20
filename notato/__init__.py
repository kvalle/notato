from flask import Flask, render_template, g
from notato.repo import MongoRepo
import config

app = Flask(__name__)
app.config.from_object(config)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.before_request
def before_request():
    database = app.config['DATABASE']
    g.repo = MongoRepo(database)

from notato.views import general
from notato.views import notes
from notato.views import files
