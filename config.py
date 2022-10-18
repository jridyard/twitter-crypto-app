'''
    App configuration file.
'''

import os
from decouple import config
import re

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # Database / Toggle :: Local SQLite || Vagrant DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')        # Use this for local DB
    # SQLALCHEMY_DATABASE_URI = "postgresql://outsize:dbpass@localhost:5432/outsize"    # Use this for vagrant DB

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # CELERYD_CONCURRENCY = 10   # set a concurrency limit (default = 5)


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7 * 4

    SQLALCHEMY_DATABASE_URI = re.sub("^postgres://","postgresql://", config('DATABASE_URL', default=''))
    CELERY_BROKER_URL = config('REDIS_URL', default=None)
    CELERY_RESULT_BACKEND = config('REDIS_URL', default=None)


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
