# -*- coding: utf-8 -*-

from cv_kickstarter import cnapi
import responses

import os
test_path = os.path.dirname(__file__)


def load_fixture(fixture_path):
    return open(os.path.join(test_path, 'fixtures/cnapi', fixture_path)).read()


def new_api():
    return cnapi.CampusNetApi(
        "AppName3000",
        "secure-app-token"
    )


def new_authenticated_api():
    api = new_api()
    api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')
    return api


def stub_successful_grade_request():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Grades',
        body=load_fixture('grades.xml')
    )


@responses.activate
def test_auth_token_is_set_with_successfull_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('authentication.xml')
    )
    api = new_api()
    api.authenticate('s123456', 'security')
    assert api.auth_token == '21EF8196-ED05-4BAB-9081'


@responses.activate
def test_user_is_authenticated_with_successfull_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('authentication.xml')
    )
    api = new_api()
    api.authenticate('s123456', 'security')
    assert api.is_authenticated() is True


def test_authentication_with_token_is_authenticated():
    api = new_api()
    api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')
    assert api.is_authenticated() is True


def test_authentication_with_token_sets_student_number():
    api = new_api()
    api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')
    assert api.student_number is 's123456'


def test_authentication_with_token_sets_auth_token():
    api = new_api()
    api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')
    assert api.auth_token is '21EF8196-ED05-4BAB-9081'


@responses.activate
def test_user_is_not_authenticated_with_wrong_authentication():
    responses.add(
        responses.POST,
        'https://auth.dtu.dk/dtu/mobilapp.jsp',
        body=load_fixture('wrong_authentication.xml')
    )
    api = new_api()
    api.authenticate('s123456', 'bad-password')
    assert api.is_authenticated() is False


@responses.activate
def test_user_object_is_returned_when_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/UserInfo',
        body=load_fixture('user.xml')
    )
    api = new_authenticated_api()
    student = api.user()
    assert student.first_name == 'Anders'
    assert student.last_name == 'And'
    assert student.email == 's123456@student.dtu.dk'
    assert student.user_id == '1234'


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
def test_user_picture_is_none_when_not_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Users/1234/Picture',
        body=load_fixture('unauthorized_request.xml'),
        content_type="application/xml; charset='uft-8'"
    )
    api = new_api()
    image = api.user_picture('1234')
    assert image is None


@responses.activate
def test_user_picture_is_returned_when_authenticated():
    responses.add(
        responses.GET,
        'https://www.campusnet.dtu.dk/data/CurrentUser/Users/1234/Picture',
        body=load_fixture('image.png'),
        content_type="image/jpeg"
    )
    api = new_authenticated_api()
    picture = api.user_picture('1234')
    assert picture.text == '12345image\n'


@responses.activate
def test_grades_has_two_programmes():
    stub_successful_grade_request()
    api = new_authenticated_api()
    programmes = api.grades()
    assert len(programmes) == 3


@responses.activate
def test_grades_has_programme_with_four_courses():
    stub_successful_grade_request()
    api = new_authenticated_api()
    programmes = api.grades()
    assert len(programmes[0].exam_results) == 4


@responses.activate
def test_grades_has_programme_with_correct_information():
    stub_successful_grade_request()
    api = new_authenticated_api()
    programmes = api.grades()
    first_programme = programmes[0]
    assert first_programme.name == "Bachelor (Softwaretek.)"
    assert first_programme.is_active is False
    assert first_programme.passed_ects_points == 20.0


@responses.activate
def test_grades_has_programme_with_correct_exam_result_information():
    stub_successful_grade_request()
    api = new_authenticated_api()
    programmes = api.grades()
    first_programme = programmes[0]
    second_exam_result = first_programme.exam_results[1]
    assert second_exam_result.course_number == "02241"
    assert second_exam_result.course_title == "Robuste softwaresystemer"
    assert second_exam_result.ects_points == 5.0
    assert second_exam_result.grade == 10
    assert second_exam_result.year == 2013


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
