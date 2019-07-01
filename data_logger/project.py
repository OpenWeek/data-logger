#! /usr/bin/env python3

from flask import Flask, render_template

def project_page(app, id):
    return "Projet %s" % id

def project_add_user_page(app, id):
    return "Projet %s on ajoute un user" % id

def project_add_sensor_page(app, id):
    return "Projet %s on ajoute un senseur" % id

def project_edit_user_page(app, id, user_id):
    return "Projet %s on edite l'user %s" % (id, user_id)

def project_edit_sensor_page(app, id, sensor_id):
    return "Projet %s on edite le senseur %s" % (id, sensor_id)
