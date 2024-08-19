import json
import os
import time

from ttetl.tt_model import Event


class FileCache:
    def __init__(self, path="data"):
        self.path = path

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
        folder_path = f"{self.path}/events"
        if not os.path.exists(folder_path):
            return

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not filename.endswith(".json") or not os.path.isfile(file_path):
                continue
            with open(file_path, "r") as f:
                event = Event(json.load(f)["data"])
                if timestamp is None or event.start.unix >= timestamp:
                    yield event
