import redis

class Config(object):
    SECRET_KEY = "qwrtg12fgt"

    SQLALCHEMY_DATABASE_URI = "mysql://zx2005:redhat@10.1.1.128:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = "10.1.1.128"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
}