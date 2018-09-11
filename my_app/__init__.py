import datetime
import json
from os.path import abspath
from os.path import dirname
from os.path import realpath

import ccy
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Markup
from redis import Redis

# from my_app.product.views import product_blueprint

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = realpath('.') + '/my_app/static/uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = 'some_random_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
redis = Redis(host='alpine')
# Restless
manager = APIManager(app, flask_sqlalchemy_db=db)
# Restful
api = Api(app)
# app.config['MONGODB_SETTINGS'] = {'DB': 'my_catalog', 'HOST': 'alpine'}
# db_mongo = MongoEngine(app)
# instance_path = dirname(dirname(abspath(__file__))) + '/instance'
# Instance config
# app = Flask(__name__,
#             instance_path=instance_path,
#             instance_relative_config=True)
# app.config.from_pyfile('config.cfg', silent=True)
# Custom static
# app = Flask(
#     __name__,
#     static_url_path='/otherstatic',
#     static_folder='static'
# )
# Class config
# app.config.from_object('config.DevelopmentConfig')
# app.register_blueprint(product_blueprint)
from my_app.auth.views import auth
from my_app.catalog.views import catalog
app.register_blueprint(auth)
# app.register_blueprint(catalog)

db.create_all()


class ConfigEncoder(json.JSONEncoder):
    def default(self, config_obj):  # pylint: disable=E0202
        if isinstance(config_obj, datetime.datetime):
            return config_obj.strftime('%Y-%m-%d %H:%I:%S')
        if isinstance(config_obj, datetime.time):
            return config_obj.strftime('%H:%I:%S')
        if isinstance(config_obj, datetime.timedelta):
            return config_obj.total_seconds()
        return super.default(self, config_obj)


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def from_now(self):
        return self.render("fromNow()")


app.jinja_env.globals['datetime'] = datetime
app.jinja_env.globals['momentjs'] = momentjs


@app.route('/logo')
def logo():
    url = url_for('static', filename='images/logo.png')
    return '<img src="{}">'.format(url)


@app.route('/config')
def config():
    pre_config = dict(app.config)
    config = dict()
    for key, value in pre_config.items():
        config[key] = value
    return json.dumps(config,
                      cls=ConfigEncoder,
                      separators=(',<br>', ':'),
                      sort_keys=True)


@app.template_filter('format_currency')
def format_currency_filter(amount):
    currency_code = ccy.countryccy(request.accept_languages.best[-2:])
    return '{} {}'.format(currency_code, amount)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
