#!/usr/bin/env python

import os
from distutils.core import setup

example_files = [os.path.join('examples', p) for p in os.listdir('examples') if not p.startswith('_')]
doc_files = ['COPYING', 'COPYING.LESSER', 'README', 'VERSION']

setup(name='pyinsim',
      version='2.0.5',
      description='InSim library for the Python programming language',
      author='Alex McBride',
      author_email='xandermcbride@gmail.com',
      url='http://pyinsim.codeplex.com/',
      packages=['pyinsim'],
      data_files=[('docs', doc_files),
                  ('examples', example_files)])
