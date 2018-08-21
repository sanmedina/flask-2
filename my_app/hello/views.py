from flask import Blueprint
from flask import render_template
from flask import request

from my_app.hello.models import MESSAGESS

hello = Blueprint('hello', __name__)


@hello.route('/')
@hello.route('/hello')
def hello_world():
    user = request.args.get('user', 'Shalabh')
    return render_template('index.html.j2', user=user)


@hello.route('/show/<key>')
def get_message(key):
    return MESSAGESS.get(key, '{} not found!'.format(key))


@hello.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    MESSAGESS[key] = message
    return '{} Added/Updated'.format(key)
