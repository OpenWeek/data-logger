from flask import Blueprint, Flask, render_template
import data_logger.queries as query

#projects_page = Blueprint('projects', __name__)
"""
@projects_page.route('/projects', methods=['GET'])
def projects():
    context = {}
    context['url'] = '/projects'
    return render_template('projects.html', **context)


@projects_page.route('/project/<id>', methods=['GET'])
def project_page(id):
    context = {}
    context['url'] = '/project/' + id
    return render_template('project.html', **context)
"""

def project_page(app, basic_context, id):
    context = basic_context
    project = query.get_project(id)

    context['name'] = project.name
    context['id'] = id
    # TODO: changer en vraies données de la DB
    context['state'] = project.state
    context['data_plan'] = project.data_plan
    context['verified_by'] = project.verified_by
    context['members'] = query.get_project_users(id)
    context['clients'] = query.get_project_clients(id)
    return render_template('project.html', **context)

def projects_page(app, basic_context):
    context = basic_context
    context['project_list'] = query.get_project_list()
    return render_template('projects.html', **context)

def project_add(app, basic_context):
    context = basic_context

    context['name'] = "new project"
    context['data_plan'] = "some data_plan"
    context['members'] = []
    context['sensors'] = []

    project = query.insert_project(context['name'], context['data_plan'],context['user_id'])
    context['id'] = project.id
    context['state'] = project.state

    basic_context['project_list'] = query.format_project_list(query.get_project_list())

    return render_template('projects.html', **context)
