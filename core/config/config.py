import os
from starlette.config import Config
from starlette.datastructures import Secret
import logging

logger = logging.getLogger(__name__)

if os.environ.get('ENV') is None:

    config = Config('.env')

    SECRET_KEY = config('SECRET_KEY', cast=Secret, default='CHANGEME')

    POSTGRES_USER = config('POSTGRES_USER', cast=str)
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=Secret)
    POSTGRES_SERVER = config('POSTGRES_SERVER', cast=str, default='db')
    POSTGRES_PORT = config('POSTGRES_PORT', cast=str, default='5432')
    POSTGRES_DB = config('POSTGRES_DB', cast=str)

    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
else:
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'pass')
    POSTGRES_SERVER = os.environ.get('POSTGRES_SERVER', 'db')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'db')
    PROJECT_DB = os.environ.get('PROJECT_DB', 'project')
    REGION_DB = os.environ.get('REGION_DB', 'region')
    INSTANCE_DB = os.environ.get('INSTANCE_DB', 'instance-name')
    DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@/{POSTGRES_DB}?host=/cloudsql/{PROJECT_DB}:{REGION_DB}:{INSTANCE_DB}'