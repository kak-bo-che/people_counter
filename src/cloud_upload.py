import sys, time
import database
import requests
from ubidots import ApiClient
import util

class CloudUpload(object):
  def __init__(self, configuration_file, database_file='jonnyboards.db'):
    self.config = {}
    self.api_key, self.sensors = util.loadConfig(configuration_file)
    self.database = database.Database(database_file)
    self.ubidotsConfig()

  def ubidotsConfig(self):
    while(True):
        try:
            self.api = ApiClient(self.api_key)
            self._ubidotsRegisterSensors()
            return True
        except requests.exceptions.ConnectionError:
            print "Failed to connect to UbiDots"
            time.sleep(5)

  def _ubidotsRegisterSensors(self):
      for sensor_name, sensor_config in self.sensors.iteritems():
          self.sensors[sensor_name]['ref'] = self.api.get_variable(sensor_config['id'])

  def RecordEvent(self, sensor_name, value, timestamp, count, duration, note):
    context = {'count': count, 'duration': duration}
    ref = self.sensors[sensor_name]['ref']
    if note:
      context['note'] = note

    ref.save_value({'value':value, 'timestamp': timestamp, 'context':context})


  def uploadLatestEvents(self):
    records = self.database.RetrieveNotUploadedRows()
    for record in records:
      print record
      record_id, timestamp, sensor, value, count, duration, note, uploaded_at = record
      self.RecordEvent(sensor, value, timestamp, count, duration, note)
      self.database.MarkRecordAsUploaded(record_id)

  def monitor(self):
    while(True):
      try:
        self.uploadLatestEvents()
        time.sleep(5)
      except requests.exceptions.ConnectionError:
        print "attempting to reconnect"
        self.ubidotsConfig()

if __name__ == "__main__":
  options = util.parseOptions()
  configuration_file = options.configuration_file
  uploader = CloudUpload(configuration_file,  options.database_file)
  uploader.monitor()
