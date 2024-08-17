import click
from ttetl.cli_actions import *

@click.group()
def cli():
  pass

@cli.command()
def test():
  test1()

@cli.group()
def show():
  pass

@show.command()
def cache():
  show_cache_stats()

@show.command()
def config():
  show_config()

if __name__ == '__main__':
  cli()