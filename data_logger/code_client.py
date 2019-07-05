#! /usr/bin/env python

from jinja2 import Template
import json
from os import name, listdir
import platform

from copy import deepcopy as dc
import nodemcu_uploader as nu

DEL = True # if true remove temporary generated file

# Utils function
def read(file_name):
    fh = open(file_name, "r")
    content = fh.read()
    fh.close()
    return content


def write(file_name, data):
    fh = open(file_name, "w")
    fh.write(data)
    fh.close()


def build_flash_data(data, required_measures):
    flash_data = {}
    for sensor_id in required_measures:
        sensor_type = required_measures[sensor_id]["type"]
        sensor_period = required_measures[sensor_id]["period"]

        flash_data[sensor_id] = dc(data[sensor_type])
        flash_data[sensor_id]["records"] = []
        flash_data[sensor_id]["type"] = sensor_type
        flash_data[sensor_id]["period"] = sensor_period

        # build an array containing boolean value corresponding to the item in the array of the possible measurment
        for measure in data[sensor_type]["value"]:
            flash_data[sensor_id]["records"].append(measure in required_measures[sensor_id]["measure"])

    return flash_data


def get_port():
    p = None
    if name == "nt":
        p = "COM5"
    else:
        tag = "usbserial" if platform.system() == "Darwin" else "USB"
        result = [i for i in listdir("/dev") if tag in i]
        if len(result) > 0:
            p = "/dev/" + result[0]
    return p


class Code:
    root = "./code_client/"
    tmp_file_name = "tmp.lua"

    def __init__(self, client_id, required_measures):
        self.template_file_main = read(self.root + "template.lua")
        self.template_file_init = read(self.root + "init_template.lua")
        self.template_file_time = read(self.root + "time_template")
        self.template_file_measures = read(self.root + "measures_template")
        self.data = json.loads(read(self.root + "sensors.json"))

        self.flash_data = build_flash_data(self.data, required_measures)
        self.client_id = client_id

        self.tmp_file_main_path = self.root + self.tmp_file_name
        self.tmp_file_init_path = self.root + "init.lua"
        self.tmp_file_time_path = self.root + "time.json"
        self.tmp_file_measures_path = self.root + "measures.json"

    def generate_code(self):
        template = Template(self.template_file_main)
        return template.render(data=self.flash_data, client_id=self.client_id)

    def generate_init(self):
        template = Template(self.template_file_init)
        return template.render(file_name=self.tmp_file_name)

    def generate_time(self):
        template = Template(self.template_file_time)
        return template.render(data=self.flash_data)
    
    def generate_measures(self):
        template = Template(self.template_file_measures)
        return template.render(data=self.flash_data)

    def write_code(self, file_path):
        write(file_path, self.generate_code())

    def upload_code(self):

        self.write_code(self.tmp_file_main_path)
        write(self.tmp_file_init_path, self.generate_init())
        write(self.tmp_file_time_path, self.generate_time())
        write(self.tmp_file_measures_path, self.generate_measures())

        port = get_port()
        if port is not None:
            uploader = nu.Uploader(port=port, baud=115200)
            if uploader.prepare():
                uploader.write_file(self.tmp_file_main_path, self.tmp_file_name, "none")
                uploader.write_file(self.tmp_file_init_path, "init.lua", "none")
                uploader.write_file(self.tmp_file_time_path, "time.json", "none")
                uploader.write_file(self.tmp_file_measures_path, "measures.json", "none")
                uploader.write_file(self.root + "json.lua", "json.lua", "none")
            else:
                print("ERR: fatal error while preparing nodemcu for reception")
        else:
            print("No device detected")

        if DEL:
            os.remove(self.tmp_file_main_path)
            os.remove(self.tmp_file_init_path)
            os.remove(self.tmp_file_time_path)
            os.remove(self.tmp_file_measures_path)


def main():

    client_id = "client_id"
    required_measures = {
        "sensor_id": {
            "type": "bme280",
            "period": 20, 
            "measure": ["temperature", "humidity"]
        },
        "sensor_id2": {
            "type": "bme280",
            "period": 10,
            "measure": ["pressure"]
        }
    }

    c = Code(client_id, required_measures)
    c.upload_code()
    # print(c.generate_code())


if __name__ == "__main__":
    main()
