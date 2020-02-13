from flask import render_template, request, jsonify, redirect, url_for, flash

from app import app


@app.route('/')
def index_page():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg='Такой страницы не существует')
