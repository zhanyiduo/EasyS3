from setuptools import setup, find_packages

import re
import os

DIR = os.path.dirname(os.path.realpath(__file__))
INIT_FILE = os.path.join(DIR, 'get_s3_data', '__init__.py')

with open(INIT_FILE, 'r') as f:
    s = f.read()
    VERSION = re.findall(r"__version__\s*=\s*['|\"](.+)['|\"]", s)[0]

setup(name='EasyS3',
      version=VERSION,
      author='Yiduo Zhan',
      author_email='zhanyiduo@gmail.com',
      packages=find_packages(),
      install_requires=[
          'boto3',
          'pandas',
      ],
      license='Use as you wish. No guarantees whatsoever.',)