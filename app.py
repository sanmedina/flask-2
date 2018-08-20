from flask import Flask

app = Flask(__name__)
# Class config
app.config.from_object('config.DevelopmentConfig')


@app.route('/')
def hello_word():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run()
