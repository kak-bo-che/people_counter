import yaml # pyyaml
import argparse
import sys
import database
import requests
from ubidots import ApiClient
import requests

class CloudUpload(object):
  def __init__(self):
    self.config = {}
    options = self._parseOptions()
    configuration_file = options.configuration_file
    self._loadConfig(configuration_file)
    self.database = database.Database()
    self._ubidotsConnect()
    self.ubidotsConfig()

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

  def ubidotsConfig(self):
    while(True):
        try:
            self._ubidotsConnect()
            self._ubidotsRegisterSensors()
            return True
        except requests.exceptions.ConnectionError:
            print "Failed to connect to UbiDots"
            time.sleep(5)

  def _ubidotsConnect(self):
      self.api = ApiClient(self.api_key)

  def _ubidotsRegisterSensors(self):
      for sensor_name, sensor_config in self.sensors.iteritems():
          self.sensors[sensor_name]['ref'] = self.api.get_variable(sensor_config['id'])

  def RecordEvent(self, sensor_id):
    sensor_config['ref'].save_value({'value':sensor_config['count'], 'context':context})
    except requests.exceptions.ConnectionError:
        self.ubidotsConfig()

  def uploadData(self):
    records = datbase.RetrieveNotUploadedRows()
    for record in records:
      print record


if __name__ == "__main__":
  uploader = CloudUpload()
  uploader.uploadData()