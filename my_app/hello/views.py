from flask import Blueprint

from my_app.hello.models import MESSAGESS

hello = Blueprint('hello', __name__)


@hello.route('/')
@hello.route('/hello')
def hello_world():
    return MESSAGESS['default']


@hello.route('/show/<key>')
def get_message(key):
    return MESSAGESS.get(key, '{} not found!'.format(key))


@hello.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    MESSAGESS[key] = message
    return '{} Added/Updated'.format(key)
