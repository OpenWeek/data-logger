from time import time
import paho.mqtt.client as mqtt
import signal
import argparse
import yaml
#import queries
import rrd_handler
import json
import sys

broker = 'localhost'
port = 1883
keepalive = 300
data = {}
client = "listener"
channel = ""

def signal_handler(signal, frame):
    sys.exit(0)
      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode(encoding='UTF-8',errors='strict')
        data = json.loads(data)
        for k, v in data.items():
            if k == "sensor_id":
                time1 = int(time()) - (len(v) * 20)
                for i in v:
                    args = {}
                    args['time'] = time1 
                    args['value'] = [i['humidity'], i['temperature']]
                    args['client_id'] = k
                    rrd_handler.update_rrd(args)
                    time1 += 20
                    
            elif k == "sensor_id2":
                time1 = int(time()) - (len(v) * 10)
                for i in v:
                    args = {}
                    args['time'] = time1 
                    args['value'] = [i['pressure']]
                    args['client_id'] = k
                    rrd_handler.update_rrd(args)
                    time1 += 10
    except:
        print("Error on message")

            
        
    
    
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from multiple client using mqtt')
    parser.add_argument('--port', '-p', action='store', type=int, help='network port to connect to (default is 1883)')
    parser.add_argument('--host', '-H', action='store', help='mqtt host to connect to (default is localhost)')
    parser.add_argument('--keepalive', '-k', action='store', type=int, help='time while the connection is maintained when no data is transmitted in seconds (default is 300)')
    args = parser.parse_args()

    try:
        with open("mqtt_db_conf.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError as exc:
        print(exc)

    if args.host == None:
        if 'BROKER' in data:
            broker = data['BROKER']
    else:
        broker = args.host

    if args.port == None:
        if 'BROKER_PORT' in data:
            port = data['BROKER_PORT']
    else:
        port = args.port
    
    if args.keepalive == None:
        if 'BROKER_KEEPALIVE' in data:
            keepalive = data['BROKER_KEEPALIVE']
    else:
        keepalive = args.keepalive

    
    signal.signal(signal.SIGINT, signal_handler)
    client = mqtt.Client(client)
    client.username_pw_set("listener", password="password")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.connect(broker, port, keepalive)
    client.subscribe("#", 0)
    client.loop_forever()
