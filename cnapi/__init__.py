"""Python client for the CampusNet API.

This library is designed for having a nice interface for integrating with
the CampusNet API. The library provides an interface for the network requests
as well as objects for wrapping the data returned by the CampusNet API.

For documentation of the Campusnet API, see:

https://www.campusnet.dtu.dk/data/Documentation/CampusNet%20public%20API.pdf

Example of usage:

At first instantiate the api:

    >>> app_name = 'MyCampusNetApp'
    >>> app_token = 'sh2870272-2ush292-ji2u98s2-2h2821-jsw9j2ihs982'

    >>> api = cnapi.CampusNetApi(app_name, app_token)

In order to fetch information, authenticate the student with the student number
and password:

    >>> api.authenticate('s123456', 'secret-password')

or if the auth token is already in posession use:

    >>> api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')

To fetch the grades of the given user:

    >>> grades = api.grades()

To fetch the user infor of the given user:

    >>> user = api.user()
"""

import requests
import xml.etree.ElementTree
import re


class CampusNetApi:
    """The interface class for the API

    This class acts as the top level interface of the api and wraps the
    behaviour needed for fetching relevant information from from the API.
    """

    def __init__(self, app_name, api_token):
        self.app_name = app_name
        self.api_token = api_token
        self.student_number = None
        self.auth_token = None

    def authenticate_with_token(self, student_number, auth_token):
        """Authenticates the given user by the given authentication token"""
        self.student_number = student_number
        self.auth_token = auth_token

    def authenticate(self, student_number, password):
        """Authenticates the given user by fetching an authentication token"""
        self.student_number = student_number
        self.auth_token = self._get_auth_token(password)

    def is_authenticated(self):
        """Returns a boolean indicating whether the user is authenticated"""
        return self.auth_token is not None

    def grades(self):
        """Fetches the grades for the authenticated user"""
        return UserGradesExtractor(self._get_grades_text()).extract()

    def user(self):
        """Fetches user infor for the authenticated user"""
        return UserInfoExtractor(self._get_user_info_text()).extract()

    def user_picture(self, user_id):
        """"Fetches the user picture"""
        image = self._get_user_picture(user_id)
        if self._is_image_response(image):
            return image
        else:
            return None

    def _get_auth_token(self, password):
        return Authenticator(self.app_name, self.api_token).auth_token(
            self.student_number,
            password
        )

    def _get_grades_text(self):
        return self._client().get('Grades').text

    def _get_user_info_text(self):
        return self._client().get('UserInfo').text

    def _get_user_picture(self, user_id):
        return self._client().get('Users/%s/Picture' % user_id)

    def _is_image_response(self, response):
        return re.search('image', response.headers['content-type'])

    def _client(self):
        return UserClient(
            self.app_name,
            self.api_token,
            self.student_number,
            self.auth_token
        )


class UserClient:
    """Network client for fetching information about the user
    through the CampusNet API. This class knows about the relevant urls and
    headers in order to perform the given request.
    """
    def __init__(self, app_name, api_token, student_number, access_token):
        self.app_name = app_name
        self.api_token = api_token
        self.student_number = student_number
        self.access_token = access_token

    def get(self, path):
        """Performs a GET request to fetch information about the given user
        and includes the relevant headers for appname, token and language.

        For example:

            user_client = UserClient('MyApp', 'api-token-123', 's123', 'atoke')
            user_client.get('Grades')

        will perform a GET request to:

            https://www.campusnet.dtu.dk/data/CurrentUser/Grades

        with the headers:

            X-appname: 'MyApp'
            X-token: 'api-token-123'
            accept-language: 'da-DK'
            X-Include-services-and-relations: 'true'
        """
        return requests.get(
            ("https://www.campusnet.dtu.dk/data/CurrentUser/%s" % path),
            headers=self._headers(),
            auth=(self.student_number, self.access_token)
        )

    def _headers(self):
        return {
            'X-appname': self.app_name,
            'X-token': self.api_token,
            'accept-language': 'da-DK',
            'X-Include-services-and-relations': 'true'
        }


class AbstractXmlInfoExtractor:
    """An abstract class for classes that extract information from the xml
    returned by the CampusNet API.

    The inheriting class needs to implement:

        _extract_information
    """
    def __init__(self, response_text):
        self.response_text = response_text

    def extract(self):
        """Extract the information from the given xml

        Returns a structure given by the child class implementing
        '_extract_information'.

        Returns None if the CampusNet API returns a Fault
        """
        response_text = self.response_text.encode('utf-8')
        xml_response = xml.etree.ElementTree.fromstring(response_text)
        if self._is_response_ok(xml_response):
            return self._extract_information(xml_response)
        else:
            return None

    def _extract_information(self):
        raise NotImplementedError(
            'Xml Info Extractors need to implement _extract_information'
        )

    def _is_response_ok(self, xml_response):
        return xml_response.tag[-5:] != 'Fault'


