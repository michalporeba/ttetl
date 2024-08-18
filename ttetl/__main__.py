import click
from ttetl.cli_actions import *
import logging

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config", "-c", help="Use a configuration file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.pass_context
def cli(ctx, config, verbose, debug):
    ctx.obj = create_config(config)

    if verbose:
        ctx.obj.set_verbose()
    if debug:
        ctx.obj.set_debug()

    configure_logging(ctx.obj)
    logging.debug(f"Using {ctx.obj.source} configuration")


@cli.command()
def test():
    test1()


@cli.group()
@click.pass_context
def show(ctx):
    pass


@show.command()
@click.pass_context
def cache(ctx):
    show_cache_stats(ctx.obj)


@show.command()
@click.pass_context
def config(ctx):
    show_config(ctx.obj)


if __name__ == "__main__":
    cli(obj=None)
