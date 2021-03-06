"""
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
"""

import os
import sys
import re
import shutil
import pathlib
import numpy
from setuptools import find_packages, setup
import distutils.command.build


if sys.version_info < (3, 5):
    raise RuntimeError('renom_rg requires greater than Python3.5')

DIR = str(pathlib.Path(__file__).resolve().parent)

requires = [
    "bottle",
    "sqlalchemy",
    "alembic",
    "xgboost"
]


entry_points = {
    'console_scripts': [
        'renom_rg = renom_rg.server.server:main',
    ]
}


class BuildNPM(distutils.command.build.build):
    """Custom build command."""

    def run(self):
        shutil.rmtree(os.path.join(DIR, 'renom_rg/server/.build'), ignore_errors=True)
        curdir = os.getcwd()
        try:
            jsdir = os.path.join(DIR, 'js')

            # skip if js directory not exists.
            if os.path.isdir(jsdir):
                os.chdir(jsdir)
                ret = os.system('npm install')
                if ret:
                    raise RuntimeError('Failed to install npm modules')

                ret = os.system('npm run build')
                if ret:
                    raise RuntimeError('Failed to build npm modules')

        finally:
            os.chdir(curdir)

        super().run()


setup(
    name="renom_rg",
    version="0.3b2",
    entry_points=entry_points,
    packages=['renom_rg'],
    install_requires=requires,
    include_package_data=True,
    zip_safe=True,
    cmdclass={
        'build': BuildNPM,
    }
)
