import os
import argparse


def main():
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
        '--db_collection',
        default='source-codes', type=str,
        help='data base collection'
    )

    arg_parser.add_argument(
        '--text_to_image_service_url',
        default='localhost', type=str,
        help='text to image service url'
    )

    arg_parser.add_argument(
        '--text_to_image_service_port',
        default=8080, type=int,
        help='text to image service port'
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
    os.environ['PYTHON_CODE_OBFUSCATION_MONGODB_DB_COLLECTION'] = args.db_collection

    os.environ['PYTHON_CODE_OBFUSCATION_TEXT_TO_IMAGE_SERVICE_URL'] = args.text_to_image_service_url
    os.environ['PYTHON_CODE_OBFUSCATION_TEXT_TO_IMAGE_SERVICE_PORT'] = str(args.text_to_image_service_port)

    os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES'] = str(args.max_tmp_files)
    os.environ['PYTHON_CODE_OBFUSCATION_MAX_TMP_FILES_AGE'] = str(args.max_tmp_files_age)

    from app import app

    app.run(port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
