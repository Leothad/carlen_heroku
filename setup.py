#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def text_of(relpath):
    """
    Return string containing the contents of the file at *relpath* relative to
    this file.
    """
    thisdir = os.path.dirname(__file__)
    file_path = os.path.join(thisdir, os.path.normpath(relpath))
    with open(file_path) as f:
        text = f.read()
    return text


# Read the version from carlen.__version__ without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = re.search(
    "__version__ = '([^']+)'", text_of('carlen/__init__.py')
).group(1)

NAME = 'carlen'
VERSION = version
PACKAGES = find_packages()
PACKAGE_DATA = {'carlen': ['templates/*.jinja', 'models/*.h5']}

INSTALL_REQUIRES = ['fastapi==0.70.*', 'Flask==2.0.*', 'Flask-PyMongo==2.3.*', 'pymongo[srv]==3.12.*', 'tensorflow==2.7.*',
                    'numpy==1.21.*', 'Pillow==8.4.*', 'scikit-image==0.18.*', 'pydantic==1.8.*']

params = {
    'name':             NAME,
    'version':          VERSION,
    'packages':         PACKAGES,
    'package_data':     PACKAGE_DATA,
    'install_requires': INSTALL_REQUIRES,
}

setup(**params)
