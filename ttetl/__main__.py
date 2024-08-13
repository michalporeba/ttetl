from tt_client import TTClient
from file_cache import FileCache

def main():
  fc = FileCache()
  tt = TTClient.build()
  for es in tt.get_event_series(1722000587):
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

      #print('-------------------------')


if __name__ == '__main__':
  main()

  #1723406845