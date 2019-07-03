#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
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

# GET METHODS

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

@app.route('/project/<id>/add/user', methods = ['POST', 'GET'])
def project_add_user(id):
    if request.method == 'POST':
        username = request.form('username')
        ## TODO: le mettre dans la db
        return redirect(url_for('project_edit_user', id = id, user_id = 42), code = 201)
    else:
        basic_context['url'] = '/project/' + id + '/add/user'
        return project_add_user_page(app, basic_context, id)


@app.route('/project/<id>/add/sensor', methods = ['POST', 'GET'])
def project_add_sensor(id):
    if request.method == 'POST':
        sensorname = request.form('sensorname')
        sensortype = request.form('sensortype')
        ## TODO: le mettre dans la db
        return redirect(url_for('project_edit_sensor', id = id, sensor_id = 69), code = 201)
    else:
        basic_context['url'] = '/project/' + id + '/add/sensor'
        return project_add_sensor_page(app, basic_context, id)

@app.route('/project/<id>/edit/user/<user_id>', methods = ['POST', 'GET'])
def project_edit_user(id, user_id):
    if request.method == 'POST':
        username = request.form('username')
        ## TODO: le modifier dans la db
        return redirect(url_for('project_edit_user', id = id, user_id = user_id), code = 200)
    else:
        basic_context['url'] = '/project/' + id + '/edit/user/' + user_id
        return project_edit_user_page(app, basic_context, id, user_id)

@app.route('/project/<id>/edit/sensor/<sensor_id>', methods = ['POST', 'GET'])
def project_edit_sensor(id, sensor_id):
    if request.method == 'POST':
        sensorname = request.form('sensorname')
        sensortype = request.form('sensortype')
        ## TODO: le modifier dans la db
        return redirect(url_for('project_edit_sensor', id = id, sensor_id = sensor_id), code = 200)
    else:
        basic_context['url'] = '/project/' + id + '/edit/sensor/' + sensor_id
        return project_edit_sensor_page(app, basic_context, id, sensor_id)

@app.route('/add/project', methods = ['POST', 'GET'])
def add_project():
    if request.method == 'POST':
        return redirect(url_for('project', id = 1), code = 201)
    else:
        basic_context['url'] = '/add/project'
        return project_add(app, basic_context)

@app.route('/admin')
def project_admin():
    basic_context['url'] = '/admin'
    return project_admin_page(app, basic_context)

# ERROR METHODS

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
