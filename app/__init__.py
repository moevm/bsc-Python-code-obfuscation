import os

from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

app.config['DB_URL'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL']
app.config['DB_NAME'] = os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME']

from app import routes
