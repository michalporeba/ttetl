from dataclasses import asdict, dataclass, field


def default_values():
    return {
        "logging": {"level": "WARNING", "target": "console"},
        "api": {"keys": [], "source": "None", "cache_duration": 3600},
        "data": {"location": "./data"},
    }


class TtetlOptions:
    def __init__(self, options=None, source="DEFAULTS"):
        if options is None:
            options = {}

        resolved = default_values()
        resolved.update(options)
        self.source = source
        self.api = ApiOptions(**resolved["api"])
        self.data = DataOptions(**resolved["data"])
        self.logging = LoggingOptions(**resolved["logging"])

    def accept_printer(self, printer):
        printer.print_options(self)

    def to_dict(self):
        return {
            "api": asdict(self.api),
            "data": asdict(self.data),
            "logging": asdict(self.logging),
        }

    def set_verbose(self):
        self.logging.level = "INFO"

    def set_debug(self):
        self.logging.level = "DEBUG"


@dataclass
class ApiOptions:
    keys: list = field(default_factory=list)
    source: str = "None"
    cache_duration: int = 3600


@dataclass
class DataOptions:
    location: str = "./data"


@dataclass
class LoggingOptions:
    level: str = "WARNING"
    target: str = "console"
