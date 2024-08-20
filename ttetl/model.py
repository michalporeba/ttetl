from dataclasses import dataclass, field
from typing import List


@dataclass
class CachedEntity:
    name: str
    count: int
    first_timestamp: int
    last_timestamp: int


@dataclass
class CacheStats:
    location: str
    entities: List[CachedEntity] = field(default_factory=list)

    def accept_printer(self, printer) -> None:
        printer.print_cache_stats(self)