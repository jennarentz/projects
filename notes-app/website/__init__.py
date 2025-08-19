from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    #initializing flask (__name__ is file name)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #import blueprints
    from .views import views
    from .auth import auth
    
    #urls stored inside blueprint file accessed with / (which means no prefix)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #define classes before creating database 
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    #if user isn't logged in- redirect
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        #looks for primary key and checks against id
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
