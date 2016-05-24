import click
import os
import sys
from .config import Config
from .keys import EnvironKey
from .helpers import print_if_debug, yaml_from_file, prepare_for_commands, cleanup

config = Config()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host')
@click.option('--port')
@click.option('--index')
@click.option('--config')
@click.option('--directive')
@click.option('--scheme')
@click.option('--url')
@click.option('--certs')
@click.option('--password')
@click.option('--username')
@click.argument('commands', nargs=-1)
def fire(host=None, port=None, index=None, config=None, directive=None, scheme=None, \
        url=None, certs=None, password=None, username=None, commands='--help'):

    os.environ['DEBUG'] = '0'

    config = Config()

    
    attrs = EnvironKey(
            host=host,
            port=port,
            index=index,
            config_path=config,
            scheme=scheme,
            certs=certs,
            url=url,
            password=password,
            user=username,
            requests_bundle=None,
            pip_target=None,
            tmp_path=None
    )


    for key, value in attrs._asdict().items():
        if value is not None:
            setattr(config, key, value)

    print_if_debug(prefix='Main', message='config.port: {}'.format(config.port))

    if directive:
        config.load_directive(directive)
    
    prepare_for_commands(config)


    # cleanup before exit.
    cleanup()




@cli.command()
def testing():
    click.echo("The devpi url is: '{0}'".format(config.url))
    os.environ['DEBUG'] = '0'
    print_if_debug(message="Loading yaml...")

    data = config.yaml
    print_if_debug(prefix='Config', message='Yaml: {}'.format(data))



