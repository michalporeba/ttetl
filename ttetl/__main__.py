from tt_client import TTClient
from file_cache import FileCache


def get_events_from_api(timestamp=None):
  fc = FileCache()
  tt = TTClient.build()

  if timestamp is None:
    timestamp = fc.get_event_series_timestamp()

  for es in tt.stream_event_series(timestamp):
    for e in tt.stream_events_in_series(es):
      print(e)
      fc.save_event(e)
    fc.save_event_series_timestamp(es)


def stream_events_from_cache(timestamp=None):
  fc = FileCache()
  for e in fc.stream_events(timestamp):
    print(e)


def main():
  #get_events_from_api() #1722000587
  stream_events_from_cache()


if __name__ == '__main__':
  main()

  #1723406845