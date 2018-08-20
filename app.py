import os

from flask import Flask

# app = Flask(__name__)
# Custom static
# app = Flask(
#     __name__,
#     static_url_path='/otherstatic',
#     static_folder='static'
# )
# Class config
# app.config.from_object('config.DevelopmentConfig')
# Load from instance
app = Flask(__name__,
            instance_path=os.path.dirname(__file__) + '/instance',
            instance_relative_config=True)
app.config.from_pyfile('config.cfg')
# Supress error
# app.config.from_pyfile('config.cfg', silent=True)


@app.route('/')
def hello_word():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run()
