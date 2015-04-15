#!/usr/bin/env python

from distutils.core import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(name='game_info',
      version='1.0',
      description='game parser info',
      author='Joao Ascenso',
      author_email='joaoricardoascenso@gmail.com',
      url='',
      packages=['game_info'],
      install_requires=reqs,
      scripts=['game_info.py']
     )
