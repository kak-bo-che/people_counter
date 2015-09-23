import RPi.GPIO as GPIO
import yaml, json
import argparse
import sys
import socket
import database

def get_ip_address():
    #socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class SensorMonitor(object):
  def __init__(self, configuration_file=''):
      self.database = database.Database()
      self.config = {}
      options = self._parseOptions()
      configuration_file = options.configuration_file
      self._loadConfig(configuration_file)
      self.ipaddress = get_ip_address()
      self._configureSensors()


  def _parseOptions(self):
      parser = argparse.ArgumentParser(description='Monitor people entering space')
      parser.add_argument('configuration_file', help='YAML configuration File')
      return parser.parse_args()

  def _loadConfig(self, filename):
      try:
          f = open(filename)
          # use safe_load instead load
          configuration = yaml.safe_load(f)
          f.close()
          self.api_key = configuration['api_key']
          self.sensors = configuration['sensors']

      except yaml.scanner.ScannerError, e:
          print "ERROR: You likely have no space after a colon in your config file"
          sys.exit(1)

  def _configureSensors(self):
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(4, GPIO.OUT)
      for sensor_name, sensor_config in self.sensors.iteritems():
          if sensor_config['pull_up']:
              GPIO.setup(sensor_config['gpio'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          else:
              GPIO.setup(sensor_config['gpio'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
          sensor_config['last_presense'] = 0
          if not 'count' in sensor_config:
              sensor_config['count'] = 0

  def monitorSensors(self):
      while(True):
        for sensor_name, sensor_config in self.sensors.iteritems():
            presence = GPIO.input(sensor_config['gpio'])
            if(presence != sensor_config['last_presense']):
                context = {}
                sensor_config['count'] += 1
                if 'last_timestamp' in sensor_config:
                    context['duration'] = int(time.time()) - sensor_config['last_timestamp']
                else:
                    context['ipaddress'] = self.ipaddress
                print "%s: %d" %(sensor_name, sensor_config['count'])
                context['count'] = sensor_config['count']
                sensor_config['last_timestamp'] = int(time.time())
                sensor_config['last_presense'] = presence
                self.database.StoreSensorData(sensor_name, presence, json.dumps(context))
                # sensor_config['ref'].save_value({'value':presence, 'context':context})

        time.sleep(0.25)
