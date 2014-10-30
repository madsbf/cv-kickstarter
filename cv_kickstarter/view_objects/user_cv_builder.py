from werkzeug import cached_property
from user_cv import UserCV


class UserCVBuilder(object):

    def __init__(self, campus_net_client):
        self.campus_net_client = campus_net_client

    def build(self):
        return UserCV(
            self.user.first_name,
            self.user.last_name,
            self.grades
        )

    @cached_property
    def user(self):
        return self.campus_net_client.user()

    @cached_property
    def grades(self):
        return self.campus_net_client.grades()
