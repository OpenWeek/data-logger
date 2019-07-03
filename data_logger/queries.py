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
    sensor_item = SensorItem(sensor_name, sample_freq, protocol)
    db.session.add(sensor_item)
    db.session.commit
    attached = Attached_Sensors(sensor_id = sensor_item.id, client_id = client_id)
    db.session.add(attached)
    db.session.commit()


def get_user_projects(user_id):
    user = User.query.filter(id = user_id).first()
    projects = list()

    for m in user.member:
        projects.append(m.of_project)
    return projects

def get_projects_user(project_id):
    project = Project.query.filter(id = project_id).first()
    users = list()

    for m in project.member:
        users.append(m.member)
    return projects


def get_project_sensors(project_id):
    sensors = list() 
    project = Project.query.filter(id = project_id).first()

    for m in project.sensor_items:
        sensors.append(m.sensor)

    return sensors
