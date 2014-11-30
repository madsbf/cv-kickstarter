class SessionAuthentication(object):

    """Utilizes the a session dictionary as authentication storage.

    Integrates with the Flask session.
    """

    def __init__(self, session_dict):
        """Initialize SessionAuthentication with a session dictionary."""
        self.session_dict = session_dict

    def is_authenticated(self):
        """Return true if the user is authenticated in the session."""
        return self.student_id is not None and self.auth_token is not None

    def authenticate(self, student_id, auth_token):
        """Authenticate a student by setting student_id and auth_token."""
        self.session_dict['student_id'] = student_id
        self.session_dict['auth_token'] = auth_token

    def log_out(self):
        """Log the user out by removing student_id and auth_token."""
        self.session_dict.pop('student_id')
        self.session_dict.pop('auth_token')

    @property
    def student_id(self):
        """Return student id from session."""
        return self.session_dict.get('student_id')

    @property
    def auth_token(self):
        """Return authentication token from session."""
        return self.session_dict.get('auth_token')
