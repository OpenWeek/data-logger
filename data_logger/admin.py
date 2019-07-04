#! /usr/bin/env python3

from flask import Flask, render_template

def project_admin_projects_page(app, basic_context):
    if basic_context['user_privilege'] == 'admin':
        context = basic_context
        context['projects_ask_approval'] = [{'name':'Red', 'state':'pending', 'verified_by':'Jean-François', 'data_plan':'gné'}]
        context['projects_ask_sensor'] = [{'name':'Précipitations Réaumur', 'state':'pending', 'verified_by':'Olivier', 'data_plan':'Y291Y291IHBldGl0ZSBwZXJydWNoZQo='}]
        return render_template('adminProjects.html', **context)
    else:
        return render_template('403.html', **context), 403


def project_admin_users_page(app, basic_context):
    if basic_context['user_privilege'] == 'admin':
        context = basic_context
        context['all_users'] = [{'email':'adolph_h@gmail.com','name':'Hitler','first_name':'Adolph','admin_level':'admin'}, {'email':'adolph_h2@gmail.com','name':'Hitler2','first_name':'Adolph2','admin_level':'user'}]
        return render_template('adminUsers.html', **context)
    else:
        return render_template('403.html', **context), 403
