from models import *

def insert_user(db, email, first_name, name, admin_level):
    """
    Insert an user in the db
    @args : db - database
    """
    user = User(email=email, first_name=first_name, name=name, admin_level=admin_level)
    db.session.add(User)
    db.session.commit()

def insert_project(db, name, state, verified_by, data_plan):
    """
    Insert a project in the db
    @args : db - database
    """
    project = Project(name, state, verified_by, data_plan)
    db.session.add(project)
    db.session.commit()

def insert_sensor(db, sensor_name, client_id, sample_freq, protocol):
    """
    Insert a sensor in the db
    @args : db - database
    """
    sensor_item = SensorItem(sensor_name, client_id, sample_freq, protocol)
    db.session.add(sensor_item)
    db.session.commit
