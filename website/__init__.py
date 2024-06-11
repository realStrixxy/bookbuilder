from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BookBuilder'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://database_n3ov_user:8pyXG4VxQr5AJgZzcAmZMds9duv22ZDW@dpg-cpkcsq4f7o1s73cn24hg-a/database_n3ov' # postgresql://database_n3ov_user:8pyXG4VxQr5AJgZzcAmZMds9duv22ZDW@dpg-cpkcsq4f7o1s73cn24hg-a.oregon-postgres.render.com/database_n3ov
    db.init_app(app)

    from .views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Book
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
