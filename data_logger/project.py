#! /usr/bin/env python3

from flask import Flask, render_template
import data_logger.queries as queries

def project_page(app, basic_context, id):
    context = basic_context
    context['name'] = "project-"+id
    context['id'] = id
    # TODO: changer en vraies données de la DB
    context['state'] = "Accepted"
    context['data_plan'] = 'some data_plan'
    context['verified_by'] = "Michel"
    context['members'] = [{'name':'Philippe', 'id':'1'},{'name':'Tom', 'id': '2'}]
    context['sensors'] = [{'name':'bureau', 'id':'1'},{'name':'cafet', 'id': '2'}]
    context['sensors_type'] = [{'sensor_name':'sol', 'id':'3', 'client_id':'2', 'sample_freq':'15', 'protocol':'QTT'},{'sensor_name':'tableau', 'id': '4', 'client_id':'1', 'sample_freq':'30', 'protocol':'QTT'}]
    
    return render_template('project.html', **context)

def project_add_user_page(app, basic_context, id):
    context = basic_context
    if context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    context['members'] = [{'name':'Jean-François', 'id':'3'},{'name':'Tom', 'id': '2'}]
    return render_template('addUser.html', **context)

def project_add_sensor_page(app, basic_context, id):
    context = basic_context
    if context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    context['sensors'] = [{'sensor_name':'sol', 'id':'3', 'client_id':'2', 'sample_freq':'15', 'protocol':'QTT'},{'sensor_name':'tableau', 'id': '4', 'client_id':'1', 'sample_freq':'30', 'protocol':'QTT'}]
    return render_template('addSensor.html', **context)

def project_edit_user_page(app, basic_context, id, user_id):
    context = basic_context
    context['members'] = [{'name':'Philippe', 'id':'1'},{'name':'Jean-François', 'id':'3'},{'name':'Tom', 'id': '2'}]
    return render_template('addUser.html', **context)

def project_edit_sensor_page(app, basic_context, id, sensor_id):
    context = basic_context
    if context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    context['sensors'] = [{'sensor_name':'bureau', 'id':'1', 'client_id':'1', 'sample_freq':'10', 'protocol':'QTT'},{'sensor_name':'cafet', 'id': '2', 'client_id':'1', 'sample_freq':'25', 'protocol':'QTT'},{'sensor_name':'sol', 'id':'3', 'client_id':'1', 'sample_freq':'15', 'protocol':'QTT'},{'sensor_name':'tableau', 'id': '4', 'client_id':'1', 'sample_freq':'30', 'protocol':'QTT'}]
    return render_template('addSensor.html', **context)

def project_add(app, basic_context):
    context = basic_context

    context['name'] = "new project"
    context['data_plan'] = "some data_plan"
    context['members'] = []
    context['sensors'] = []

    project = queries.insert_project(context['name'], context['data_plan'],context['user_id'])
    context['id'] = project.id
    context['state'] = project.state

    basic_context['project_list'] = queries.format_project_list(queries.get_project_list())

    return render_template('projects.html', **context)
