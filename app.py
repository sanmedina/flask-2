from flask import Flask

app = Flask(__name__)
# Custom static
# app = Flask(
#     __name__,
#     static_url_path='/otherstatic',
#     static_folder='static'
# )
# Class config
app.config.from_object('config.DevelopmentConfig')


@app.route('/')
def hello_word():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run()
