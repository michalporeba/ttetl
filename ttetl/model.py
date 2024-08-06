def get_ticket_groups_from(data):
    return data.get('default_ticket_groups', data.get('ticket_groups', []))


class EventSeries:
  def __init__(self, data):
    self.raw = data
    self.id = data['id']
    self.created_at = data['created_at']
    self.description = data['description']
    self.name = data['name']
    self.is_published = data['status'] == 'published'
    self.is_private = data['private'] == 'true'
    self.location_name = data.get('venue', {}).get('name', '')
    self.location_postcode = data.get('venue', {}).get('postal_code', '')
    self.ticket_groups = [TicketGroup(dtg) for dtg in get_ticket_groups_from(data)]

  def __str__(self):
    return f'{self.name} [{self.id}]'


class TicketGroup:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    #self.max_tickets = int(data.get('max_per_order', '0'))


  def __str__(self):
    return f'{self.name} [{self.id}]'