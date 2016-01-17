import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ['DEBUG'] if 'DEBUG' in os.environ else False

ADMINS = frozenset(['alecthomas3@gmail.com'])

SECRET_KEY = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ else os.urandom(32)

SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

SCHEME = os.environ['CHA_SCHEME'] if 'CHA_SCHEME' in os.environ else "http"