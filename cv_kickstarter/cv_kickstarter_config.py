"""Configuration for cv_kickstarter."""
try:
    # Try to parse for Python 3
    from configparser import ConfigParser
except ImportError:
    # Fall back to the Python 2 way
    from ConfigParser import ConfigParser

import os
env = os.environ


class CvKickstarterConfig(object):

    """Configuration for cv_kickstarter."""

    def __init__(self, config_file_path='app.cfg'):
        """Initialize configuration with config file path.

        Defaults config_file_path to 'app.cfg'.
        """
        self.config = ConfigParser()
        self.config.read(config_file_path)

    def secret_key(self):
        """Return the secret key for Flask app.

        Given by environment variable SECRET_KEY or in config file as
        [flask]
        secret_key: my-secret-key
        """
        return (env.get('SECRET_KEY') or
                self._get_from_config_file("flask", "secret_key"))

    def campus_net_app_name(self):
        """Return the campus net app name for CampusNet API.

        Given by environment variable CAMPUS_NET_APP_NAME or in config file as
        [campusnet]
        app_name: my-app-name
        """
        return (env.get('CAMPUS_NET_APP_NAME') or
                self._get_from_config_file("campusnet", "app_name"))

    def campus_net_app_token(self):
        """Return the campus net app token name for CampusNet API.

        Given by environment variable CAMPUS_NET_APP_TOKEN or in config file as
        [campusnet]
        app_token: secret-app-token
        """
        return (env.get('CAMPUS_NET_APP_TOKEN') or
                self._get_from_config_file("campusnet", "app_token"))

    def career_builder_key(self):
        """Return the career builder api key.

        Given by environment variable CAREER_BUILDER_DEVELOPER_KEY or
        in config file as
        [campusnet]
        app_token: secret-app-token
        """
        return (env.get('CAREER_BUILDER_DEVELOPER_KEY') or
                self._get_from_config_file("careerbuilder", "developer_key"))

    def go_key(self):
        """Return the go.dk api key.

        Given by environment variable GO_DEVELOPER_KEY or
        in config file as
        [godk]
        guid: secret-guid-key
        """
        return (env.get('GO_DEVELOPER_KEY') or
                self._get_from_config_file("godk", "guid"))

    def mongo_url(self):
        """Return the URL for the Mongo DB.

        This is not mandatory to get the app to work.

        Given by environment variable MONGO_URL.
        """
        return env.get("MONGO_URL")

    def mongo_db_name(self):
        """Return the database name of the Mongo Database.

        Given by environment variable MONGO_DB_NAME  or in config file as
        [mongo]
        db_name: my_mongo_db_name
        """
        return (env.get("MONGO_DB_NAME") or
                self._get_from_config_file("mongo", "db_name"))

    def opbeat_org_id(self):
        return env.get("OPBEAT_ORG_ID")

    def opbeat_app_id(self):
        return env.get("OPBEAT_APP_ID")

    def opbeat_secret_token(self):
        return env.get("OPBEAT_SECRET_TOKEN")

    def _get_from_config_file(self, group, key):
        return self.config.get(group, key)
