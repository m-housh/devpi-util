from setuptools import setup, find_packages

setup(
        name='devpi-client-util',
        version='0.1.0',
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
