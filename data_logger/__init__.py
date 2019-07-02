#! /usr/bin/env python3

from flask import Flask, render_template
from data_logger.models import db
from data_logger.profile import *
from data_logger.project import *
from data_logger.admin import *
app = Flask(__name__)
app.config.from_json('config.json')
db.init_app(app)

@app.route('/')
def index():
    project_list = {'1':'Température salle Intel', '2':'Précipitations salle Intel', '3':'Précipitations salle Paul Otlet'}
    context = {'user_name': 'Philippe'}
    return render_template('test.html', **context)

@app.route('/profile')
def profile():
    return profile_page(app)

@app.route('/project/<id>')
def project(id):
    return project_page(app, id)

@app.route('/project/<id>/add/user')
def project_add_user(id):
    return project_add_user_page(app, id)

@app.route('/project/<id>/add/sensor')
def project_add_sensor(id):
    return project_add_sensor_page(app, id)

@app.route('/project/<id>/edit/user/<user_id>')
def project_edit_user(id, user_id):
    return project_edit_user_page(app, id, user_id)

@app.route('/project/<id>/edit/sensor/<sensor_id>')
def project_edit_sensor(id, sensor_id):
    return project_edit_sensor_page(app, id, sensor_id)

@app.route('/admin')
def project_admin():
    return project_admin_page(app)

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
