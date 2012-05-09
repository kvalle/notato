from functools import wraps
from flask import Flask, request, Response, render_template

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    with open('storage/note', 'w') as note:
        if request.method == 'POST':
            text = request.form['note']
            note.write(text)
        else:
            text = note.read()
    return render_template('index.html', text=text)

if __name__ == "__main__":
    app.run(debug=True)
