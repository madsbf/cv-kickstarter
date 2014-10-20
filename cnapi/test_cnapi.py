# -*- coding: utf-8 -*-

import cnapi
import responses


def load_fixture(fixture_path):
    return open('fixtures/%s' % fixture_path).read()


def new_api(auth_token=None):
    return cnapi.CampusNetApi(
        "AppName3000",
        "secure-app-token",
        's123456',
        auth_token
    )


@responses.activate
def test_auth_token_is_set_with_successfull_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('authentication.xml')
    )
    api = new_api()
    api.authenticate('security')
    assert api.auth_token == '21EF8196-ED05-4BAB-9081-44313ABD3D32'


@responses.activate
def test_user_is_authenticated_with_successfull_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('authentication.xml')
    )
    api = new_api()
    api.authenticate('security')
    assert api.is_authenticated() is True


@responses.activate
def test_user_is_not_authenticated_with_wrong_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('wrong_authentication.xml')
    )
    api = new_api()
    api.authenticate('bad-password')
    assert api.is_authenticated() is False


@responses.activate
def test_user_object_is_returned_when_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/UserInfo',
        body=load_fixture('user.xml')
    )
    api = new_api('21EF8196-ED05-4BAB-9081-44313ABD3D32')
    student = api.user()
    assert student.first_name == 'Anders'
    assert student.last_name == 'And'
    assert student.email == 's123456@student.dtu.dk'


@responses.activate
def test_user_object_is_empty_when_not_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/UserInfo',
        body=load_fixture('unauthorized_request.xml')
    )
    api = new_api()
    student = api.user()
    assert student is None


@responses.activate
def test_grades_objects_are_returned_when_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Grades',
        body=load_fixture('grades.xml')
    )
    api = new_api('21EF8196-ED05-4BAB-9081-44313ABD3D32')
    grades = api.grades()
    first_grade = grades[1]
    assert first_grade.ects_points == 5.0
    assert first_grade.grade == 10
    assert first_grade.year == 2013
    assert first_grade.course.title == u'Robuste softwaresystemer'
    assert first_grade.course.course_number == u'02241'


@responses.activate
def test_grades_is_empty_when_not_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Grades',
        body=load_fixture('unauthorized_request.xml')
    )
    api = new_api()
    grades = api.grades()
    assert grades is None
