"""
Contains the setup script for talata_bont_backend package
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = dict(

    # meta data
    name='talata_bont_backend',
    description='Backend Service of 3bont.com',
    author='3bont.com',
    # 'url': 'URL to get it at.',
    # 'download_url': 'Where to download it.',
    author_email='info@3bont.com',
    version='0.1',

    # installation requirements

    # package
    package_dir = {'': 'lib'},
    packages = ['talata_bont_backend',
                'talata_bont_backend.crawlers',
                'talata_bont_backend.util']
)

setup(**config)