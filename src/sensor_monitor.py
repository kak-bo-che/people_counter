import RPi.GPIO as GPIO
import json
import sys, time
import database
import util

class SensorMonitor(object):
  def __init__(self, configuration_file, database_file='jonnyboards.db'):
      self.config = {}
      self.database = database.Database(database_file)

      (self.api_key, self.sensors) = util.loadConfig(configuration_file)
      self.ipaddress = util.get_ip_address()
      self._configureSensors()

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
                    duration = int(time.time()) - sensor_config['last_timestamp']
                    note = None
                else:
                    duration = None
                    note = self.ipaddress
                sensor_config['last_timestamp'] = int(time.time())
                sensor_config['last_presense'] = presence
                self.database.StoreSensorData(sensor_name, presence, sensor_config['count'], duration, note)

        time.sleep(0.25)

def main():
  options = util.parseOptions()
  configuration_file = options.configuration_file
  counter = SensorMonitor(configuration_file, options.database_file)
  counter.monitorSensors()

if __name__ == "__main__":
  main()