class UserInfoExtractor(AbstractXmlInfoExtractor):
    """Is able to extract user info based on xml describe the user"""

    def _extract_information(self, xml_response):
        student_info_xml = xml_response.attrib
        return Student(
            student_info_xml['GivenName'],
            student_info_xml['FamilyName'],
            student_info_xml['Email'],
            student_info_xml['UserId']
        )


class UserGradesExtractor(AbstractXmlInfoExtractor):
    """Is able to extract the grades of the given user"""

    def _extract_information(self, xml_response):
        programme_xmls = xml_response.findall("EducationProgramme")
        return self._xml_to_programme_exam_results(programme_xmls)

    def _xml_to_programme_exam_results(self, programme_xmls):
        return map(self._xml_to_programme_exam_result, programme_xmls)

    def _xml_to_programme_exam_result(self, programme_xml):
        attributes = programme_xml.attrib
        return ProgramExamResults(
            attributes["DisplayName"],
            self._active_status_to_boolean(attributes["Active"]),
            self._ects_passed(programme_xml),
            self._programme_xml_to_exam_results(programme_xml)
        )

    def _ects_passed(self, programme_xml):
        return float(programme_xml.find("PassedEctsSum").attrib["Total"])

    def _programme_xml_to_exam_results(self, programme_xml):
        exam_result_xmls = programme_xml.findall("ExamResults/ExamResult")
        return map(self._xml_to_exam_result, exam_result_xmls)

    def _xml_to_exam_result(self, exam_result_xml):
        return ExamResultXmlMapper(exam_result_xml).exam_result()

    def _active_status_to_boolean(self, active_status_string):
        if active_status_string == 'true':
            return True
        else:
            return False


class ExamResultXmlMapper(object):
    """Is able to extract and map exam result xml into ExamResult objects"""

    def __init__(self, exam_result_xml):
        self.exam_result_xml = exam_result_xml

    """Returns an exam result object with information given by the xml"""
    def exam_result(self):
        exam_result_attributes = self.exam_result_xml.attrib
        return ExamResult(
            self._map_to_course(exam_result_attributes),
            float(exam_result_attributes['EctsPoints']),
            self._parse_grade(exam_result_attributes['Grade']),
            exam_result_attributes['Period'],
            int(exam_result_attributes['Year'])
        )

    def _parse_grade(self, grade):
        try:
            return int(grade)
        except ValueError:
            return grade

    def _map_to_course(self, exam_result_attributes):
        return Course(
            exam_result_attributes["Name"],
            exam_result_attributes["CourseCode"]
        )


class Authenticator:
    """Can authenticate a user based on a user name and a password by
    requesting an auth token from the API.

    Example usage:

        >>> auth = Authenticator('MyApp', 'app-token-123')
        >>> token = auth.auth_token('s1234', 'secretpass')
    """

    def __init__(self, app_name, api_token):
        self.app_name = app_name
        self.api_token = api_token

    def auth_token(self, username, password):
        """Fetches and returns an authentication token from CampusNet API.
        The request is a POST request send the given app name, app token,
        username and password.

        If the authentication fails, it will return None.
        """
        response = requests.post(
            'https://auth.dtu.dk/dtu/mobilapp.jsp',
            headers=self._headers(),
            data=self._authentication_payload(username, password)
        )
        return self._extract_password_from_response_body(response.text)

    def _headers(self):
        return {
            'X-appname': self.app_name,
            'X-token': self.api_token
        }

    def _authentication_payload(self, username, password):
        return {
            'username': username,
            'password': password
        }

    def _extract_password_from_response_body(self, response_text):
        response_text_xml = xml.etree.ElementTree.fromstring(response_text)
        if self._is_authenticated(response_text_xml):
            return response_text_xml.find('LimitedAccess').attrib['Password']
        else:
            return None

    def _is_authenticated(self, response_text_xml):
        return response_text_xml.find('LimitedAccess') is not None


class Student:
    """Structured class for user info from CampusNet API"""

    def __init__(self, first_name, last_name, email, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = user_id


class ProgramExamResults:
    """Structured class for programme with exam results for CampusNet API"""

    def __init__(self, programme_name, is_active, passed_ects_points, grades):
        self.programme_name = programme_name
        self.is_active = is_active
        self.passed_ects_points = passed_ects_points
        self.grades = grades


class ExamResult:
    """Structured class for exam results from CampusNet API"""

    def __init__(self, course, ects_points, grade, period, year):
        self.course = course
        self.ects_points = ects_points
        self.grade = grade
        self.period = period
        self.year = year


class Course:
    """Structured class for courses from CampusNet API"""

    def __init__(self, title, course_number):
        self.title = title
        self.course_number = course_number
