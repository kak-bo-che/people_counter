import argparse
import yaml
import socket

def get_ip_address():
    #socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def parseOptions(self):
    parser = argparse.ArgumentParser(description='Monitor people entering space')
    parser.add_argument('configuration_file', help='YAML configuration File')
    return parser.parse_args()

def loadConfig(filename):
    try:
        f = open(filename)
        # use safe_load instead load
        configuration = yaml.safe_load(f)
        f.close()
        return (configuration['api_key'], configuration['sensors'])

    except yaml.scanner.ScannerError, e:
        print "ERROR: You likely have no space after a colon in your config file"
        sys.exit(1)