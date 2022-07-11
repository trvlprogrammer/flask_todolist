from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "danger"
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.todolist import bp as todolist_bp
    app.register_blueprint(todolist_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


    if not app.debug and not app.testing:
        # if app.config['MAIL_SERVER']:
        #     auth = None
        #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        #         auth = (app.config['MAIL_USERNAME'],
        #                 app.config['MAIL_PASSWORD'])
        #     secure = None
        #     if app.config['MAIL_USE_TLS']:
        #         secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        #         toaddrs=app.config['ADMINS'], subject='Todolist Failure',
        #         credentials=auth, secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)

        basedir = os.path.abspath(os.path.dirname(__file__))

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)        
        else :
            log_path = os.path.join(basedir,'logs')
            if app.config['LOG_PATH']:
                log_path = app.config['LOG_PATH']
            elif not os.path.exists(log_path):
                os.mkdir(log_path)                                
            file_handler = RotatingFileHandler(os.path.join(log_path,'todolist.log'),
                                                maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Todolist Startup')


    if not app.config['EXPORT_PATH']:
        export_path = os.path.join(basedir,'export') 
        if not os.path.exists(export_path):
                os.mkdir(export_path)
        app.config['EXPORT_PATH'] = export_path
    if not app.config['UPLOAD_PATH']:
        upload_path = os.path.join(basedir,'upload')
        if not os.path.exists(upload_path):
                os.mkdir(upload_path)
        app.config['UPLOAD_PATH'] = upload_path
            
        
    return app

    

from app import models