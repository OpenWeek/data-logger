from data_logger.models import *

def insert_user(email, first_name, name, admin_level):
    """
    Insert an user in the db
    @args : db - database
    """
    user = User(email=email, first_name=first_name, name=name, admin_level=admin_level)
    db.session.add(User)
    db.session.commit()
    return user

def insert_project(name, data_plan,user_id):
    """
    Insert a project in the db
    @args : db - database
    """
    
    creator = User.query.filter_by(id=user_id).first()

    project = Project(name = name,state=0, data_plan=data_plan, creator = creator)
    db.session.add(project)
    db.session.commit()
    return project

def insert_sensor(sensor_name, client_id, sample_freq, protocol):
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
    return sensor_item


def get_project(project_id):
    return Project.query.filter_by(id=project_id).first()

def get_project_list():
    return Project.query.all()

def format_project_list(plist):
    flist = []
    for p in plist:
        flist.append({"id":p.id,"name":p.name})
    return flist

def get_user_projects(user_id):
    user = User.query.filter_by(id = user_id).first()
    projects = list()

    for m in user.member:
        projects.append(m.of_project)
    return projects

def get_projects_user(project_id):
    project = Project.query.filter_by(id = project_id).first()
    users = list()

    for m in project.member:
        users.append(m.member)
    return projects


def get_project_sensors(project_id):
    sensors = list() 
    project = Project.query.filter_by(id = project_id).first()

    for m in project.sensor_items:
        sensors.append(m.sensor)

    return sensors


