from backend import app
from flask import render_template, jsonify, request


@app.route('/')
@app.route('/<path>')
def catch_all(path=''):
    """
        method catches all requests that are not api requests
        ensures # routing possibilities within VUE
        :param path:
        :return:
    """
    return render_template('index.html')
