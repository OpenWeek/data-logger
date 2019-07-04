from flask import Blueprint, Flask, render_template
import data_logger.queries as queries


projects_page = Blueprint('projects', __name__)


@projects_page.route('/projects', methods=['GET'])
def projects():
    context = {}
    return render_template('projects.html', **context)


@projects_page.route('/project/<id>', methods=['GET'])
def project_page(id):
    context = {}
    return render_template('project.html', **context)


def project_add_user_page(app, basic_context, id):
    context = basic_context
    context['members'] = [{'name':'Jean-François', 'id':'3'},{'name':'Tom', 'id': '2'}]
    return render_template('addUser.html', **context)

def project_add_sensor_page(app, basic_context, id):
    context = basic_context
    if context['user_privilege'] == 'user':
        return render_template('403.html', **context), 403
    context['sensors'] = [{'sensor_name':'sol', 'id':'3', 'client_id':'2', 'sample_freq':'15', 'protocol':'QTT'},{'sensor_name':'tableau', 'id': '4', 'client_id':'1', 'sample_freq':'30', 'protocol':'QTT'}]
    return render_template('addSensor.html', **context)

def project_add_client_page(app, basic_context):
    return nil

def project_edit_user_page(app, basic_context, id, user_id):
    context = basic_context
    context['members'] = [{'name':'Philippe', 'id':'1'},{'name':'Jean-François', 'id':'3'},{'name':'Tom', 'id': '2'}]
    return render_template('addUser.html', **context)

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
