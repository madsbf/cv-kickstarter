import sys

sys.path.append('cnapi')

from flask import Flask, render_template, request, redirect
from cnapi import CampusNetApi


app = Flask(__name__)


app.config.update(dict(
    DEBUG=True,
))


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/cv')
def cv_page():
    app.logger.debug(request.args)
    api = CampusNetApi(
        'StudyPlanner3000',
        '03157abb-4cb1-47c3-8b52-cdad0f82e78a',
        request.args['dtu_id']
    )
    api.authenticate(request.args['password'])
    if api.is_authenticated():
        return render_template('cv.html', user=api.user())
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run()
