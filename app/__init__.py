from flask import Flask
from peewee import SqliteDatabase
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config.from_object('config.Config')

# Database setup
db = SqliteDatabase(app.config['DATABASE'])

# Flask-WTF CSRF protection
csrf = CSRFProtect(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

from app import routes
