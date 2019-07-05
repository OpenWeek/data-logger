#! /usr/bin/env python3

from flask import Flask, render_template
import data_logger.queries as query


def project_admin_projects_page(app, basic_context):
    if basic_context['user_privilege'] == 'admin':
        context = basic_context
        context['projects_ask_approval'] = query.get_project_approval_list()
        context['projects_ask_sensor'] = [{'name':'Précipitations Réaumur', 'state':'pending', 'verified_by':'Olivier', 'data_plan':'Y291Y291IHBldGl0ZSBwZXJydWNoZQo='}]
        return render_template('adminProjects.html', **context)
    else:
        return render_template('403.html', **context), 403


def project_admin_users_page(app, context):
    if context['user_privilege'] == 'admin':
        return render_template('adminUsers.html', **context)
    else:
        return render_template('403.html', **context), 403
