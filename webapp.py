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
    session_auth = SessionAuthentication(session)
    if session_auth.is_authenticated():
        return redirect('/cv')
    return render_template('login.html')


@app.route('/auth')
@consumes('application/json')
def auth():
    basic_auth = RequestBasicAuth(request.authorization)
    session_auth = SessionAuthentication(session)
    if not basic_auth.is_credentials_given():
        return unauthorized()
    campus_net_client.authenticate(basic_auth.username, basic_auth.password)
    if campus_net_client.is_authenticated():
        session_auth.authenticate(
            basic_auth.username,
            campus_net_client.auth_token
        )
        return '', 200
    else:
        return unauthorized()


@app.route('/cv')
def cv_page():
    session_auth = SessionAuthentication(session)
    if not session_auth.is_authenticated():
        return authenticate()
    campus_net_client.authenticate_with_token(
        session_auth.student_id,
        session_auth.auth_token
    )
    return render_template('cv.html', user=campus_net_client.user())


def unauthorized():
    return 'Unauthorized', 401


def authenticate():
    return redirect('/')


class SessionAuthentication(object):
    def __init__(self, session_dict):
        self.session_dict = session_dict

    def is_authenticated(self):
        return self.student_id is not None and self.auth_token is not None

    def authenticate(self, student_id, auth_token):
        session['student_id'] = student_id
        session['auth_token'] = auth_token

    @property
    def student_id(self):
        return session.get('student_id')

    @property
    def auth_token(self):
        return session.get('auth_token')


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
