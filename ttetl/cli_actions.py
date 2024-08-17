from tt_client import TTClient
from file_cache import FileCache
from ttetl.tt_model import TicketGroupAggregate
from actions import get_config
from cli_printer import CliPrinter

printer = CliPrinter()

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
    yield e


def get_ticket_groups(events):
  groups = {}
  events_count = 0
  for e in events:
    events_count += 1
    for tg in e.ticket_groups:
      name = GROUP_NAME_CORRECTIONS.get(tg.name, tg.name)

      if not name in groups.keys():
        groups[name] = TicketGroupAggregate(name)
      groups[name].add(tg)

  print(f'events processed: {events_count}')
  for tg in groups.values():
    print(tg)
    for tt in tg.ticket_types:
      print(tt)


GROUP_NAME_CORRECTIONS = {
  'Ambulance Crew': 'Ambulance Crews',
  'ETA/PTA': 'Ambulance Crews',
  'PTA/ETA': 'Ambulance Crews',
  'Vehicle Crew': 'Ambulance Crews',
  'Emergency Ambulance': 'Ambulance Crews',
  'First Aider': 'First Aiders',
  'Command': 'Command & Support',
  'Command and Control': 'Command & Support',
  'Command & Control': 'Command & Support',
  'Event Management': 'Command & Support',
  'Healthcare Professional': 'Healthcare Professionals',
  'Health Care Professionals': 'Healthcare Professionals',
  'ALS Ambulance Crew': 'Healthcare Professionals',
  'Stadium HCPs': 'Healthcare Professionals',
  'HCP': 'Healthcare Professionals',
  "HCP's": 'Healthcare Professionals'
}


def main():
  #get_events_from_api() #1722000587
  fc = FileCache()
  events = fc.stream_events() #1722000587
  get_ticket_groups(events)


def test1():
  print("Hello")


def show_cache_stats():
  print('SHOWING CACHE STATS')


def show_config():
  get_config().accept_printer(printer)