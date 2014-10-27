class RequestBasicAuth(object):
    def __init__(self, request_authorization):
        self.request_authorization = request_authorization

    def is_credentials_given(self):
        return self.request_authorization is not None

    @property
    def username(self):
        return self.request_authorization.username

    @property
    def password(self):
        return self.request_authorization.password
