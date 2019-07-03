#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
from data_logger.models import db
from data_logger.profile import *
from data_logger.project import *
from data_logger.admin import *
app = Flask(__name__)
app.config.from_json('config.json')
db.init_app(app)

project_list = [{"id":'1',"name":'Température salle Intel', "status":'approved'}, {"id":'22',"name":'Précipitations salle Intel', "status":'pending'},{"id":'33' ,"name":'Précipitations salle Paul Otlet', "status":'refused'}]
user_name = 'Dupont'
user_firstname = 'Pierre'
user_privilege = 'admin'
admin_level = 'admin'
user_email = 'philippe@uclouvain.be'
user_id = 44
basic_context = {}
basic_context['user_name'] = user_name
basic_context['user_firstname'] = user_firstname
basic_context['user_privilege'] = user_privilege
basic_context['admin_level'] = admin_level
basic_context['user_email'] = user_name
basic_context['project_list'] = project_list
basic_context['user_id'] = user_id

# GET METHODS

@app.route('/')
def index():
    basic_context['url'] = '/'
    context = basic_context
    return render_template('index.html', **context)

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        userfirstname = request.form['userfirstname']
        email = request.form['email']
        ## TODO: CHANGER DONNEE DANS BDD
        return redirect(url_for('profile'), code = 201)
    else:
        basic_context['url'] = '/profile'
        return profile_page(app, basic_context)

## PROJECT SIDE

@app.route('/project/<id>')
def project(id):
    basic_context['url'] = '/project/' + id
    return project_page(app, basic_context, id)

@app.route('/projects')
def projects():
    basic_context['url'] = '/projects'
    context = basic_context
    return render_template('projects.html', **context)

@app.route('/add/project', methods = ['POST', 'GET'])
def add_project():
    if request.method == 'POST':
        ## TODO: Ajouter nouveau projet à la DB
        return redirect(url_for('project', id = 1), code = 303)
    else:
        basic_context['url'] = '/add/project'
        return project_add(app, basic_context)

@app.route('/project/<id>/ask/sensor', methods = ['POST', 'GET'])
def ask_sensor(id):
    if request.method == 'POST':
        return redirect(url_for('project', id=id), code = 200)
    pass

@app.route('/project/<id>/client/<client_id>')
def client_show(id, client_id):
    pass

#### ADD SECTION

@app.route('/project/<id>/add/user', methods = ['POST', 'GET'])
def project_add_user(id):
    if request.method == 'POST':
        email = request.form['mail']
        user = query.project_add_user(id,query.get_user_id(email))
        return redirect(url_for('project_edit_user', id = id, user_id = user.id), code = 303)
    else:
        basic_context['url'] = '/project/' + id + '/add/user'
        return project_add_user_page(app, basic_context, id)

@app.route('/project/<id>/add/client', methods = ['POST', 'GET'])
def project_add_client(id):
    if basic_context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    else:
        if request.method == 'POST':
            ## TODO: adapter au nouveau code
            return redirect(url_for('project_add_client', id = id), code = 202)
        else:
            return "Ajouter client du projet %s" % id

@app.route('/project/<id>/client/<client_id>/add/sensor', methods = ['POST', 'GET'])
def project_add_sensor(id, client_id):
    if request.method == 'POST':
        sensorname = request.form['sensorname']
        sensortype = request.form['sensortype']
        ## TODO: le mettre dans la db
        return redirect(url_for('client_show', id = id, client_id = client_id), code = 303)
    else:
        basic_context['url'] = '/project/' + id + '/add/sensor'
        return project_add_sensor_page(app, basic_context, id)

#### EDIT SECTION

@app.route('/project/<id>/edit/user/<user_id>', methods = ['POST', 'GET'])
def project_edit_user(id, user_id):
    if request.method == 'POST':
        username = request.form['username']
        ## TODO: le modifier dans la db
        return redirect(url_for('project_edit_user', id = id, user_id = user_id), code = 201)
    else:
        basic_context['url'] = '/project/' + id + '/edit/user/' + user_id
        return project_edit_user_page(app, basic_context, id, user_id)

#### REMOVE SECTION

@app.route('/remove/project/<id>')
def remove_project(id):
    ## TODO: Remove project dans la DB
    pass

@app.route('/project/<id>/remove/user/<user_id>', methods = ['POST', 'GET'])
def project_remove_user(id, user_id):
    ## TODO: Remove user dans la DB
    pass

@app.route('/project/<id>/remove/client/<client_id>', methods = ['POST', 'GET'])
def project_remove_client(id, client_id):
    ## TODO: Remove client dans la DB
    pass

@app.route('/project/<id>/client/<client_id>/remove/sensor/<sensor_id>', methods = ['POST', 'GET'])
def project_remove_sensor(id, client_id, sensor_id):
    ## TODO: Remove sensor dans la DB
    pass

## ADMIN SIDE

@app.route('/admin')
def project_admin():
    basic_context['url'] = '/admin'
    return project_admin_page(app, basic_context)

@app.route('/admin/approve/project/<project_id>')
def admin_approve_project(project_id):
    pass

@app.route('/admin/reject/project/<project_id>')
def admin_reject_project(project_id):
    pass

@app.route('/admin/approve/sensors/project/<project_id>')
def admin_approve_sensor(project_id):
    pass

@app.route('/admin/reject/sensors/project/<project_id>')
def admin_reject_sensor(project_id):
    pass



## OTHER SIDE

@app.route('/logout')
def logout():
    basic_context['url'] = '/logout'
    ## TODO: modifier les privilèges
    return "You have been succesfully disconnected"

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
