try:
    # Try to parse for Python 3
    from configparser import ConfigParser
except ImportError:
    # Fall back to the Python 2 way
    from ConfigParser import ConfigParser

import os
env = os.environ


class CvKickstarterConfig(object):
    def __init__(self, config_file_path='app.cfg'):
        self.config = ConfigParser()
        self.config.read(config_file_path)

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

    def mongo_url(self):
        return env.get("MONGO_URL")

    def mongo_db_name(self):
        return (env.get("MONGO_DB_NAME") or
                self._get_from_config_file("mongo", "db_name"))

    def _get_from_config_file(self, group, key):
        return self.config.get(group, key)
