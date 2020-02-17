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
    return flask.render_template('index.html', DBViewType=db_engine.DBViewType)


@app.route('/view_code/<StorageType:storage_type>/<ObjectId:id>')
def view_code(storage_type, id):
    file = load_code(storage_type, id)

    if file is None:
        flask.abort(404)

    return flask.render_template('view_code.html', file=file)


@app.route('/view_db/<DBViewType:db_view_type>')
def view_db(db_view_type):
    tags = flask.request.args.getlist('tags')

    if db_view_type == db_engine.DBViewType.ALL:
        files = app.db_engine.get_all_files()
    elif db_view_type == db_engine.DBViewType.ANY_TAG_MATCH:
        if len(tags) == 0:
            flask.abort(400)

        flask.abort(500)
    elif db_view_type == db_engine.DBViewType.ALL_TAGS_MATCH:
        if len(tags) == 0:
            flask.abort(400)

        flask.abort(500)
    else:
        flask.abort(500)

    return flask.render_template('view_db.html',
        files=files, 
        search_tags=tags, 
        StorageType=db_engine.StorageType
    )


@app.route('/view_tags', methods=['GET', 'POST'])
def view_tags():
    request_method = flask.request.method

    if request_method == 'GET':
        tags = app.db_engine.get_all_tags()
        return flask.render_template('view_tags.html', tags=tags, DBViewType=db_engine.DBViewType)
    elif request_method == 'POST':
        search_type = flask.request.form['search_type']
        db_view_type = db_engine.DBViewType(search_type)

        tags = flask.request.form.getlist('tags')

        return flask.redirect(
            flask.url_for('view_db', 
                db_view_type=db_view_type, 
                tags=tags
            )
        )
    else:
        flask.abort(400)


@app.route('/upload_text', methods=['GET', 'POST'])
def upload_text():
    request_method = flask.request.method

    if request_method == 'GET':
        return flask.render_template('upload_text.html')
    elif request_method == 'POST':
        code = flask.request.form['code']

        str_tags = flask.request.form['tags']
        tags = [] if len(str_tags) == 0 else [tag.strip() for tag in str_tags.split(',')]

        save_to_db = 'save_to_db' in flask.request.form
        storage_type = db_engine.StorageType.DATABASE if save_to_db else db_engine.StorageType.TEMPORARY

        inserted_id = store_code(storage_type, code, tags)

        return flask.redirect(
            flask.url_for('obfuscate_settings', 
                storage_type=storage_type, 
                id=inserted_id
            )
        )
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

        str_tags = flask.request.form['tags']
        tags = [] if len(str_tags) == 0 else [tag.strip() for tag in str_tags.split(',')]

        save_to_db = 'save_to_db' in flask.request.form
        storage_type = db_engine.StorageType.DATABASE if save_to_db else db_engine.StorageType.TEMPORARY

        inserted_id = store_code(storage_type, code, tags, file_name)

        return flask.redirect(
            flask.url_for('obfuscate_settings', 
                storage_type=storage_type, 
                id=inserted_id
            )
        )
    else:
        flask.abort(400)


@app.route('/obfuscate_settings/<StorageType:storage_type>/<ObjectId:id>')
def obfuscate_settings(storage_type, id):
    file = load_code(storage_type, id)

    if file is None:
        flask.abort(404)

    return flask.render_template('obfuscate_settings.html', 
        file=file,
        storage_type=storage_type,
        id=id
    )


@app.route('/delete/<ObjectId:id>')
def delete_file(id):
    deleted_count = app.db_engine.delete_file_by_id(id)

    if deleted_count != 1:
        flask.abort(404)

    return_url = getattr(flask.request, 'referrer', flask.url_for('index_page'))

    return flask.redirect(return_url)


@app.errorhandler(404)
def not_found(e):
    return flask.render_template('error.html',
        code=404, 
        msg='Такой страницы не существует.'
    )


@app.errorhandler(400)
def bad_request(e):
    return flask.render_template('error.html',
        code=400, 
        msg='Неправильный запрос.'
    )
