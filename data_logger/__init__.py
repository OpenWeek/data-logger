#! /usr/bin/env python3

from flask import Flask, render_template
from data_logger.models import db
from data_logger.profile import *
from data_logger.project import *
from data_logger.admin import *
app = Flask(__name__)
app.config.from_json('config.json')
db.init_app(app)

project_list = [{"id":'1',"name":'Température salle Intel'}, {"id":'22',"name":'Précipitations salle Intel'},{"id":'33' ,"name":'Précipitations salle Paul Otlet'}]
user_name = 'Philippe'
user_privilege = 'admin'
basic_context = {}
basic_context['user_name'] = user_name
basic_context['user_privilege'] = user_privilege
basic_context['project_list'] = project_list

@app.route('/')
def index():
    basic_context['url'] = '/'
    context = basic_context
    return render_template('index.html', **context)

@app.route('/profile')
def profile():
    basic_context['url'] = '/profile'
    return profile_page(app, basic_context)

@app.route('/project/<id>')
def project(id):
    basic_context['url'] = '/project/' + id
    return project_page(app, basic_context, id)

@app.route('/projects')
def projects():
    basic_context['url'] = '/projects'
    context = basic_context
    return render_template('projects.html', **context)

@app.route('/project/<id>/add/user')
def project_add_user(id):
    basic_context['url'] = '/project/' + id + '/add/user'
    return project_add_user_page(app, basic_context, id)

@app.route('/project/<id>/add/sensor')
def project_add_sensor(id):
    basic_context['url'] = '/project/' + id + '/add/sensor'
    return project_add_sensor_page(app, basic_context, id)

@app.route('/project/<id>/edit/user/<user_id>')
def project_edit_user(id, user_id):
    basic_context['url'] = '/project/' + id + '/edit/user/' + user_id
    return project_edit_user_page(app, basic_context, id, user_id)

@app.route('/project/<id>/edit/sensor/<sensor_id>')
def project_edit_sensor(id, sensor_id):
    basic_context['url'] = '/project/' + id + '/edit/sensor/' + sensor_id
    return project_edit_sensor_page(app, basic_context, id, sensor_id)

@app.route('/admin')
def project_admin():
    basic_context['url'] = '/admin'
    return project_admin_page(app, basic_context)

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
