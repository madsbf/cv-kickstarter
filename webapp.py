import sys

sys.path.append('cnapi')

import os
from flask import Flask, render_template, request, session, redirect
from flask_negotiate import consumes
from cnapi import CampusNetApi
from flask_sslify import SSLify

app = Flask(__name__)
env = os.environ
app.secret_key = env['SECRET_KEY']
campus_net_client = CampusNetApi(
    env['CAMPUS_NET_APP_NAME'],
    env['CAMPUS_NET_APP_TOKEN']
)

# Enforce https on Heroku
if 'DYNO' in os.environ:
    sslify = SSLify(app)

app.config.update(dict(
    DEBUG=True,
))


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/auth')
@consumes('application/json')
def auth():
    auth = request.authorization
    if auth is None:
        return unauthorized()
    campus_net_client.authenticate(auth.password)
    if campus_net_client.is_authenticated():
        session['student_id'] = auth.username
        session['auth_token'] = campus_net_client.auth_token
        return '', 200
    else:
        return unauthorized()


@app.route('/cv')
def cv_page():
    if 'auth_token' not in session or 'student_id' not in session:
        return authenticate()
    campus_net_client.authenticate_with_token(
        session['student_id'],
        session['auth_token']
    )
    return render_template('cv.html', user=campus_net_client.user())


def unauthorized():
    return 'Unauthorized', 401


def authenticate():
    return redirect('/')


if __name__ == '__main__':
    app.run()
