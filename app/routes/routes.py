import flask

from app import app
from app.database.storage_type import StorageType


def store_code(storage_type, code, tags, file_name=None):
    if storage_type == StorageType.DATABASE:
        inserted_id = app.db_engine.upload(file_name, code, tags)
    elif storage_type == StorageType.TEMPORARY:
        inserted_id = app.db_engine.generate_id()
        serialized_file = app.db_engine.serialize_file(file_name, code, tags)
        app.tmp_storage[str(inserted_id)] = serialized_file
    else:
        flask.abort(500)

    return inserted_id


def load_code(storage_type, id):
    if storage_type == StorageType.DATABASE:
        return app.db_engine.get_file_by_id(id)
    elif storage_type == StorageType.TEMPORARY:
        return app.tmp_storage.get(str(id), None)
    else:
        flask.abort(500)


@app.route('/')
def index_page():
    return flask.render_template('index.html')


@app.route('/upload_text', methods=['GET', 'POST'])
def upload_text():
    request_method = flask.request.method

    if request_method == 'GET':
        return flask.render_template('upload_text.html')
    elif request_method == 'POST':
        source_code = flask.request.form['source_code']

        tags = flask.request.form['tags'].split(',')

        save_to_db = True if flask.request.form['save_to_db'] == 'on' else False
        storage_type = StorageType.DATABASE if save_to_db else StorageType.TEMPORARY

        if storage_type == StorageType.DATABASE:
            inserted_id = app.db_engine.upload(None, source_code, tags)
        else:
            inserted_id = app.db_engine.generate_id()
            serialized_file = app.db_engine.serialize_file(None, source_code, tags)
            app.tmp_storage[str(inserted_id)] = serialized_file

        return flask.redirect(flask.url_for('obfuscate_settings', storage_type=storage_type, id=inserted_id))
    else:
        flask.abort(400)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    request_method = flask.request.method

    if request_method == 'GET':
        return flask.render_template('upload_text.html')
    elif request_method == 'POST':
        file = flask.request.files['source_code']
        
        file_name = file.filename
        
        source_code_bytes = file.read()
        source_code = str(source_code_bytes, 'utf-8')

        tags = flask.request.form['tags'].split(',')

        save_to_db = True if flask.request.form['save_to_db'] == 'on' else False
        storage_type = StorageType.DATABASE if save_to_db else StorageType.TEMPORARY

        if storage_type == StorageType.DATABASE:
            inserted_id = app.db_engine.upload(file_name, source_code, tags)
        else:
            inserted_id = app.db_engine.generate_id()
            serialized_file = app.db_engine.serialize_file(file_name, source_code, tags)
            app.tmp_storage[str(inserted_id)] = serialized_file

        return flask.redirect(flask.url_for('obfuscate_settings', storage_type=storage_type, id=inserted_id))
    else:
        flask.abort(400)


@app.errorhandler(404)
def not_found(e):
    return flask.render_template('error.html', code=404, msg='Такой страницы не существует.')


@app.errorhandler(400)
def bad_request(e):
    return flask.render_template('error.html', code=400, msg='Неправильный запрос.')
