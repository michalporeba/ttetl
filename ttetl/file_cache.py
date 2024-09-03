import json
import os
import time

from model import CacheStats, CachedEntity
from ttetl.tt_model import Event
from ttetl.options import DataOptions


def stream_data_from(path):
    if not os.path.exists(path):
        return

    for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if not filename.endswith(".json") or not os.path.isfile(file_path):
                continue

            with open(file_path, "r") as f:
                yield json.load(f)


class FileCache:
    def __init__(self, options: DataOptions):
        self.path = options.location

    def save_event(self, event):
        path = f"{self.path}/events/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}{event.id}.json", "w") as f:
            json.dump({"timestamp": int(time.time()), "data": event.raw}, f, indent=2)

    def save_event_series_timestamp(self, event_series):
        path = f"{self.path}/timestamps/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/last_event_series", "w") as f:
            f.write(str(event_series.created_at))

    def get_event_series_timestamp(self):
        path = f"{self.path}/timestamps/last_event_series"
        if not os.path.exists(path):
            return 0
        with open(path, "r") as f:
            return int(f.read())

    def stream_events(self, timestamp=None):
        for data in stream_data_from(f"{self.path}/events"):
            event = Event(data["data"])
            if timestamp is None or event.start.unix >= timestamp:
                yield event

    def get_stats(self) -> CacheStats:
        stats = CacheStats(location = self.path)
        first = None
        last = None
        count = 0
        for data in stream_data_from(f"{self.path}/events"):
            ts = data["timestamp"]
            if first is None or first > ts:
                first = ts
            if last is None or last < ts:
                last = ts
            count += 1

        stats.entities.append(CachedEntity(name="Events", count=count, first=first, last=last))
        return stats