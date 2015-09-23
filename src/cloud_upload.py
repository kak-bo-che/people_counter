from ubidots import ApiClient
import requests

class CloudUpload(object):
  def __init__(self):
    self._ubidotsConnect()
    self.ubidotsConfig()


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
