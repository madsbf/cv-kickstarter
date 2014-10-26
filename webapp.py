import sys

sys.path.append('cnapi')

import os
from flask import Flask, render_template, request, session, redirect
from flask_negotiate import consumes
from cnapi import CampusNetApi

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

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
    api = CampusNetApi(
        'StudyPlanner3000',
        '03157abb-4cb1-47c3-8b52-cdad0f82e78a',
        auth.username
    )
    api.authenticate(auth.password)
    if api.is_authenticated():
        session['student_id'] = auth.username
        session['auth_token'] = api.auth_token
        return '', 200
    else:
        return unauthorized()


@app.route('/cv')
def cv_page():
    if 'auth_token' not in session or 'student_id' not in session:
        return authenticate()
    api = CampusNetApi(
        'StudyPlanner3000',
        '03157abb-4cb1-47c3-8b52-cdad0f82e78a',
        session['student_id'],
        session['auth_token']
    )
    return render_template('cv.html', user=api.user())


def unauthorized():
    return 'Unauthorized', 401


def authenticate():
    return redirect('/')


if __name__ == '__main__':
    app.run()
