import os
from dotenv import load_dotenv
from datetime import datetime,timedelta,timezone

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
ACCESS_EXPIRES = timedelta(hours=1)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    BASE_DIR = basedir
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    EXPORT_PATH = os.environ.get('EXPORT_PATH') 
    LOG_PATH = os.environ.get('LOG_PATH')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['doalfatih@gmail.com']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH')
    ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))) 
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))) 
    JWT_ACCESS_TOKEN_EXPIRES=ACCESS_EXPIRES