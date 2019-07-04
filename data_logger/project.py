from flask import Blueprint, Flask, render_template
import data_logger.queries as queries

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
