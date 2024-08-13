import os
import requests
import requests_cache
import time
from model import Event, EventSeries

BATCH_SIZE = 100
HEADERS = {
  'Accept': 'application/json'
}
URL_BASE = 'https://api.tickettailor.com/v1'
API_DELAY = 0.05


def get_time_limit(timestamp):
  if timestamp is None:
    return ''
  return f'&created_at.gt={timestamp}'


def stream_data(session, auth, endpoint, timestamp = None):
  url = f'{URL_BASE}{endpoint}'
  ts = get_time_limit(timestamp)
  response = session.get(f'{url}?limit={BATCH_SIZE}{ts}', auth=auth, headers=HEADERS)

  time.sleep(API_DELAY)
  data = response.json().get('data')
  next_batch = response.json()['links']['next']

  while True:
    for d in data:
      yield d

    if next_batch is None:
      break

    time.sleep(API_DELAY)
    response = session.get(f'{URL_BASE}{next_batch}', auth=auth, headers=HEADERS)
    data = response.json()['data']
    next_batch = response.json()['links']['next']


class TTClient:

  def __init__(self, api_key):
    self.api_key = api_key
    self.auth = (api_key,'')
    self.session = requests_cache.CachedSession('demo_cache')


  def get_event_series(self, timestamp=None):
    for d in stream_data(self.session, self.auth, '/event_series', timestamp):
      yield EventSeries(d)

  def get_events_in_series(self, event_series):
    for d in stream_data(self.session, self.auth, f'/event_series/{event_series.id}/events'):
      yield event_series.create_event(d)

  def get_event(self, event_id):
    pass

  def build():
    api_key = os.environ['TICKET_TAILOR_API']
    return TTClient(api_key)
