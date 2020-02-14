import os

from flask import Flask
from expiringdict import ExpiringDict

from app.database import db_engine

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

app.config['DB_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL']
app.config['DB_NAME'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME']

app.config['MAX_TMP_FILES'] = os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES']
app.config['MAX_TMP_FILES_AGE'] = os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES_AGE']

app.tmp_storage = ExpiringDict(app.config['MAX_TMP_FILES'], app.config['MAX_TMP_FILES_AGE'])

from app.routes import routes
