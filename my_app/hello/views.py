from my_app import app
from my_app.hello.models import MESSAGESS


@app.route('/')
@app.route('/hello')
def hello_world():
    return MESSAGESS['default']


@app.route('/show/<key>')
def get_message(key):
    return MESSAGESS.get(key, '{} not found!'.format(key))


@app.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    MESSAGESS[key] = message
    return '{} Added/Updated'.format(key)
