from tt_client import TTClient


def main():
  tt = TTClient.build()
  for es in tt.get_event_series_since(0):
    print(f'EVENT SERIES: {es}')
    for tg in es.ticket_groups:
      print(f'\tTICKET: {tg}')


if __name__ == '__main__':
  main()