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
    if not basic_auth.is_credentials_given():
        return unauthorized()
    campus_net_client.authenticate(basic_auth.password)
    if campus_net_client.is_authenticated():
        session['student_id'] = basic_auth.username
        session['auth_token'] = campus_net_client.auth_token
        return '', 200
    else:
        return unauthorized()


@app.route('/cv')
def cv_page():
    if not is_authenticated_with_session():
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


@property
def basic_auth():
    return RequestBasicAuth(request.authorization)


def is_authenticated_with_session():
    return 'auth_token' in session or 'student_id' in session


class RequestBasicAuth(object):
    def __init__(self, request_authorization):
        self.request_authorization = request_authorization

    def is_credentials_given(self):
        return self.request_authorization is not None

    @property
    def username(self):
        return self.request_authorization.username

    @property
    def password(self):
        return self.request_authorization.password


if __name__ == '__main__':
    app.run()
