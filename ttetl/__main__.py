import click
import logging

from ttetl.cli_actions import (
    configure_logging,
    create_config,
    fetch_all,
    show_cache_stats,
    show_config,
    cli_show_events
)

logger = logging.getLogger(__name__)


@click.group()
@click.option("--api-key", help="Use a specific API key")
@click.option("--config", "-c", help="Use a configuration file")
@click.option("--data", "-d", help="Local data store location")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.pass_context
def cli(ctx, api_key, config, data, verbose, debug):
    ctx.obj = create_config(config)

    if api_key:
        ctx.obj.add_api_keys([api_key], "CLI parameter")
    if data:
        ctx.obj.set_data_location(data)
    if verbose:
        ctx.obj.set_verbose()
    if debug:
        ctx.obj.set_debug()

    configure_logging(ctx.obj)
    logging.debug(f"Using {ctx.obj.source} configuration")


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


@show.command()
@click.pass_context
def events(ctx):
    cli_show_events(ctx.obj)

@cli.group()
@click.pass_context
def fetch(ctx):
    pass


@fetch.command()
@click.pass_context
def all(ctx):
    fetch_all(ctx.obj)


if __name__ == "__main__":
    cli(obj=None)
