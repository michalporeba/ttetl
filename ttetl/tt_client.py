import os
import time

import requests_cache

from ttetl.tt_model import EventSeries

BATCH_SIZE = 100
HEADERS = {"Accept": "application/json"}
URL_BASE = "https://api.tickettailor.com/v1"
API_DELAY = 0.05


def get_time_limit(timestamp):
    if timestamp is None:
        return ""
    return f"&created_at.gt={timestamp}"


def get_data_and_next(session, auth, url):
    time.sleep(API_DELAY)
    response = session.get(url, auth=auth, headers=HEADERS)
    data = response.json().get("data")
    next_batch = response.json()["links"]["next"]
    return (data, next_batch)


def stream_data(session, auth, endpoint, timestamp=None):
    url = f"{URL_BASE}{endpoint}?limit={BATCH_SIZE}{get_time_limit(timestamp)}"
    (data, next_batch) = get_data_and_next(session, auth, url)

    while True:
        for d in data:
            yield d

        if next_batch is None:
            break

        (data, next_batch) = get_data_and_next(session, auth, f"{URL_BASE}{next_batch}")


class TTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth = (api_key, "")
        self.session = requests_cache.CachedSession("demo_cache")

    def stream_event_series(self, timestamp=None):
        for d in stream_data(self.session, self.auth, "/event_series", timestamp):
            yield EventSeries(d)

    def stream_events_in_series(self, event_series):
        for d in stream_data(
            self.session, self.auth, f"/event_series/{event_series.id}/events"
        ):
            yield event_series.create_event(d)

    def stream_events(self, timestamp=None):
        for es in self.stream_event_series(timestamp):
            for e in self.stream_events_in_series(es):
                yield e

    def get_event(self, event_series_id, event_id):
        response = self.session.get(
            f"{URL_BASE}/event_series/{event_series_id}/events/{event_id}",
            auth=self.auth,
            headers=HEADERS,
        )
        return None

    def build():
        api_key = os.environ["TICKET_TAILOR_API"]
        return TTClient(api_key)
