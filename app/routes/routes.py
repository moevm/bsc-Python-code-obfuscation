import flask

from app import app
from app.database import db_engine


def store_code(storage_type, code, tags, file_name=None):
    if storage_type == db_engine.StorageType.DATABASE:
        inserted_id = app.db_engine.upload(file_name, code, tags)
    elif storage_type == db_engine.StorageType.TEMPORARY:
        inserted_id = app.db_engine.generate_id()
        serialized_file = app.db_engine.serialize_file(file_name, code, tags)
        app.tmp_storage[str(inserted_id)] = serialized_file
    else:
        flask.abort(500)

    return inserted_id


def load_code(storage_type, id):
    if storage_type == db_engine.StorageType.DATABASE:
        return app.db_engine.get_file_by_id(id)
    elif storage_type == db_engine.StorageType.TEMPORARY:
        return app.tmp_storage.get(str(id), None)
    else:
        flask.abort(500)


@app.route('/')
def index_page():
    return flask.render_template('index.html')


@app.route('/view_code/<StorageType:storage_type>/<ObjectId:id>')
def view_code(storage_type, id):
    file = load_code(storage_type, id)

    if file is None:
        flask.abort(404)

    return flask.render_template('view_code.html', file=file)


@app.route('/upload_text', methods=['GET', 'POST'])
def upload_text():
    request_method = flask.request.method

    if request_method == 'GET':
        return flask.render_template('upload_text.html')
    elif request_method == 'POST':
        code = flask.request.form['code']

        tags = flask.request.form['tags'].split(',')

        save_to_db = 'save_to_db' in flask.request.form
        storage_type = db_engine.StorageType.DATABASE if save_to_db else db_engine.StorageType.TEMPORARY

        inserted_id = store_code(storage_type, code, tags)

        return flask.redirect(flask.url_for('obfuscate_settings', storage_type=storage_type, id=inserted_id))
    else:
        flask.abort(400)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    request_method = flask.request.method

    if request_method == 'GET':
        return flask.render_template('upload_file.html')
    elif request_method == 'POST':
        file = flask.request.files['source_code']
        
        file_name = file.filename
        
        code_bytes = file.read()
        code = str(code_bytes, 'utf-8')

        tags = flask.request.form['tags'].split(',')

        save_to_db = 'save_to_db' in flask.request.form
        storage_type = db_engine.StorageType.DATABASE if save_to_db else db_engine.StorageType.TEMPORARY

        inserted_id = store_code(storage_type, code, tags, file_name)

        return flask.redirect(flask.url_for('obfuscate_settings', storage_type=storage_type, id=inserted_id))
    else:
        flask.abort(400)


@app.route('/obfuscate_settings/<StorageType:storage_type>/<ObjectId:id>')
def obfuscate_settings(storage_type, id):
    file = load_code(storage_type, id)

    if file is None:
        flask.abort(404)

    return flask.render_template('obfuscate_settings.html', file=file, storage_type=storage_type, id=id)

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('error.html', code=404, msg='Такой страницы не существует.')


@app.errorhandler(400)
def bad_request(e):
    return flask.render_template('error.html', code=400, msg='Неправильный запрос.')
