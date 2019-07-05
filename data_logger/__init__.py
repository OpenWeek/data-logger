#! /usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
import data_logger.queries as query

from data_logger.models import *
import data_logger.queries as query
from data_logger.profile import *
from data_logger.admin import *
from data_logger.project import *
from firmware import Nodemcu, Firmware

app = Flask(__name__)
app.config.from_json('config.json')

#app.register_blueprint(projects_page)

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

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'), code = 302)
    else:
        basic_context['url'] = '/login'
        context = basic_context
        return render_template('login.html', **context)

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        userfirstname = request.form['userfirstname']
        email = request.form['email']
        user_id = query.get_user_id(email)
        if user_id is None:
            return redirect(url_for('profile'), code = 303)
        ## TODO: supprimer l'user dans la db
        query.insert_user(email, first_name, name, pwd, basic_context['admin_level'])
        basic_context['user_name'] = username
        basic_context['user_firstname'] = userfirstname
        return redirect(url_for('profile'), code = 303)
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
    return projects_page(app, basic_context)

@app.route('/add/project', methods = ['POST', 'GET'])
def add_project():
    if request.method == 'POST':
        ## TODO: Ajouter nouveau projet à la DB
        name = request.form['name']
        project = query.insert_project(name, "Data zzz", basic_context['user_name'])
        return redirect(url_for('project', id = project.id), code = 303)
    else:
        basic_context['url'] = '/add/project'
        return project_add(app, basic_context)

@app.route('/project/<id>/client/<client_id>/ask/sensor')
def ask_sensor(id, client_id):
    return redirect(url_for('client_show', id=id, client_id=client_id), code = 303)

@app.route('/project/<id>/client/<client_id>')
def client_show(id, client_id):
    sensors = query.get_client_sensors(client_id)
    context = basic_context
    context['sensors'] = query.format_sensors_list(sensors)
    context['project'] = {"id":id}
    context['client'] = {"id":client_id}
    context["sensors_type"] = query.get_sensors_type()
    #return context["sensors_type"][0];
    return render_template('sensors.html', **context), 200

@app.route('/project/<id>/client/<client_id>/flash')
def client_flash(id, client_id):
    #TODO ; flash(client_id)
    no = Nodemcu()
    modules = no.load_modules()
    
    return redirect(url_for('project', id=id), code = 302)

#### ADD SECTION

@app.route('/project/<id>/add/user', methods = ['POST', 'GET'])
def project_add_user(id):
    if request.method == 'POST':
        email = request.form['mail']
        user_id = query.get_user_id(email)
        if user_id is None:
            return redirect(url_for('project', id=id), 303)
        user = query.project_add_user(id,user_id)
        if user is None:
            return "400 User not found"
        return redirect(url_for('project_edit_user', id = id, user_id = user.id), code = 303)
    return "400 Bad Request"

@app.route('/project/<id>/add/client', methods = ['POST', 'GET'])
def project_add_client(id):
    if basic_context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    else:
        if request.method == 'POST':
            ## TODO: adapter au nouveau code
            clientIP = request.form['clientIP']
            clientMac = request.form['clientMac']
            #clientFirmware = request.form['clientFirmware']
            state = 0
            if basic_context['user_privilege'] == "admin":
                state = 1
            # TODO: Fonction pour détecter si IPv4
            client = query.insert_client(clientMac, 4, clientIP, Firmware(path = '/etc', version = 42, sdk = "v15"), basic_context['user_id'],id ,state=state)
            query.project_add_client(id,client.id)
            return redirect(url_for('client_show', id = id, client_id = client.id), code = 303)
        else:
            return render_template('400.html', **context), 400

@app.route('/project/<id>/client/<client_id>/add/sensor', methods = ['POST', 'GET'])
def project_add_sensor(id, client_id):
    if request.method == 'POST':
        ## TODO: Faire quelque chose avec sensortype et sensor_subtype
        sensorname = request.form['sensor_name']
        sensortype = request.form['sensor_type']
        sensorsubtype = request.form.getlist('sensor_subtype')
        sensorfreq = request.form.getlist('sensor_freq')
        query.insert_sensor(sensorname, client_id, ";".join(str(x) for x in sensorfreq), ";".join(str(x) for x in sensorsubtype))
        ## TODO: le mettre dans la db
        return redirect(url_for('client_show', id = id, client_id = client_id), code = 303)
    else:
        return render_template('400.html', **context), 400

