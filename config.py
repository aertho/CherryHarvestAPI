import os
_basedir = os.path.abspath(os.path.dirname(__file__))

try:
    DEBUG = os.environ['DEBUG']
except KeyError:
    DEBUG = True

ADMINS = frozenset(['alecthomas3@gmail.com'])
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    SECRET_KEY = "\x0f\xd6\x17y\r!>g\x14E\xbbQ\x06\x9b\x8b\xb0\xa7\xfc\xd1M'\xb8'\xee"

try:
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
except KeyError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')

DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

SCHEME = "http"