import click
import logging
import os
import re
import time

from actions import (get_cache_stats, get_config, get_events_from_api)
from cli_printer import CliPrinter
from file_cache import FileCache
from options import TtetlOptions
from utils import format_duration

from ttetl.tt_model import TicketGroupAggregate

logger = logging.getLogger(__name__)

printer = CliPrinter()

def stream_events_from_cache(timestamp=None):
    fc = FileCache()
    for e in fc.stream_events(timestamp):
        print(e)
        yield e


def get_ticket_groups(events):
    groups = {}
    events_count = 0
    for e in events:
        events_count += 1
        for tg in e.ticket_groups:
            name = GROUP_NAME_CORRECTIONS.get(tg.name, tg.name)

            if name not in groups.keys():
                groups[name] = TicketGroupAggregate(name)
            groups[name].add(tg)

    print(f"events processed: {events_count}")
    for tg in groups.values():
        print(tg)
        for tt in tg.ticket_types:
            print(tt)


GROUP_NAME_CORRECTIONS = {
    "Ambulance Crew": "Ambulance Crews",
    "ETA/PTA": "Ambulance Crews",
    "PTA/ETA": "Ambulance Crews",
    "Vehicle Crew": "Ambulance Crews",
    "Emergency Ambulance": "Ambulance Crews",
    "First Aider": "First Aiders",
    "Command": "Command & Support",
    "Command and Control": "Command & Support",
    "Command & Control": "Command & Support",
    "Event Management": "Command & Support",
    "Healthcare Professional": "Healthcare Professionals",
    "Health Care Professionals": "Healthcare Professionals",
    "ALS Ambulance Crew": "Healthcare Professionals",
    "Stadium HCPs": "Healthcare Professionals",
    "HCP": "Healthcare Professionals",
    "HCP's": "Healthcare Professionals",
}


def main():
    # get_events_from_api() #1722000587
    fc = FileCache()
    events = fc.stream_events()  # 1722000587
    get_ticket_groups(events)


def create_config(path):
    if not path:
        options = TtetlOptions()
        api_keys: str = os.environ.get("TICKET_TAILOR_API")
        if api_keys is not None:
            keys_list = [key.strip() for key in api_keys.split(",")]
            options.add_api_keys(keys_list, "ENV:TICKET_TAILOR_API")
        return options

    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, path)
    print(f"getting config from {full_path}")
    return get_config(full_path)


def configure_logging(options: TtetlOptions) -> None:
    level = options.logging.level.upper()
    message_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = "%H:%M:%S"

    if re.match("console", options.logging.target, re.IGNORECASE):
        logging.basicConfig(level=level, format=message_format, datefmt=date_format)
    else:
        logging.basicConfig(
            filename=options.logging.target,
            level=level,
            format=message_format,
            datefmt=date_format,
        )


def show_cache_stats(options):
    stats = get_cache_stats(options)
    stats.accept_printer(printer)


def show_config(options):
    options.accept_printer(printer)


def fetch_all(options):
    click.echo("Fetching data from Ticket Tailor")
    events = 0
    start_time = int(time.time())

    for e in get_events_from_api(options.api, 1722000587):
        events += 1
        t = f"[{format_duration(int(time.time()-start_time))}]"
        message = f"{t} Fetched {events} events..."
        click.echo(message, nl=False)
        click.echo("\b" * len(message), nl=False)

    click.echo("\nDone!")
