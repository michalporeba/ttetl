from tt_client import TTClient
from file_cache import FileCache


def get_events(timestamp=None):
  fc = FileCache()
  tt = TTClient.build()

  if timestamp is None:
    timestamp = fc.get_event_series_timestamp()

  for es in tt.get_event_series(timestamp):
    print()
    #print(es)
    for e in tt.get_events_in_series(es):
      print(e)
      fc.save_event(e)
      for tg in e.ticket_groups:
        print(tg)
        for t in tg.ticket_types:
          #print(t)
          pass
    fc.save_event_series_timestamp(es)
      #print('-------------------------')

def main():
  get_events() #1722000587


if __name__ == '__main__':
  main()

  #1723406845