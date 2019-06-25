#! /usr/bin/env python3

from flask import Flask, render_template
from data_logger.models import db

app = Flask(__name__)
app.config.from_json('config.json')
db.init_app(app)

@app.route('/')
def index():
    context = {'user_name': 'test_name'}
    return render_template('index.html', **context)

@app.route('/test')
def test():
    return "This is a test"

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
