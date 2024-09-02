import json
import time

from model import CacheStats
from options import TtetlOptions
from printer import Printer
from utils import format_duration

class CliPrinter(Printer):
    def print_options(self, options: TtetlOptions) -> None:
        print(json.dumps(options.to_dict(), indent=2))

    def print_cache_stats(self, stats: CacheStats) -> None:
        print(f"Data cahed in {stats.location}")
        print(f"{'ENTITY':<10}{'COUNT':>7}{'OLDEST':>12}{'YOUNGEST':>12}")
        now = int(time.time())
        for e in stats.entities:
            first = format_duration(now-e.first)
            last = format_duration(now-e.last)
            print(f"{e.name:<10}{e.count:>7}{first:>12}{last:>12}")