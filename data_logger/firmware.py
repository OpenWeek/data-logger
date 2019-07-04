from subprocess import run
from re import sub
from abc import ABC
from os import listdir, mkdir


class Firmware: 
    
  base_firmware_dir = '/var/www/data-logger/data_logger/firmware/'
  container = ''
  bin_path = ''
  command = []

  def __init__(self,name=''):
    if name != '':
      self.container = '{0}-firmware'.format(name)
      self.bin_path = '/opt/{0}/bin/'.format(self.container)
      self.firmware_dir = '{0}{1}/'.format(self.base_firmware_dir, name)
      self.command = ["lxc", "exec", self.container, "--", "bash", "-c"]
      
      """ Check if the destination directory exists, if not creates it """
      base_dir_content = listdir(self.base_firmware_dir)
      if name not in base_dir_content:
        mkdir(self.firmware_dir)

  @staticmethod
  def clean(s):
    return s.decode('utf-8')[:-1]

  def build(self):
    pass 


class Nodemcu(Firmware):
  version = -1

  def __init__(self):
    super().__init__('nodemcu')
    self.version = 0

  def build(self):

    """ Build firmware into LXD container """
    run(self.command + ["/opt/docker-nodemcu-build/build-esp8266"], capture_output=False)

    raw = run(self.command + ["ls {0} | grep nodemcu | grep .bin".format(self.bin_path)], capture_output=True)
    name = super().clean(raw.stdout)
    if name != '':
      firmware_path = self.bin_path + name

      """ Get firmware using LXD REST API """
      run(["curl", "--unix-socket", "/var/lib/lxd/unix.socket", "a/1.0/containers/{0}/files?path={1}".format(self.container, firmware_path), "--output", '{0}{1}'.format(self.firmware_dir, name)])
        
      """ Remove useless files """
      run(self.command + ["rm {0}/*".format(self.bin_path)])

