import os
from setuptools import setup, find_packages

dirname = os.path.dirname(os.path.realpath(__file__))
version = {}

with open(os.path.join(dirname, 'version.py')) as fp:
    exec(fp.read(), version)

setup(
        name='devpi-client-util',
        version=version['__version__'],
        author='Michael Housh',
        author_email='mhoush@houshhomeenergy.com',
        url='https://github.com/m-housh/devpi-util',
        packages=find_packages(),
        zip_safe=False,
        install_requires=[
            'click',
            'pyyaml',
        ],
        entry_points={
            'console_scripts': [
                'devpi-client-util = util.cli:cli'
            ],
        },
)
