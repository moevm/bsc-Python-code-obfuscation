import os
import tempfile
import pathlib

import flask
import expiringdict

from app.database import db_engine
from app.routes import url_converters
from app.text_to_image import text_to_image

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

app.config['DB_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL']
app.config['DB_NAME'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME']
app.config['DB_COLLECTION'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_COLLECTION']

app.config['TEXT_TO_IMAGE_SERVICE_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_TEXT_TO_IMAGE_SERVICE_URL']
app.config['TEXT_TO_IMAGE_SERVICE_PORT'] = int(os.environ['PYTHON_CODE_OBFUSCATION_TEXT_TO_IMAGE_SERVICE_PORT'])

app.config['MAX_TMP_FILES'] = int(os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES'])
app.config['MAX_TMP_FILES_AGE'] = int(os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES_AGE'])

app.config['TMP_DIR'] = pathlib.Path(tempfile.gettempdir())

app.db_engine = db_engine.DBEngine(app.config['DB_URL'], app.config['DB_NAME'], app.config['DB_COLLECTION'])
app.tmp_storage = expiringdict.ExpiringDict(app.config['MAX_TMP_FILES'], app.config['MAX_TMP_FILES_AGE'])
app.text_to_image_engine = text_to_image.TextToImageEngine(app.config['TEXT_TO_IMAGE_SERVICE_URL'], app.config['TEXT_TO_IMAGE_SERVICE_PORT'])

app.url_map.converters['StorageType'] = url_converters.StorageTypeURLConverter
app.url_map.converters['ObjectId'] = url_converters.ObjectIdURLConverter
app.url_map.converters['DBViewType'] = url_converters.DBViewTypeConverter

from app.routes import routes
