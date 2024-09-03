import logging
import json
import os

from file_cache import FileCache
from model import CacheStats
from options import ApiOptions, DataOptions, TtetlOptions
from tt_client import TTClient

logger = logging.getLogger(__name__)

def get_config(path: str) -> TtetlOptions:
    if os.path.exists(path):
        with open(path, "r") as f:
            custom_options = json.load(f)

        return TtetlOptions(custom_options, source=path)

    return TtetlOptions()


def get_cache_stats(options: TtetlOptions) -> CacheStats:
    fc = FileCache(options.data.location)
    return fc.get_stats()


def get_events_from_api(options: TtetlOptions, timestamp=None):
    fc = FileCache(options.data)
    tt = TTClient(options.api)

    if timestamp is None:
        timestamp = fc.get_event_series_timestamp()

    for es in tt.stream_event_series(timestamp):
        for e in tt.stream_events_in_series(es):
            fc.save_event(e)
            logger.info(f'fetched: {e}')
            yield e
        fc.save_event_series_timestamp(es)


def stream_events_from_cache(options: TtetlOptions, timestamp=None):
    fc = FileCache(options.data)
    for e in fc.stream_events(timestamp):
        print(e)
        yield e
