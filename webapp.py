from flask import Flask


app = Flask(__name__)


app.config.update(dict(
    DEBUG=True
))


@app.route('/', methods=['GET'])
def login():
    return 'Hello world', 200


if __name__ == '__main__':
    app.run()
