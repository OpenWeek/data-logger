from data_logger.models import *


##Insert

def insert_user(email, first_name, name, pwd, admin_level = 0):
    """
    Insert an user in the db
    """
    user = User(email=email, first_name=first_name, name=name, admin_level=admin_level, pwd=pwd)
    db.session.add(User)
    db.session.commit()
    return user

def insert_project(name, data_plan,user_id):
    """
    Insert a project in the db
    """

    project = Project(name = name,state=0, data_plan=data_plan, creator_id = user_id)
    db.session.add(project)
    db.session.commit()
    return project

def insert_sensor(sensor_name, client_id, sample_freq, protocol):
    """
    Insert a sensor in the db
    """
    sensor_item = SensorItem(sensor_name, sample_freq, protocol)
    db.session.add(sensor_item)
    db.session.commit
    attached = Attached_Sensors(sensor_id = sensor_item.id, client_id = client_id)
    db.session.add(attached)
    db.session.commit()
    return sensor_item

def insert_firmware(path,version,sdk):
    firm=Firmware(path=path,version=version,sdk=sdk)
    db.session.add(firm)
    db.commit()
    return firm

def insert_controller(name, ni2c, nspi,valim,vdata):
    con = Controller(name=name,ni2c=ni2c, nspi=nspi, valim=valim,vdata=vdata)
    db.session.add(con)
    db.commit()
    return con

def insert_client(mac, ip_version, ip, controller, firmware, creator, state = 0, enabled = True):
    client= Client(mac=mac, ip_version=ip_version, ip=ip, controller=controller, firmware=firmware, added_r=creator, firmware_r=firmware, controller_r=controller)
    db.session.add(client)
    db.session.commit()
    return client

##Get

def get_user_id(user_mail):
    return User.query.filter_by(email=user_mail).first().id

def get_users():
    return

def get_project(project_id):
    return Project.query.filter_by(id=project_id).first()

def get_project_list():
    return Project.query.all()

def format_project_list(plist):
    flist = []
    for p in plist:
        flist.append({"id":p.id,"name":p.name})
    return flist

def format_sensors_list(slist):
    flist = []
    for s in slist:
        flist.append({"id":s.id,"sensor_name":s.sensor_name,
        "sample_freq":s.sample_freq,"protocol":s.protocol,"valim":s.valim,
        "vdata":s.vdata})
    return flist

def get_user_projects(user_id):
    user = User.query.filter_by(id = user_id).first()
    projects = list()

    if user.member is None:
        return None
    for m in user.member:
        projects.append(m.of_project)
    return projects

def get_project_users(project_id):
    project = Project.query.filter_by(id = project_id).first()
    users = list()

    for m in project.members:
        users.append(m.member)
    return users


def get_project_clients(project_id):
    client = list()
    project = Project.query.filter_by(id = project_id).first()

    if project.clients is None:
        return None
    for m in project.clients:
        client.append(m.client)

    return client

def get_client_sensors(client_id):
    sensors = dict()
    client = Client.query.filter_by(id=client_id).first()

    if client.sensors is None:
        return None
    for s in client.sensors:
        sensors.append(s.sensoritem)

##Add

def project_add_user(project_id, user_id):
    project = Project.query.filter_by(id = project_id).first()
    user = User.query.filter_by(id = user_id).first()
    member = Member(writable = False, of_project = project, member=user)
    db.session.add(member)
    db.session.commit()

def project_add_client(project_id, client_id):
    member_client = Member_Client(project_id=project_id, client_id=client_id)
    db.session.add(member_client)
    db.commit()

def client_add_sensor(client_id, sensor_id):
    sensor = Attached_Sensor(client_id=client_id, sensoritem_id=sensor_id)
    db.session.add(member_client)
    db.commit()



##Delete:

def del_project(project_id):
    project = Project.query.filter_by(id = project_id).first()
    for c in get_project_clients(project_id):
        for s in get_client_sensors(c.id):
             db.session.delete(s)
        db.session.delete(c)
    db.session.delete(project)
    db.commit()
