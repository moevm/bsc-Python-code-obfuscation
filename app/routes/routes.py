from flask import render_template, request, jsonify, redirect, url_for, flash

from app import app


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/view_code')
def view_code():
    file_id = request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            return render_template('view_code.html', file=file)
        else:
            flash(f'неверный параметр id(={file_id})', 'error')
            return redirect(url_for('index_page'))    
    else:
        flash('отсутствует параметр id', 'error')
        return redirect(url_for('index_page'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file = request.files['source_code']
        
        filename = file.filename
        
        source_code_bytes = file.read()
        source_code = str(source_code_bytes, 'utf-8')

        tags_str = request.form['tags']

        if len(tags_str) == 0:
            tags = []
        else:
            tags = tags_str.split(',')

        save_to_db = True if request.form['save_to_db'] == 'on' else False

        inserted_id = app.db_engine.upload(filename, source_code, tags)

        return redirect(url_for('obfuscate_settings', id=str(inserted_id)))


@app.route('/obfuscate_settings')
def obfuscate_settings():
    file_id = request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            return render_template('obfuscate_settings.html', file=file, file_id=file_id)
        else:
            flash(f'неверный параметр id(={file_id})', 'error')
            return redirect(url_for('index_page'))    
    else:
        flash('отсутствует параметр id', 'error')
        return redirect(url_for('index_page'))


@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    file_id = request.args.get('id', None)

    if file_id is not None:
        file = app.db_engine.get_file_by_id(file_id)

        if file is not None:
            # TODO obfuscation here
            return redirect(url_for('view_code', id=file_id))
        else:
            flash(f'неверный параметр id(={file_id})', 'error')
            return redirect(url_for('index_page'))    
    else:
        flash('отсутствует параметр id', 'error')
        return redirect(url_for('index_page'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg='Такой страницы не существует')
