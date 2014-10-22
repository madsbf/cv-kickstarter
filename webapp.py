import os
from flask import Flask


app = Flask(__name__)


app.config.update(dict(
    host='0.0.0.0',
    debug=True,
    port=int(os.environ.get('PORT', 5000))
))


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
