#!/bin/env python3
from configparser import ConfigParser
import click
from loguru import logger


# Default config file
DEFAULT_CFG = 'settings.ini'

def configure(ctx, param, filename):
    cfg = ConfigParser()
    cfg.read(filename)
    ctx.default_map = {}
    for sect in cfg.sections():
        command_path = sect.split('.')
        if command_path[0] != 'settings':
            continue
        defaults = ctx.default_map
        for cmdname in command_path[1:]:
            defaults = defaults.setdefault(cmdname, {})
        defaults.update(cfg[sect])

# Create CLI group
@click.group()
@click.option('-c', '--config', type = click.Path(dir_okay=False), default = DEFAULT_CFG,
              callback = configure, is_eager = True, expose_value = False,
              help = 'Read option defaults from the specified INI file', show_default = True,
              )
@click.option('-v', '--verbose', count=True, help='Increase verbosity, -v for INFO, -vv for DEBUG', default=0)
def cli(**kwargs):
    # Set log level
    if kwargs['verbose'] == 0:
        logger.remove()
        logger.add(lambda msg: click.echo(msg, err=True), level='WARNING')
    elif kwargs['verbose']== 1:
        logger.remove()
        logger.add(lambda msg: click.echo(msg, err=True), level='INFO')
    elif kwargs['verbose']> 1:
        logger.remove()
        logger.add(lambda msg: click.echo(msg, err=True), level='DEBUG')
    else:
        raise ValueError('Invalid verbose value')

from pysignalcatbot.cli import *
cli.add_command(start)
cli.add_command(single)


if __name__ == '__main__':
    cli()