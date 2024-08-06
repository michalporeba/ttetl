from tt_client import TTClient


def main():
  tt = TTClient.build()
  for es in tt.get_event_series():
    print(es)
    for e in tt.get_events_in_series(es):
      print(e)
      for tg in e.ticket_groups:
        print(tg)
        for t in tg.tickets:
          print(t)


if __name__ == '__main__':
  main()