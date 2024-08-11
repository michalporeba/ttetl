def get_ticket_groups_from(data):
    return data.get('default_ticket_groups', data.get('ticket_groups', []))

def get_ticket_types_from(data):
    return data.get('default_ticket_types', data.get('ticket_types', []))

def get_int_value(property, data, default=None):
  value = data.get(property, None)
  if value is None:
    return default
  return int(value)

class Event:
  def __init__(self, series, data):
    self.raw = data
    self.id = data['id']
    self.description = series.description
    self.name = series.name
    self.location_name = series.location_name
    self.location_postcode = series.location_postcode
    self.start = {
      "date": data.get('start', {}).get('date', ''),
      "time": data.get('start', {}).get('time', ''),
      "unix": data.get('start', {}).get('unix', '')
    }
    self.end = {
      "date": data.get('end', {}).get('date', ''),
      "time": data.get('end', {}).get('time', ''),
      "unix": data.get('end', {}).get('unix', '')
    }
    self.tickets_available = data['tickets_available']
    self.total_issued_tickets = data['total_issued_tickets']
    self.unavailable = data['unavailable'] == 'true'
    types = { tt['id']: TicketType(tt) for tt in get_ticket_types_from(data)}
    self.ticket_groups = [TicketGroup(dtg) for dtg in get_ticket_groups_from(data)]
    for tg in self.ticket_groups:
      for tt in tg.ticket_ids:
        tg.ticket_types.append(types.pop(tt))
    self.ticket_types = types.values()

  def duration(self):
    return (self.end["unix"] - self.start["unix"])/60/60

  def __str__(self):
    return f'EVENT: {self.name} ({self.start["date"]}) {self.duration()} hours [{self.id}]'

class EventSeries:
  def __init__(self, data):
    self.raw = data
    self.id = data['id']
    self.created_at = data['created_at']
    self.description = data.get('description','')
    self.name = data.get('name','')
    self.is_published = data['status'] == 'published'
    self.is_private = data['private'] == 'true'
    self.location_name = data.get('venue', {}).get('name', '')
    self.location_postcode = data.get('venue', {}).get('postal_code', '')
    #self.ticket_groups = [TicketGroup(dtg) for dtg in get_ticket_groups_from(data)]
    #self.ticket_types = [TicketType(tt) for tt in get_ticket_types_from(data)]

  def create_event(self, data):
    return Event(self, data)

  def __str__(self):
    return f'EVENT SERIES: {self.name} [{self.id}]'


class TicketGroup:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.ticket_ids = data['ticket_ids']
    self.max_per_order = get_int_value('max_per_order', data)
    self.min_per_order = get_int_value('min_per_order', data, self.max_per_order)
    self.price = get_int_value('price', data, 0)
    self.ticket_types = []

  def quantity_issued(self):
    return sum([t.quantity_issued for t in self.ticket_types])

  def __str__(self):
    return f'TICKET GROUP: {self.name} [{self.id}] {self.quantity_issued()}/{self.min_per_order}'


class TicketType:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.price = get_int_value('price', data, 0)
    self.quantity_available = get_int_value('quantity', data, 0)
    self.quantity_held = get_int_value('quantity_held', data, 0)
    self.quantity_issued = get_int_value('quantity_issued', data, 0)
    self.quantity_total = get_int_value('quantity_total', data, 0)

  def __str__(self):
    return f'TICKET TYPE: {self.name} [{self.id}] {self.quantity_issued}/{self.quantity_total}'