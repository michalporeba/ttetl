import logging

from model import CacheStats
from options import TtetlOptions


class Printer:
    def print_options(self, options: TtetlOptions) -> None:
        logging.error("print_options not defined in {self}!")

    def print_cache_stats(self, stats: CacheStats) -> None:
        logging.error("print_cache_stats not defined in {self}!")