class SessionAuthentication(object):
    def __init__(self, session_dict):
        self.session_dict = session_dict

    def is_authenticated(self):
        return self.student_id is not None and self.auth_token is not None

    def authenticate(self, student_id, auth_token):
        self.session_dict['student_id'] = student_id
        self.session_dict['auth_token'] = auth_token

    def log_out(self):
        self.session_dict.pop('student_id')
        self.session_dict.pop('auth_token')

    @property
    def student_id(self):
        return self.session_dict.get('student_id')

    @property
    def auth_token(self):
        return self.session_dict.get('auth_token')
