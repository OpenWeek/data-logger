from jinja2 import Template
import json
import os
import platform
from subprocess import Popen, PIPE

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
    for sensor_name in required_measures:
        flash_data[sensor_name] = data[sensor_name]
        flash_data[sensor_name]["records"] = []

        # build an array containing boolean value corresponding to the item in the array of the possible measurment
        for measure in data[sensor_name]["value"]:
            flash_data[sensor_name]["records"].append(measure in required_measures[sensor_name])

    return flash_data


def get_port():
    p = None
    if os.name == "nt":
        p = "COM5"
    else:
        tag = "usbserial" if platform.system() == "Darwin" else "tty"

        p = Popen(["ls", "/dev"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        r = output.decode("utf-8").split("\n")
        r = [s for s in r if tag in s]
        p = "/dev/" + r[-1]
    print("port:", p)
    return p


class Code:
    root = "./code_client/"
    tmp_file_name = "tmp.lua"

    def __init__(self, required_measures):
        self.template_file_main = read(self.root + "template.lua")
        self.template_file_init = read(self.root + "init_template.lua")
        self.data = json.loads(read(self.root + "sensors.json"))

        self.flash_data = build_flash_data(self.data, required_measures)

        self.tmp_file_main_path = self.root + self.tmp_file_name
        self.tmp_file_init_path = self.root + "init.lua"

    def generate_code(self):
        template = Template(self.template_file_main)
        return template.render(data=self.flash_data)

    def generate_init(self):
        template = Template(self.template_file_init)
        return template.render(file_name=self.tmp_file_name)

    def write_code(self, file_path):
        write(file_path, self.generate_code())

    def upload_code(self):

        self.write_code(self.tmp_file_main_path)
        write(self.tmp_file_init_path, self.generate_init())
        uploader = nu.Uploader(port=get_port(), baud=115200)
        if uploader.prepare():
            uploader.write_file(self.tmp_file_main_path, self.tmp_file_name, "none")
            uploader.write_file(self.tmp_file_init_path, "init.lua", "none")
            uploader.write_file(self.root + "json.lua", "json.lua", "none")
        else:
            print("ERR: fatal error while preparing nodemcu for reception")

        if DEL:
            os.remove(self.tmp_file_main_path)
            os.remove(self.tmp_file_init_path)


def main():

    required_measures = {
        "bme280": ["temperature", "humidity"]
    }

    c = Code(required_measures)
    c.upload_code()


if __name__ == "__main__":
    main()
