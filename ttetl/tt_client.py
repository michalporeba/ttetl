import os
import requests
import requests_cache
from model import EventSeries

BATCH_SIZE = 5
HEADERS = {
  'Accept': 'application/json'
}
URL_BASE = 'https://api.tickettailor.com/v1/'




session = requests_cache.CachedSession('demo_cache')
for i in range(60):
    session.get('https://httpbin.org/delay/1')

class TTClient:

  def __init__(self, api_key):
    self.api_key = api_key
    self.auth = (api_key,'')
    self.session = requests_cache.CachedSession('demo_cache')


  def get_event_series_since(self, time):
    response = self.session.get(f'{URL_BASE}event_series?limit={BATCH_SIZE}', auth=self.auth, headers=HEADERS)
    for d in response.json()['data']:
      yield EventSeries(d)


  def build():
    api_key = os.environ['TICKET_TAILOR_API']
    return TTClient(api_key)
