import json

from model import CacheStats
from options import TtetlOptions
from printer import Printer


class CliPrinter(Printer):
    def print_options(self, options: TtetlOptions) -> None:
        print(json.dumps(options.to_dict(), indent=2))

    def print_cache_stats(self, stats: CacheStats) -> None:
        print(f"Data cahed in {stats.location}")