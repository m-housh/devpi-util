import click
import os
import sys
import subprocess
from time import sleep
from .config import Config
from .environ_key import EnvironKey, environ_key
from .helpers import print_if_debug, yaml_from_file, prepare_for_commands, cleanup

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', envvar=environ_key.host, default=None)
@click.option('--port', envvar=environ_key.port, default=None)
@click.option('--index', envvar=environ_key.index, default=None)
@click.option('--config-path', envvar=environ_key.config_path, default=None)
@click.option('--directive', default=None)
@click.option('--scheme', envvar=environ_key.scheme, default=None)
@click.option('--url', envvar=environ_key.url, default=None)
@click.option('--certs', envvar=environ_key.certs, default=None)
@click.option('--password', envvar=environ_key.password, default=None)
@click.option('--username', envvar=environ_key.user, default=None)
@click.option('--debug', envvar=environ_key.debug, default='1')
@click.argument('devpi', nargs=-1)
def fire(devpi, **kwargs):

    os.environ['DEBUG'] = '0'
        
    print_if_debug('Main', "Kwargs: '{}'".format(kwargs))
    directive = kwargs.pop('directive', None)
    config = Config(**kwargs)


    print_if_debug(prefix='Main', message='config.port: {}'.format(config.port))

    if directive:
        config.load_directive(directive)
    
    prepare_for_commands(config)
    
    print_if_debug('Main', message="Devpi: '{}'".format(devpi))
        
    if 'sh' in devpi:
        subprocess.call(['sh'])
    else:

        if 'devpi' in devpi:
            print_if_debug('Main', message="Devpi found")
        else:
            print_if_debug('Main', message="Devpi found")
            devpi = ('devpi',) + devpi

        print_if_debug(prefix='Main', message='Connecting to devpi url: \'{}\''.format(config.url()))

        config.export()
        # connect to devpi-server at the url
        print_if_debug(prefix='Main', message='Connecting to devpi url: \'{}\''.format(config.url()))
        subprocess.call(['devpi', 'use', config.url(), '1>&2>/dev/null'])
        # connect to an index before issuing commands
        if config.index:
            print_if_debug('Main', 'Connecting to index: \'{}\''.format(config.index))
            subprocess.call(['devpi', 'use', config.index, '1>&2>/dev/null'])

        if config.password:
            if config.user:
                print_if_debug('Main', 'Attempting login...')
                subprocess.call(['devpi', 'login', config.user, '--password', \
                        config.password])

        #subprocess.call(['sh', '/app/util/test.sh'])
        subprocess.call(devpi)

    # cleanup before exit.
    cleanup()




@cli.command()
@click.option('--debug', default='1')
@click.option('--host', default='localhost')
@click.argument('devpi', nargs=-1)
def testing(devpi, **kwargs):
    os.environ['DEBUG'] = '0'

    print_if_debug(prefix='Testing', message='In testing')
    print_if_debug(prefix='Testing', message='Kwargs: {}'.format(kwargs))
    print_if_debug(prefix='Testing', message='Devpi: {}'.format(devpi))

