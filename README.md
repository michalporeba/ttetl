# ttetl
Ticket Tailor API Python client for data analysis. 


set `TICKET_TAILOR_API` environmental variable

# Usage

To get data from the API, first set up the API key in `TICKET_TAILOR_API` environmental variable.

```python
api_key = '...your.api.key.here...'
tt = TTClient(api_key)
```

Process events
```python
  
```

Process event series and events
```python
for es in tt.stream_event_series(timestamp):
  print(es)
  for e in tt.stream_events_in_series(es):
    print(e)
    for tg in e.ticket_groups:
      print(tg)
      for t in tg.ticket_types:
        print(t)
```
