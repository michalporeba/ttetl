import json
from options import TtetlOptions
from printer import Printer


class CliPrinter(Printer):
    def print_options(self, options: TtetlOptions) -> None:
        print(json.dumps(options.to_dict(), indent=2))
