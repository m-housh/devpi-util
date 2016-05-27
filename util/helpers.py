import click
import sys
import os
import subprocess
from shutil import copytree, rmtree, ignore_patterns
from tempfile import mkdtemp
from .environ_key import environ_key
import yaml

def _is_debug():
    """ Get debug from the environment and return True or False accordingly. """
    debug = os.environ.get('DEBUG', '1').lower()
    if debug is '0' or debug is 'true':
        return True
    return False

def print_if_debug(prefix='Main', message=None):
    if _is_debug():
        return click.echo('[{0}]=> {1}'.format(prefix, message))

def yaml_from_file(path, directive=None):
    if not os.path.isfile(path):
        return False

    with open(path, 'r') as stream:
        try:
            data = yaml.load(stream)
            if directive is not None:
                data = data.get(str(directive))
        except yaml.YAMLError as error:
            print_if_debug('Yaml', 'Error loading file: {}'.format(path))
            return None
    return data

def _is_non_empty_dir(path):
    if os.path.isdir(path):
        lst = os.listdir(path)
        if len(lst) > 0:
            return True
    return False

def cleanup():
    """ Cleans-up after commands, and removes tmp directory. """
    tmp_path = os.environ.get(environ_key.tmp_dir, None)
    if tmp_path is not None:
        print_if_debug(prefix='Cleanup', message="Removing tmp path: '{}'".format(tmp_path))
        rmtree(tmp_path)

    return True

def prepare_for_commands(config):
    """ Takes a config instance and sets up the environment depending on config.
    
    **Args:**
        * **config** *(:py:class:`.config.Config`)*
            A config instance to be used for the setup.
    """
    tmp_path = config.tmp_dir()
    tmp_certs = os.path.join(tmp_path, 'certs')
    print_if_debug(prefix='Prepare:Certs', message='tmp_certs: {}'.format(tmp_certs))

    if _is_non_empty_dir(config.certs):
        print_if_debug(prefix='Prepare:Certs', message='Copying Certs...')
        copytree(config.certs, tmp_certs, ignore=ignore_patterns('.DS_Store'))

        print_if_debug(prefix='Prepare:Certs', message='Rehashing certs...')
        output = subprocess.run(['c_rehash', tmp_certs])
        
        if output.returncode == 0:
            print_if_debug(prefix='Prepare:Certs', message='Done: {}!'.format(output.returncode))
            # if successfull set the requests_ca_bundle variable
            os.environ[environ_key.requests_bundle] = tmp_certs
        else:
            print_if_debug(prefix='Prepare:Certs', message='Error hashing certs.')
            clean_up()
            sys.exit(1) 
    
    # check site-packages directory and set pip_target if applicable.
    if _is_non_empty_dir('/site-packages'):
        print_if_debug(prefix='Prepare:Site-Packages', 
                message="Setting pip target to '/site-packages'")
        os.environ[environ_key.pip_target] = '/site-packages'
    else:
        print_if_debug(prefix='Prepare:Site-Packages',
                message="'/site-packages' is empty, skipping.")

