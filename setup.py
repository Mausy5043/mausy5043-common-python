#!/usr/bin/env python3

from distutils.core import setup

setup(name='mausy5043-common-python',
      version='0.4.1',
      description='Common Python Utilities from Mausy5043',
      author='Maurice (mausy5043) Hendrix',
      author_email='undisclosed@example.com',
      url='https://github.com/Mausy5043/mausy5043-common-python',
      license='MIT',
      py_modules=['mausy5043libs/__init__',
                  'mausy5043libs/libdaemon3',
                  'mausy5043libs/libsmart3',
                  'mausy5043funcs/__init__',
                  'mausy5043funcs/fileops3'
                  ],
      )
