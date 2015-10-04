#!/usr/bin/env python

import os
from setuptools import setup

setup(name='JonnyBoardsSensor',
      version='0.1.0',
      description='A sensor platform for measuring the number of people seeing advertising',
      author='Troy Ross',
      author_email='kak.bo.che@gmail.com',
      url='https://github.com/kak-bo-che/people_counter.git',
      install_requires=['ubidots', 'RPi.GPIO', 'pyyaml', 'flask'],
      packages=['src'],
      entry_points={
          'console_scripts': [
              'sensor_monitor = src.sensor_monitor:main',
              'cloud_upload = src.cloud_upload:main'
          ]
      },
     )

