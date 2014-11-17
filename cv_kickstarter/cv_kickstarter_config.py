import ConfigParser
import os
env = os.environ


class CvKickstarterConfig(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("app.cfg")

    def secret_key(self):
        return (env.get('SECRET_KEY') or
                self._get_from_config_file("flask", "secret_key"))

    def campus_net_app_name(self):
        return (env.get('CAMPUS_NET_APP_NAME') or
                self._get_from_config_file("campusnet", "app_name"))

    def campus_net_app_token(self):
        return (env.get('CAMPUS_NET_APP_TOKEN') or
                self._get_from_config_file("campusnet", "app_token"))

    def career_builder_key(self):
        return (env.get('CAREER_BUILDER_DEVELOPER_KEY') or
                self._get_from_config_file("careerbuilder", "developer_key"))

    def go_key(self):
        return (env.get('GO_DEVELOPER_KEY') or
                self._get_from_config_file("godk", "guid"))

    def _get_from_config_file(self, group, key):
        return self.config.get(group, key)