#### EDIT SECTION

@app.route('/project/<id>/edit/user/<user_id>', methods = ['POST', 'GET'])
def project_edit_user(id, user_id):
    if request.method == 'POST':
        username = request.form['username']
        ## TODO: le modifier dans la db
        return "501 Not Implemented", 501
        return redirect(url_for('project_edit_user', id = id, user_id = user_id), code = 201)
    else:
        return render_template('400.html', **context), 400

#### REMOVE SECTION

@app.route('/remove/project/<id>', methods = ['POST', 'GET'])
def remove_project(id):
    if request.method == 'POST':
        ## TODO: Remove project dans la DB
        query.del_project(id)
        return redirect(url_for('projects'), code = 302)
    else:
        return render_template('400.html', **context), 400

@app.route('/project/<id>/remove/user/<user_id>', methods = ['POST', 'GET'])
def project_remove_user(id, user_id):
    if request.method == 'POST':
        ## TODO: Remove user dans la DB
        return "501 Not Implemented", 501
        return redirect(url_for('project', id = id), code = 200)
    else:
        return render_template('400.html', **context), 400

@app.route('/project/<id>/remove/client/<client_id>', methods = ['POST', 'GET'])
def project_remove_client(id, client_id):
    if request.method == 'POST':
        ## TODO: Remove client dans la DB
        return "501 Not Implemented", 501
        return redirect(url_for('project', id = id), code = 200)
    else:
        return render_template('400.html', **context), 400

@app.route('/project/<id>/client/<client_id>/remove/sensor/<sensor_id>', methods = ['POST', 'GET'])
def project_remove_sensor(id, client_id, sensor_id):
    if request.method == 'POST':
        query.del_sensor(client_id,sensor_id)
        return redirect(url_for('project', id = id), code = 200)
    else:
        return render_template('400.html', **context), 400

## ADMIN SIDE

@app.route('/admin/users')
def project_users_admin():
    basic_context['url'] = '/admin/users'
    context = basic_context.copy()
    context['all_users'] = query.format_users(query.get_users())
    return project_admin_users_page(app, context)

@app.route('/admin/projects')
def project_projects_admin():
    basic_context['url'] = '/admin/projects'
    return project_admin_projects_page(app, basic_context)

@app.route('/admin/approve/project/<project_id>', methods = ['POST', 'GET'])
def admin_approve_project(project_id):
    if request.method == 'POST':
        query.project_approve(project_id)
        return "ok", 200
    return render_template('400.html', **context), 400

@app.route('/admin/reject/project/<project_id>', methods = ['POST', 'GET'])
def admin_reject_project(project_id):
    if request.method == 'POST':
        query.project_reject(project_id)
        return "ok", 200
    return render_template('400.html', **context), 400

@app.route('/admin/approve/sensors/project/<project_id>', methods = ['POST', 'GET'])
def admin_approve_sensor(project_id):
    if request.method == 'POST':
        return "501 Not Implemented", 501
    return render_template('400.html', **context), 400

@app.route('/admin/reject/sensors/project/<project_id>', methods = ['POST', 'GET'])
def admin_reject_sensor(project_id):
    if request.method == 'POST':
        return "501 Not Implemented", 501
    return render_template('400.html', **context), 400

@app.route('/admin/add/user', methods = ['POST', 'GET'])
def admin_add_user():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        first_name = request.form['first_name']
        password = request.form['password']
        admin_level_str = request.form['admin_level']
        if admin_level_str == 'admin':
            admin_level = 2
        elif admin_level_str == 'creator':
            admin_level = 1
        else:
            admin_level = 0
        query.insert_user(email, first_name, name, password, admin_level)
        return redirect(url_for('project_users_admin'), code = 303)
    return render_template('400.html', **context), 400

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
