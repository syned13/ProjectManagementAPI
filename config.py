class Config():
    pass
class DevelopmentConfig(Config):
    DEBUG = True


#dict para las diferentes configuraciones
config = {
    'development': DevelopmentConfig
}