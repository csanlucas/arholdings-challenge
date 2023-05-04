from dotenv import load_dotenv
import os

from .environments import ENV_LOCAL, ENV_PROD

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=f'{basedir}/../.env')

class Config():
    DATABASE_CRED = None

    @staticmethod
    def set_database_credentials(env=''):
        cred = None
        if env == ENV_LOCAL:
            cred = {
                'NAME': os.environ.get('NAME_DB_LOCAL'),
                'USER': os.environ.get('USER_DB_LOCAL'),
                'PASSWORD': os.environ.get('PASSWORD_DB_LOCAL'),
                'HOST': os.environ.get('HOST_DB_LOCAL'),
                'PORT': os.environ.get('PORT_DB_LOCAL')
            }
        elif env == ENV_PROD:
            cred = {
                'NAME': os.environ.get('NAME_DB_PROD'),
                'USER': os.environ.get('USER_DB_PROD'),
                'PASSWORD': os.environ.get('PASSWORD_DB_PROD'),
                'HOST': os.environ.get('HOST_DB_PROD'),
                'PORT': os.environ.get('PORT_DB_PROD')
            }
        Config.DATABASE_CRED = cred
        return cred
