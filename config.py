import os
import datetime 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('GW_SECRET_KEY') or 'gy9Vl5K2OW6igD--7SyzdYhH-rIgO-mVmLBB7PvbtCA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=7) #default 1 year

    MAIL_SERVER = os.environ.get('GW_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('GW_MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('GW_MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('GW_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('GW_MAIL_PASSWORD')
    MAIL_DEBUG = 0
    GW_MAIL_SUBJECT_PREFIX = '[GothonWeb]'
    GW_MAIL_SENDER = 'Gothon Game-Master <' + str(MAIL_USERNAME) + '>'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('GW_DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'gothon.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('GW_TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('GW_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

