from flask_sqlalchemy import SQLAlchemy
from enum import Enum


db = SQLAlchemy()


class Admin_level(Enum):
    USER = 0
    CREATOR = 1
    ADMIN = 2


class SensorProtocol(Enum):
    I2C = 0
    SPI = 1
    ONEWIRE = 2


class SDK(Enum):
    NODEMCU = 0
    MICROPYTHON = 1


class Voltage(Enum):
    V5 = 5.0
    V3 = 3.3


class State(Enum):
    PENDING = 0
    ACCEPTED = 1
    REFUSED = 2


class ClientState(Enum):
    PENDING = 0
    ACCEPTED  = 1
    FLASHED = 2
    READY = 3


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    admin_level = db.Column(db.Integer, nullable=False)

    #added = db.relationship('Client', backref='added_clients', foreign_keys=['added_by'], lazy=True)
    #client_verified = db.relationship('Client', backref='verified_client',foreign_keys=['verified_by'], lazy=True)


    member = db.relationship('Member', backref='member', lazy=True)
    
    
    __table_args__ = ({'sqlite_autoincrement': True},)


class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    ni2c = db.Column(db.Integer, nullable=False)
    nspi= db.Column(db.Integer, nullable=False)
    valim = db.Column(db.Float, nullable=False)
    vdata = db.Column(db.Float, nullable=False)

    clients = db.relationship('Client', backref='controller', lazy=True)

    __table_args__ = ({'sqlite_autoincrement': True},)


class Firmware(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    path = db.Column(db.String(120), unique=True, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    sdk = db.Column(db.String(20), nullable=False)


    clients = db.relationship('Client', backref='firmware', lazy=True)

    __table_args__ = ({'sqlite_autoincrement': True},)

    def __repr__(self):
        return '<Firmware {} {}>'.format(repr(self.name), repr(self.version))


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    valim = db.Column(db.Float, nullable=False, default=Voltage.V5)
    vdata = db.Column(db.Float, nullable=False, default=Voltage.V3)

    instances = db.relationship('SensorItem', backref='sensor', lazy=True)
    protocols = db.relationship('Sensor_Protocols', backref='sensor', lazy=True)
    
    __table_args__ = ({'sqlite_autoincrement': True},)


class Sensor_Protocols(db.Model):
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), primary_key=True, nullable=False)
    protocol = db.Column(db.Integer, primary_key=True, nullable=False)
    #add relationship to Sensor



    # add constraint on correct values ?
    # __table_args__ = (db.CheckConstraint())


class SensorItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    samp_freq = db.Column(db.Float, nullable=False)
    protocol = db.Column(db.Integer, nullable=False)

    sensor_name = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    sensor_name_r = db.relationship('Sensor', backref='sensor', lazy=True)

    attached_sensors = db.relationship('Attached_Sensors', backref='sensoritem', lazy=True)

    __table_args__ = ({'sqlite_autoincrement': True},)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    state = db.Column(db.Integer, nullable=False, default=State.PENDING)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    data_plan = db.Column(db.String(300), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    clients = db.relationship('Member_Client', backref='project', lazy=True) 

    creator = db.relationship('User', backref="created",foreign_keys=[creator_id],lazy=True) 
    verified_r = db.relationship('User', backref='verified', foreign_keys=[verified_by],lazy=True)
    deleted_at = db.Column(db.Date, nullable=True)
    #members = db.relationship('User', backref='members', lazy=True)
    #verifier = db.relationship('User', backref='verified_by', lazy=True)


    __table_args__ = ({'sqlite_autoincrement': True},)


class Member(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True, nullable=False)
    writable = db.Column(db.Boolean, nullable=False, default=False)
    
    #member = db.relationship('User',backref="member_of", lazy = True)
    of_project = db.relationship('Project', backref="members",lazy = True)
    


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    state = db.Column(db.Integer, nullable=False, default=ClientState.PENDING)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    mac = db.Column(db.String(17), nullable=False)
    ip_version = db.Column(db.Integer, nullable=False, default=4)
    ip = db.Column(db.String(40), nullable=False)

    controller_name = db.Column(db.Integer, db.ForeignKey('controller.id'), nullable=False)
    firmware_id = db.Column(db.Integer, db.ForeignKey('firmware.id'), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    verified_r = db.relationship('User', backref="verified_client", foreign_keys=[verified_by],lazy=True)
    added_r = db.relationship('User', backref="added_client", foreign_keys=[added_by], lazy=True)
    sensors = db.relationship('Attached_Sensors', backref='client', lazy=True)
    firmware_r = db.relationship('Firmware', backref='firm_client',foreign_keys=[firmware_id], lazy=True)
    controller_r = db.relationship('Controller', backref='control_client', lazy=True)

    __table_args__ = ({'sqlite_autoincrement': True},)


class Attached_Sensors(db.Model):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False, primary_key=True)
    sensoritem_id = db.Column(db.Integer, db.ForeignKey(SensorItem.id), nullable=False, primary_key=True)

class Member_Client(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id), nullable= False, primary_key=True)
    client = db.relationship('Client', backref='project', lazy=True)
