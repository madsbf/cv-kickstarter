from flask import Flask


app = Flask(__name__)


app.config.update(dict(
    debug=True,
))


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
