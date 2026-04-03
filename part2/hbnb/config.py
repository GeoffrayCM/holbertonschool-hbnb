class Config:
    SECRET_KEY = "dev_key"
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True