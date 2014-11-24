import sys

sys.path.append('cv_kickstarter/lib')
sys.path.append('cv_kickstarter/view_objects')
sys.path.append('cv_kickstarter/models')
sys.path.append('cv_kickstarter')
sys.path.append('cnapi')
sys.path.append('job_searcher')

import os
from session_authentication import SessionAuthentication
from mongo_store import MongoStore
from user_cv_builder import UserCVBuilder
from flask import (Flask, render_template, request, session, redirect, jsonify,
                   Response)
from flask_negotiate import consumes
from cnapi import CampusNetApi
from flask_sslify import SSLify
from career_builder import CareerBuilder
from cv_kickstarter_config import CvKickstarterConfig

app = Flask(__name__)
config = CvKickstarterConfig(os.environ.get("CONFIG_FILE") or "app.cfg")

app.secret_key = config.secret_key()
campus_net_client = CampusNetApi(
    config.campus_net_app_name(),
    config.campus_net_app_token()
)
career_builder_key = config.career_builder_key()
go_key = config.go_key()

# Enforce https on Heroku
if 'DYNO' in os.environ:
    sslify = SSLify(app)

app.config.update(dict(
    DEBUG=True
))

mongo_store = MongoStore('cv_kickstarter', config.mongo_url())


@app.route('/')
def login():
    session_auth = SessionAuthentication(session)
    if session_auth.is_authenticated():
        return redirect('/cv')
    return render_template('login.html')


@app.route('/auth')
@consumes('application/json')
def auth():
    basic_auth = request.authorization
    campus_net_client.authenticate(
        basic_auth.get('username'),
        basic_auth.get('password')
    )
    if campus_net_client.is_authenticated():
        SessionAuthentication(session).authenticate(
            basic_auth.username,
            campus_net_client.auth_token
        )
        return '', 200
    else:
        return jsonify(**{'error': 'Wrong student id or password'}), 401


@app.route('/log_out', methods=['POST'])
def log_out():
    session_auth = SessionAuthentication(session)
    session_auth.log_out()
    return redirect('/')


@app.route('/cv')
def cv_page():
    session_auth = SessionAuthentication(session)
    if not session_auth.is_authenticated():
        return authenticate()
    campus_net_client.authenticate_with_token(
        session_auth.student_id,
        session_auth.auth_token
    )
    user_view = UserCVBuilder(campus_net_client, mongo_store).build()
    k = [keyword.keyword for keyword in user_view.highest_ranked_keywords][:4]
    jobs_view = CareerBuilder(career_builder_key)\
        .find_results(keywords=k)
    return render_template('cv.html', user_view=user_view, jobs_view=jobs_view)


@app.route('/cv/picture')
def picture():
    session_auth = SessionAuthentication(session)
    if not session_auth.is_authenticated():
        return '', 401
    campus_net_client.authenticate_with_token(
        session_auth.student_id,
        session_auth.auth_token
    )
    user = campus_net_client.user()
    picture = campus_net_client.user_picture(user.user_id)
    return Response(stream_picture(picture))


def authenticate():
    return redirect('/')


def stream_picture(picture):
    for chunk in picture.iter_content(1024):
        yield chunk


if __name__ == '__main__':
    app.run()
