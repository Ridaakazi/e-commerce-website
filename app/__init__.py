from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField 
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager,login_required,logout_user,current_user



app = Flask(__name__)
app.config.from_object('config')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)


migrate = Migrate(app, db)


bcrypt =Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"




from app import views, models