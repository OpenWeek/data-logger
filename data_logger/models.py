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

    added = db.relationship('Client', backref='user', lazy=True)
    #client_verified = db.relationship('Client', backref='user', lazy=True)
    project_verified = db.relationship('Project', backref='user', lazy=True)
    member = db.relationship('Member', backref='user', lazy=True)

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

    # add constraint on correct values ?
    # __table_args__ = (db.CheckConstraint())


class SensorItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    samp_freq = db.Column(db.Float, nullable=False)
    protocol = db.Column(db.Integer, nullable=False)

    sensor_name = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)

    # attached_sensors = db.relationship('Attached_Sensors', backref='sensoritem', lazy=True)

    __table_args__ = ({'sqlite_autoincrement': True},)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    state = db.Column(db.Integer, nullable=False, default=State.PENDING)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    data_plan = db.Column(db.String(300), nullable=False)

    clients = db.relationship('Client', backref='project', lazy=True)
    
    __table_args__ = ({'sqlite_autoincrement': True},)


class Member(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True, nullable=False)
    writable = db.Column(db.Boolean, nullable=False, default=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    state = db.Column(db.Integer, nullable=False, default=ClientState.PENDING)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    mac = db.Column(db.String(17), nullable=False)
    ip_version = db.Column(db.Integer, nullable=False, default=4)
    ip = db.Column(db.String(40), nullable=False)

    #sensors = db.relationship('Attached_Sensors', backref='client', lazy=True)

    controller_name = db.Column(db.Integer, db.ForeignKey('controller.id'), nullable=False)
    firmware_id = db.Column(db.Integer, db.ForeignKey('firmware.id'), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    # verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    __table_args__ = ({'sqlite_autoincrement': True},)

"""
class Attached_Sensors(db.Model):
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False, primary_key=True)
    sensoritem = db.Column(db.Integer, db.ForeignKey('sensoritem.id'), nullable=False, primary_key=True)
"""
