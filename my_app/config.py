class BaseConfig(object):
    '''Base config class'''
    SECRET_KEY = 'A random key'
    DEBUG = True
    TESTING = True
    NEW_CONFIG_VARIABLE = 'my value'


class ProductionConfig(BaseConfig):
    '''Production specific config'''
    DEBUG = False
    SECRET_KEY = open('secret')


class StagingConfig(BaseConfig):
    '''Staging specific config'''
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    '''Development environment specific config'''
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Another random secret key'
