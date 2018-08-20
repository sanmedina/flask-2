from flask import Flask
from flask import url_for

from my_app.hello.views import hello

app = Flask(__name__)
# Custom static
# app = Flask(
#     __name__,
#     static_url_path='/otherstatic',
#     static_folder='static'
# )
app.register_blueprint(hello)

@app.route('/logo')
def logo():
    url = url_for('static', filename='images/logo.png')
    return '<img src="{}">'.format(url)
