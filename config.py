import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = 'asdlsdaklwj'
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
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')
    