from dataclasses import asdict, dataclass, field


def default_values():
    return {
        "logging": {"level": "WARNING", "target": "console"},
        "api": {
            "keys": [],
            "keys_source": "None",
            "cache_duration": 3600,
            "delay_seconds": 0.05,
            "url_base": "https://api.tickettailor.com/v1"
        },
        "data": {"location": "./data"},
    }


class TtetlOptions:
    def __init__(self, options: dict | None = None, source: str = "DEFAULTS"):
        if options is None:
            options = {}

        resolved = default_values()
        resolved.update(options)
        self.source = source
        self.api = ApiOptions(**resolved["api"])
        self.data = DataOptions(**resolved["data"])
        self.logging = LoggingOptions(**resolved["logging"])

    def accept_printer(self, printer) -> None:
        printer.print_options(self)

    def to_dict(self) -> dict:
        return {
            "api": asdict(self.api),
            "data": asdict(self.data),
            "logging": asdict(self.logging),
        }

    def set_verbose(self) -> None:
        self.logging.level = "INFO"

    def set_debug(self) -> None:
        self.logging.level = "DEBUG"

    def add_api_keys(self, keys: list[str], source: str) -> None:
        self.api.keys = keys
        self.api.keys_source = source


@dataclass
class ApiOptions:
    keys: list = field(default_factory=list)
    keys_source: str = "None"
    cache_duration: int = 3600
    delay_seconds: int = 0.05
    url_base: str = "https://api.tickettailor.com/v1"


@dataclass
class DataOptions:
    location: str = "./data"


@dataclass
class LoggingOptions:
    level: str = "WARNING"
    target: str = "console"
