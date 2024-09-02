import logging
import time

import requests_cache

from datetime import timedelta
from ttetl.tt_model import EventSeries
from options import ApiOptions

logger = logging.getLogger(__name__)
HEADERS = {"Accept": "application/json"}

def get_time_limit(timestamp):
    if timestamp is None:
        return ""
    return f"&created_at.gt={timestamp}"


def get_data_and_next(options, session, auth, url):
    time.sleep(options.delay_seconds)
    response = session.get(url, auth=auth, headers=HEADERS)
    data = response.json().get("data")
    next_batch = response.json()["links"]["next"]
    return (data, next_batch)


def stream_data(options, session, auth, endpoint, timestamp=None):
    url = f"{options.url_base}{endpoint}?limit={options.batch_size}{get_time_limit(timestamp)}"
    (data, next_batch) = get_data_and_next(options, session, auth, url)

    while True:
        for d in data:
            yield d

        if next_batch is None:
            break

        (data, next_batch) = get_data_and_next(session, auth, f"{options.url_base}{next_batch}")


class TTClient:
    def __init__(self, options: ApiOptions):
        self.options = options
        self.api_key = options.keys[0]
        self.auth = (self.api_key, "")
        self.session = requests_cache.CachedSession()
        self.session.cache.delete(older_than=timedelta(seconds=options.cache_seconds))

    def stream_event_series(self, timestamp=None):
        for d in stream_data(
            self.options,
            self.session,
            self.auth,
            "/event_series",
            timestamp
        ):
            yield EventSeries(d)

    def stream_events_in_series(self, event_series):
        for d in stream_data(
            self.options,
            self.session,
            self.auth,
            f"/event_series/{event_series.id}/events"
        ):
            yield event_series.create_event(d)

    def stream_events(self, timestamp=None):
        for es in self.stream_event_series(timestamp):
            for e in self.stream_events_in_series(es):
                yield e

    def get_event(self, event_series_id, event_id):
        response = self.session.get(
            f"{self.otpions.url_base}/event_series/{event_series_id}/events/{event_id}",
            auth=self.auth,
            headers=HEADERS,
        )
        return None
