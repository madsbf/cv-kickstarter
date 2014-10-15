import requests
import xml.etree.ElementTree

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
    >>> student_number = 's123456'

    >>> api = cnapi.CampusNetApi(app_name, app_token, student_number)

In order to fetch information, authenticate with the password of the user:

    >>> api.authenticate('secret-password')

To fetch the grades of the given user:

    >>> grades = api.grades()

To fetch the user infor of the given user:

    >>> api.user_info()
"""


class CampusNetApi:
    """The interface class for the API

    This class acts as the top level interface of the api and wraps the
    behaviour needed for fetching relevant information from from the API.
    """

    def __init__(self, app_name, api_token, student_number, auth_token=None):
        self.app_name = app_name
        self.api_token = api_token
        self.student_number = student_number
        self.auth_token = auth_token

    def authenticate(self, password):
        """Authenticates the given user by fetching an authentication token"""
        self.auth_token = self._get_auth_token(password)

    def is_authenticated(self):
        """Returns a boolean indicating whether the user is authenticated"""
        return self.auth_token is not None

    def grades(self):
        """Fetches the grades for the authenticated user"""
        return UserGradesExtractor(self._client().get('Grades').text).extract()

    def user_info(self):
        """Fetches user infor for the authenticated user"""
        return UserInfoExtractor(self._client().get('UserInfo').text).extract()

    def _get_auth_token(self, password):
        return Authenticator(self.app_name, self.api_token).auth_token(
            self.student_number,
            password
        )

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
    def __init__(self, response_text):
        self.response_text = response_text

    def extract(self):
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
    def _extract_information(self, xml_response):
        student_info_xml = xml_response.attrib
        return Student(
            student_info_xml['GivenName'],
            student_info_xml['FamilyName'],
            student_info_xml['Email']
        )


class UserGradesExtractor(AbstractXmlInfoExtractor):
    def _extract_information(self, xml_response):
        courses_xml = xml_response.findall(
            "EducationProgramme/ExamResults/ExamResult"
        )
        return [self._map_to_exam_results(course_xml.attrib)
                for course_xml in courses_xml]

    def _map_to_exam_results(self, course_xml):
        return ExamResult(
            self._map_to_course(course_xml),
            course_xml['EctsPoints'],
            course_xml['Grade'],
            course_xml['Period'],
            course_xml['Year']
        )

    def _map_to_course(self, course_xml):
        return Course(
            course_xml["Name"],
            course_xml["CourseCode"]
        )


class Authenticator:
    def __init__(self, app_name, api_token):
        self.app_name = app_name
        self.api_token = api_token

    def auth_token(self, username, password):
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
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class ExamResult:
    def __init__(self, course, ects_points, grade, period, year):
        self.course = course
        self.ects_points = ects_points
        self.grade = grade
        self.period = period
        self.year = year


class Course:
    def __init__(self, title, course_number):
        self.title = title
        self.course_number = course_number
