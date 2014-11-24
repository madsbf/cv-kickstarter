import sys
sys.path.append('cv_kickstarter/lib')

from session_authentication import SessionAuthentication


def test_authentication_sets_credentials_on_session():
    session = {}
    session_auth = SessionAuthentication(session)
    session_auth.authenticate('my_student_id', 'ksj2-s82s-2u1h2')
    assert session['student_id'] == 'my_student_id'
    assert session['auth_token'] == 'ksj2-s82s-2u1h2'


def test_student_id_is_returned_after_authentication():
    session = {}
    session_auth = SessionAuthentication(session)
    session_auth.authenticate('my_student_id', 'ksj2-s82s-2u1h2')
    assert session_auth.student_id == 'my_student_id'


def test_auth_token_is_returned_after_authentication():
    session = {}
    session_auth = SessionAuthentication(session)
    session_auth.authenticate('my_student_id', 'ksj2-s82s-2u1h2')
    assert session_auth.auth_token == 'ksj2-s82s-2u1h2'


def test_authenticated_session_authentication_is_authenticated():
    session = {}
    session_auth = SessionAuthentication(session)
    session_auth.authenticate('my_student_id', 'ksj2-s82s-2u1h2')
    assert session_auth.is_authenticated() is True


def test_new_session_authentication_is_not_authenticated():
    session = {}
    session_auth = SessionAuthentication(session)
    assert session_auth.is_authenticated() is False


def test_logged_out_session_authentication_removes_credentials_from_session():
    session = {}
    session_auth = SessionAuthentication(session)
    session_auth.authenticate('my_student_id', 'ksj2-s82s-2u1h2')
    session_auth.log_out()
    assert 'student_id' not in session
    assert 'auth_token' not in session


def test_logged_out_session_authentication_is_not_authenticated():
    session = {}
    session_auth = SessionAuthentication(session)
    assert session_auth.is_authenticated() is False
