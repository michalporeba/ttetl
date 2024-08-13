import os
import json
import time

class FileCache:
  def __init__(self, path='data'):
    self.path = path

  def save_event(self, event):
    path = f'{self.path}/events/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}{event.id}.json', 'w') as f:
      json.dump({
        'timestamp': int(time.time()),
        'data': event.raw
      }, f, indent=2)

  def save_event_series_timestamp(self, event_series):
    path = f'{self.path}/timestamps/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f'{path}/last_event_series', 'w') as f:
       f.write(str(event_series.created_at))

  def get_event_series_timestamp(self):
     path = f'{self.path}/timestamps/last_event_series'
     if not os.path.exists(path):
        return 0
     with open(path, 'r') as f:
        return int(f.read())