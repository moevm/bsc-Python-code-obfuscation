import os

import flask
import expiringdict

from app.database import db_engine

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

app.config['DB_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL']
app.config['DB_NAME'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME']
app.config['DB_COLLECTION'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_COLLECTION']

app.config['MAX_TMP_FILES'] = int(os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES'])
app.config['MAX_TMP_FILES_AGE'] = int(os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES_AGE'])

app.db_engine = db_engine.DBEngine(app.config['DB_URL'], app.config['DB_NAME'], app.config['DB_COLLECTION'])
app.tmp_storage = expiringdict.ExpiringDict(app.config['MAX_TMP_FILES'], app.config['MAX_TMP_FILES_AGE'])

from app.routes import routes
