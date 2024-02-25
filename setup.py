#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='og_log',
      version='0.1.0',
      description='Simple trace logger',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Olivier Galand',
      author_email='galand.olivier.david@gmail.com',
      url='https://github.com/OlivierGaland/pyog-log',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
            "sys",
            "datetime",
            "threading",
            "inspect"
      ],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3.0',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3'
      ]
      )
