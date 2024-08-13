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
