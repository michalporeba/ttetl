import json
import os

from file_cache import FileCache
from model import CacheStats
from options import TtetlOptions


def get_config(path: str) -> TtetlOptions:
    if os.path.exists(path):
        with open(path, "r") as f:
            custom_options = json.load(f)

        return TtetlOptions(custom_options, source=path)

    return TtetlOptions()


def get_cache_stats(options: TtetlOptions) -> CacheStats:
    fc = FileCache(options.data.location)
    return fc.get_stats()
