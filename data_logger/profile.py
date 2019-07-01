#! /usr/bin/env python3

from flask import Flask, render_template

def profile_page(app):
    context = {'user_name': 'philippe'}
    return render_template('profile.html', **context)
