from subprocess import run
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
  basedir = '/opt/nodemcu-firmware/'
  modules_filename = 'user_modules.h'
  modules_path = ''
  version = -1
  modules = []
  config = []
  header = '#ifndef __USER_MODULES_H__\n#define __USER_MODULES_H__\n\n#ifndef LUA_CROSS_COMPILER\n\n'
  footer = '#endif  /* LUA_CROSS_COMPILER */\n#endif  /* __USER_MODULES_H__ */'


  def __init__(self):
    super().__init__('nodemcu')
    self.version = 0

    include_path = '{0}app/include/'.format(self.basedir)
    self.modules_path = '{0}{1}'.format(include_path, self.modules_filename)

    """ Get content of the include directory from nodemcu-firmware """
    raw = run(self.command + ["ls \"{0}\"".format(include_path)], capture_output=True)

    if raw.returncode == 0:
      """ If successfull reading of the dir content """
      config_dir_content = Firmware.clean(raw.stdout).split('\n')
      backup_file = '{0}.orig'.format(self.modules_filename) 

      if backup_file not in config_dir_content:
        """ Check if the original modules file has backup, if not creates it """
        run(self.command + ["mv \"{0}\" \"{0}.orig\"".format(self.modules_path)])
      
      elif self.modules_filename in config_dir_content :
        """ Check if modules file from old build exist, if true, destroy it """
        run(self.command + ["rm \"{0}\"".format(self.modules_path)])
    
    """ Load list of supported modules by NodeMCU """
    self.modules = self.__load_modules()


  def __get_file(self, src, dest):
    curl = ["curl", "--unix-socket", "/var/lib/lxd/unix.socket", 
            "a/1.0/containers/{0}/files?path={1}".format(self.container, src),
            "--output", dest]
    run(curl)


  def __load_modules(self):
    raw = run(self.command + ["cat \"{0}.orig\"".format(self.modules_path)], capture_output=True)
    return [i.split('#define ')[-1].split(' //')[0] for i in raw.stdout.decode('utf-8').split('\n') if 'LUA_USE_MODULES' in i] if raw.returncode == 0 else []


  def gen_config(self, indexes):
    """ Get config from User """
    self.config = [self.modules[i] for i in range(0, len(self.modules)) if i in indexes]

    """ Generate textual modules configuration """
    file_content = self.header
    for i in self.config:
      file_content = '{0}\n#define {1}'.format(file_content, i)
    file_content = '{0}\n\n\n{1}'.format(file_content, self.footer)

    curl = ["curl", "-X", "POST", "--unix-socket", "/var/lib/lxd/unix.socket", 
            "a/1.0/containers/{0}/files?path={1}".format(self.container, self.modules_path),
            "--data", file_content, "--header", "Content-Type:text/xml"]
    raw = run(curl)
    # TODO : check raw.returncode for errors


  def build(self):
    if len(self.config) == 0:
      print('Error : no modules to build\n')
      return

    """ Build firmware into LXD container """
    run(self.command + ["/opt/docker-nodemcu-build/build-esp8266"], capture_output=False)

    raw = run(self.command + ["ls {0} | grep nodemcu | grep .bin".format(self.bin_path)], capture_output=True)
    name = super().clean(raw.stdout)
    if name != '':
      firmware_path = self.bin_path + name

      """ Get firmware using LXD REST API """
      #run(["curl", "--unix-socket", "/var/lib/lxd/unix.socket", "a/1.0/containers/{0}/files?path={1}".format(self.container, firmware_path), "--output", '{0}{1}'.format(self.firmware_dir, name)])
      self.__get_file(firmware_path, '{0}{1}'.format(self.firmware_dir, name))
        
      """ Remove useless files """
      run(self.command + ["rm {0}/*".format(self.bin_path)])

