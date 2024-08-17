from dataclasses import dataclass, field, asdict

def default_values():
  return {
    "logging": {
      "level": "DEBUG",
      "target": "console"
    },
    "api": {
      "keys": [],
      "source": "None",
      "cache_duration": 3600
    },
    "data": {
      "location": "./data"
    }
  }

class TtetlOptions:
  def __init__(self, options = {}):
    resolved = default_values()
    resolved.update(options)
    self.api = ApiOptions(**resolved['api'])
    self.data = DataOptions(**resolved['data'])
    self.logging = LoggingOptions(**resolved['logging'])

  def accept_printer(self, printer):
     printer.print_options(self)

  def to_dict(self):
     return {
        'api': asdict(self.api),
        'data': asdict(self.data),
        'logging': asdict(self.logging)
     }

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
    level: str = "DEBUG"
    target: str = "console"