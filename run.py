import os
import argparse

arg_parser = argparse.ArgumentParser(description='bsc Python code obfuscation local demo server')

arg_parser.add_argument(
    '-p', '--port', 
    default=5000, type=int,
    help='Port to run'
)

arg_parser.add_argument(
    '-d', '--debug',
    default=False, action='store_true',
    help='Enable run in debug mode'
)

arg_parser.add_argument(
    '--db_url',
    default='mongodb://localhost:27017/', type=str,
    help='url mongod is listening on'
)

arg_parser.add_argument(
    '--db_name',
    default='python-code-obfuscation', type=str,
    help='data base name'
)

arg_parser.add_argument(
    '--max_tmp_files',
    default=1000, type=int,
    help='maximum number of simultaneously stored files in RAM'
)

arg_parser.add_argument(
    '--max_tmp_files_age',
    default=86400, type=int,
    help='maximum age in seconds of temporary files stored in RAM'
)

args = arg_parser.parse_args()

os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_URL'] = args.db_url
os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_NAME'] = args.db_name

from app import app

app.run(port=args.port, debug=args.debug)
