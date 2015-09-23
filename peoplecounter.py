from ubidots import ApiClient
import requests
import RPi.GPIO as GPIO
import time
import socket
import yaml # pyyaml
import argparse
import sys

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class PeopleCounter(object):
    def __init__(self, configuration_file=''):
        self.config = {}
        options = self._parseOptions()
        configuration_file = options.configuration_file
        self._loadConfig(configuration_file)
        self._ubidotsConnect()
        self.ipaddress = get_ip_address() #socket.gethostbyname(socket.gethostname())
        self._configureSensors()
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

    def monitorSensors(self):
        while(True):
            try:
                for sensor_name, sensor_config in self.sensors.iteritems():
                    presence = GPIO.input(sensor_config['gpio'])
                    if presence:
                        GPIO.output(4, GPIO.HIGH)
                    else:
                        GPIO.output(4, GPIO.LOW)
                    if(presence != sensor_config['last_presense']):
                        if presence == 1:
                            context = {}
                            sensor_config['count'] += 1
                            if 'last_timestamp' in sensor_config:
                                context['duration'] = int(time.time()) - sensor_config['last_timestamp']
                            else:
                                context['ipaddress'] = self.ipaddress
                            print "%s: %d" %(sensor_name, sensor_config['count'])
                            sensor_config['ref'].save_value({'value':sensor_config['count'], 'context':context})
                        else:
                            sensor_config['last_timestamp'] = int(time.time())
                        sensor_config['last_presense'] = presence

                time.sleep(0.25)
            except requests.exceptions.ConnectionError:
                self.ubidotsConfig()

counter = PeopleCounter()
counter.monitorSensors()
