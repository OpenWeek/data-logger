#! /usr/bin/env python3

from flask import Flask, render_template

def profile_page(app, basic_context):
    context = basic_context
    context['user'] = [{'email':'philippe@uclouvain.be', 'first_name':'philippe', 'name':'Dupont', 'admin'}]
    return render_template('profile.html', **context)
