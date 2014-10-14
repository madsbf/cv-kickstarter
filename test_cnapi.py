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
def test_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('authentication.xml')
    )
    api = new_api()
    api.authenticate('security')
    assert api.auth_token == '21EF8196-ED05-4BAB-9081-44313ABD3D32'
    assert api.is_authenticated() is True


@responses.activate
def test_unauthorized():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('wrong_authentication.xml')
    )
    api = new_api()
    api.authenticate('bad-password')
    assert api.is_authenticated() is False


@responses.activate
def test_user_info():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/UserInfo',
        body=load_fixture('user_info.xml')
    )
    api = new_api('21EF8196-ED05-4BAB-9081-44313ABD3D32')
    student = api.user_info()
    assert student.first_name == 'Anders'
    assert student.last_name == 'And'
    assert student.email == 's123456@student.dtu.dk'


@responses.activate
def test_grades():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Grades',
        body=load_fixture('grades.xml')
    )
    api = new_api('21EF8196-ED05-4BAB-9081-44313ABD3D32')
    grades = api.grades()
    assert grades[1].course.title == u'Robuste softwaresystemer'
