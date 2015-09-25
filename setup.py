#!/usr/bin/env python

from distutils.core import setup

setup(name='JonnyBoardsSensor',
      version='0.1.0',
      description='A sensor platform for measuring the number of people seeing advertising',
      author='Troy Ross',
      author_email='kak.bo.che@gmail.com',
      url='https://github.com/kak-bo-che/people_counter.git',
      requires=['ubidots', 'RPi.GPIO', 'pyyaml'],
      packages=['src'],
     )

