#! /usr/bin/env python3

from flask import Flask, render_template

def profile_page(app, basic_context):
    context = basic_context
    context['user'] = {'email':context['user_email'], 'first_name':context['user_firstname'], 'name':context['user_name'], 'rank':context['user_privilege']}
    return render_template('profile.html', **context)
