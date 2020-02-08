import os

from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

app.config['DB_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL']
app.config['DB_NAME'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME']

from app.database import db_engine

app.db_engine = db_engine.DBEngine(app.config['DB_URL'], app.config['DB_NAME'])

from app.routes import routes
