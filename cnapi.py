import requests
import xml.etree.ElementTree


class CampusNetApi:
    def __init__(self, app_name, api_token, student_number, auth_token=None):
        self.app_name = app_name
        self.api_token = api_token
        self.student_number = student_number
        self.auth_token = auth_token

    def authenticate(self, password):
        if self.auth_token is not None:
            return None
        self.auth_token = self._get_auth_token(password)

    def grades(self):
        return UserGradesExtractor(self._client().get('Grades').text).grades()

    def user_info(self):
        return UserInfoExtractor(self._client().get('UserInfo').text).user()

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
    def __init__(self, app_name, api_token, student_number, access_token):
        self.app_name = app_name
        self.api_token = api_token
        self.student_number = student_number
        self.access_token = access_token

    def get(self, path):
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


class UserInfoExtractor:
    def __init__(self, user_info_response_text):
        self.user_info_response_text = user_info_response_text

    def user(self):
        response_text = self.user_info_response_text.encode('utf-8')
        xml_response = xml.etree.ElementTree.fromstring(response_text)
        return self._map_xml_to_student(xml_response.attrib)

    def _map_xml_to_student(self, student_info_xml):
        return Student(
            student_info_xml['GivenName'],
            student_info_xml['FamilyName'],
            student_info_xml['Email']
        )


class UserGradesExtractor:
    def __init__(self, grades_response_text):
        self.grades_response_text = grades_response_text

    def grades(self):
        response_text = self.grades_response_text.encode('utf-8')
        xml_response = xml.etree.ElementTree.fromstring(response_text)
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
            'appname': self.app_name,
            'token': self.api_token
        }

    def _authentication_payload(self, username, password):
        return {
            'username': username,
            'password': password
        }

    def _extract_password_from_response_body(self, response_text):
        return xml.etree.ElementTree.fromstring(
            response_text
        ).find('LimitedAccess').attrib['Password']


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
