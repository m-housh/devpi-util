"""
    devpi-client-util.cli
    =====================

    Holds the command line commands for our application.

"""
import click
import os
import sys
import subprocess
from time import sleep
from .config import Config
from .environ_key import EnvironKey, environ_key
from .helpers import print_if_debug, yaml_from_file, prepare_for_commands, cleanup, command

#:TODO get rid of the group and just have one command.
@click.group()
def cli():
    pass

@command()
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
    """ Our main command-line entrypoint for the app. 
    
   **Options:**
        * **- -config-path** (*str*):
            The path to the config (yaml) file that holds directives (sub-key's) for devpi
            connections.
        * **- -directive** (*str*):
            The sub-key to read from the config (yaml) file to use for this session.

        .. note::
            The following options are available, to override values in the config file,
            or if a config file is not being used.

        * **- -host** (*str*):
            This set's the devpi host for the session.
        * **- -port** (*str*):
            This set's the devpi host's port for the session.
        * **- -scheme** (*str*):
            This set's the scheme to use to build the url for this session. Defaults to 'http'.
        * **- -url** (*str*):
            A full url for the session, this will override any of the options for ('scheme',
            'host' and 'port').

        .. note::
            If a full url is not used then one will be built using 'scheme://host:port/',
            however if a value is passed in with the 'url' option then that will be used
            instead.

        * **- -index** (*str*):
            This set's the devpi index to connect to for this session.
        * **- -certs** (*str*):
            This set's a path for custom cert's for request validation's.  Used if using
            self-signed certs for you devpi-server instance. Defaults to '/certs'. 
        * **- -username** (*str*):
            This set's the devpi username for the session, if 'username' and 'password' options
            are set then we will attempt a login (which can be required, depending on your
            command and devpi-server setup)
        * **- -password** (*str*):
            This set's the password for the devpi username for this session.
        * **- -debug** (*str*):
           This set's debug for the session, which gives you some output while running this
           script.

    **Arguments:**
        Due to the way args get parsed all 'OPTIONS' for the set-up of this script should be 
        followed with '--' and everything after '--' get passed into devpi-client command.  
        This is not needed, if you are not passing options to devpi, but easier to get in
        the habit of using it.

    **Example:**  
        .. code:: bash

            $ docker run -it --rm \\
                -v "$PWD":/app \\
                -v "$PWD/config":/config \\
                --link devpi-server \\
                mhoush/devpi-client-util \\
                --directive local \\# the config sub-key to use for this session
                -- \\ # everything following this is the devpi-client command's to use.
                upload --with-docs

    
    """
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

        with open(os.devnull, 'w') as devnull:
            subprocess.call(['devpi', 'use', config.url()], stdout=devnull, stderr=devnull)
        # connect to an index before issuing commands
        if config.index:
            print_if_debug('Main', 'Connecting to index: \'{}\''.format(config.index))
            with open(os.devnull, 'w') as devnull:
                subprocess.call(['devpi', 'use', config.index], stdout=devnull, stderr=devnull)

        if config.password:
            if config.user:
                print_if_debug('Main', 'Attempting login...')
                with open (os.devnull, 'w') as devnull:
                    subprocess.call(['devpi', 'login', config.user, '--password', \
                            config.password], stdout=devnull, stderr=devnull)

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

