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
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg='Такой страницы не существует')
