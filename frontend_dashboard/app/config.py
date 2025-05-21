import os


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv("SECRET_KEY") or "plVdTwE0roGrrdXMBzWv9SSguvg6YDJp"
    PATH_CONFIG_YAML = os.path.join(BASE_DIR, "config.yaml")
    PATH_WELCOME = os.path.join("home", "welcome.py")
    PATH_LOGIN = os.path.join("auth", "login.py")
    PATH_LOGOUT = os.path.join("auth", "logout.py")
