import flask

from app import app


@app.route('/')
def index_page():
    return flask.render_template('index.html')


@app.route('/view_code')
def view_code():
    file_id = flask.request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            return flask.render_template('view_code.html', file=file)
        else:
            flask.flash(f'неверный параметр id(={file_id})', 'error')
            return flask.redirect(flask.url_for('index_page'))    
    else:
        flask.flash('отсутствует параметр id', 'error')
        return flask.redirect(flask.url_for('index_page'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if flask.request.method == 'GET':
        return flask.render_template('upload.html')
    else:
        file = flask.request.files['source_code']
        
        filename = file.filename
        
        source_code_bytes = file.read()
        source_code = str(source_code_bytes, 'utf-8')

        tags_str = flask.request.form['tags']

        if len(tags_str) == 0:
            tags = []
        else:
            tags = tags_str.split(',')

        save_to_db = True if flask.request.form['save_to_db'] == 'on' else False

        inserted_id = app.db_engine.upload(filename, source_code, tags)

        return flask.redirect(flask.url_for('obfuscate_settings', id=str(inserted_id)))


@app.route('/obfuscate_settings')
def obfuscate_settings():
    file_id = flask.request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            return flask.render_template('obfuscate_settings.html', file=file, file_id=file_id)
        else:
            flask.flash(f'неверный параметр id(={file_id})', 'error')
            return flask.redirect(flask.url_for('index_page'))    
    else:
        flask.flash('отсутствует параметр id', 'error')
        return flask.redirect(flask.url_for('index_page'))


@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    file_id = flask.request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            # TODO obfuscation here
            return flask.redirect(flask.url_for('view_code', id=file_id))
        else:
            flask.flash(f'неверный параметр id(={file_id})', 'error')
            return flask.redirect(flask.url_for('index_page'))    
    else:
        flask.flash('отсутствует параметр id', 'error')
        return flask.redirect(flask.url_for('index_page'))


@app.errorhandler(404)
def not_found(e):
    return flask.render_template('error.html', code=404, msg='Такой страницы не существует.')


@app.errorhandler(400)
def bad_request(e):
    return flask.render_template('error.html', code=400, msg='Неправильный запрос.')
