import sys

sys.path.append('cnapi')

from flask import Flask, render_template, requ
from cnapi import CampusNetApi


app = Flask(__name__)


app.config.update(dict(
    debug=True,
))


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/cv')
def cv_page():
    api = CampusNetApi(
        'StudyPlanner3000',
        '03157abb-4cb1-47c3-8b52-cdad0f82e78a',
        student_id
    )
    api.authenticate('y72QxXj8')
    if api.is_authenticated()
        return render_template('cv.html', student_)
    else:
        return 'Wrong password', 403


if __name__ == '__main__':
    app.run()
