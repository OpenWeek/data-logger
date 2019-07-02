import pytest
from data_logger.models import *
from data_logger import app

app.app_context().push()
db.create_all()

def test_User():
    user1 = User(name="test_user",first_name="1",email="1@1.1",admin_level=0)
    user2 = User(name="test_user",first_name="2",email="2@2.2",admin_level=0)
    user3 = User(name="test_user",first_name="3",email="3@3.3",admin_level=1)
    try:
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        
        db.session.delete(user1)
        db.session.delete(user2)
        db.session.delete(user3)
        db.session.commit() 
        assert True
    except :
        assert False

def test_Client():
    user1 = User(name="test_user",first_name="1",email="1@1.1",admin_level=0)
    user3 = User(name="test_user",first_name="3",email="3@3.3",admin_level=1)
    firmware1 = Firmware(path="./etc",version=1,sdk="1")
    controller1 = Controller(name="controler1",ni2c=1,nspi=1,valim=5.0,vdata=5.0)
    client1 = Client(state=0,enabled=True, mac="1111",ip_version=1,ip="1.1.1",controller=controller1,firmware=firmware1,added_r=user1,verified_r=user3)


    try:
        db.session.add(user1)
        db.session.add(user3)
        db.session.add(firmware1)
        db.session.add(controller1)
        db.session.add(client1)
        db.session.commit()
        
        db.session.delete(user1)
        db.session.delete(user3)
        db.session.delete(client1)
        db.session.delete(firmware1)
        db.session.delete(controller1)
        db.session.commit()
        assert True
    except : 
        assert False
