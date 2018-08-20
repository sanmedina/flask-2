import datetime
import json

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
# Class config
# app.config.from_object('config.DevelopmentConfig')
app.register_blueprint(hello)


class ConfigEncoder(json.JSONEncoder):
    def default(self, config_obj):
        if isinstance(config_obj, datetime.datetime):
            return config_obj.strftime('%Y-%m-%d %H:%I:%S')
        if isinstance(config_obj, datetime.time):
            return config_obj.strftime('%H:%I:%S')
        if isinstance(config_obj, datetime.timedelta):
            return config_obj.total_seconds()
        return super.default(self, config_obj)


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
