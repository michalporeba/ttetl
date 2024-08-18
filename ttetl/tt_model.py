def get_ticket_groups_from(data):
    return data.get("default_ticket_groups", data.get("ticket_groups", []))


def get_ticket_types_from(data):
    return data.get("default_ticket_types", data.get("ticket_types", []))


def get_int_value(property, data, default=None):
    value = data.get(property, None)
    if value is None:
        return default
    return int(value)


class TimePoint:
    def __init__(self, data):
        self.date = data.get("date", "")
        self.time = data.get("time", "")
        self.unix = data.get("unix", "")


class Event:
    def __init__(self, data):
        self.raw = data
        self.add_series_data(data.get("_series", {}))

        self.id = data["id"]
        self.event_series_id = data["event_series_id"]
        self.start = TimePoint(data.get("start", {}))
        self.end = TimePoint(data.get("end", {}))

        self.tickets_available = data["tickets_available"]
        self.total_issued_tickets = data["total_issued_tickets"]
        self.unavailable = data["unavailable"] == "true"

        self.group_tickets_from_data(data)

    def add_series_data(self, data):
        self.description = data.get("description")
        self.name = data.get("name")
        self.location_name = data.get("location_name")
        self.location_postcode = data.get("location_postcode")
        self.series_is_published = data.get("series_is_published", False)
        self.series_is_private = data.get("series_is_private", False)

    def add_other_tickets_group(self, other_ticket_types):
        if len(other_ticket_types) > 0:
            other_group = TicketGroup(
                {
                    "id": "other",
                    "name": "Other",
                    "ticket_ids": list(other_ticket_types.keys()),
                }
            )
            other_group.ticket_types = other_ticket_types.values()
            self.ticket_groups.append(other_group)

    def group_tickets_from_data(self, data):
        types = {tt["id"]: TicketType(tt) for tt in get_ticket_types_from(data)}
        self.ticket_groups = [TicketGroup(dtg) for dtg in get_ticket_groups_from(data)]
        for tg in self.ticket_groups:
            for tt in tg.ticket_ids:
                tg.ticket_types.append(types.pop(tt))

        self.add_other_tickets_group(types)

    def duration(self):
        return round((self.end.unix - self.start.unix) / 60 / 60, 2)

    def quantity_total(self):
        return sum([tg.quantity_total() for tg in self.ticket_groups])

    def quantity_issued(self):
        return sum([tg.quantity_issued() for tg in self.ticket_groups])

    def __str__(self):
        identity = f"[{self.id}] {self.name} ({self.start.date})"
        duration = f"{self.duration()} hours"
        levels = f"[{self.quantity_issued()}/{self.quantity_total()}]"
        return f"EVENT: {identity} - {duration} - {levels}"


class EventSeries:
    def __init__(self, data):
        self.raw = data
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.description = data.get("description", "")
        self.name = data.get("name", "")
        self.is_published = data["status"] == "published"
        self.is_private = data["private"] == "true"
        self.location_name = data.get("venue", {}).get("name", "")
        self.location_postcode = data.get("venue", {}).get("postal_code", "")

    def _data_for_event(self):
        return {
            "_series": {
                "description": self.description,
                "name": self.name,
                "location_name": self.location_name,
                "location_postcode": self.location_postcode,
                "series_is_published": self.is_published,
                "series_is_private": self.is_private,
            }
        }

    def create_event(self, data):
        return Event({**self._data_for_event(), **data})

    def __str__(self):
        return f"EVENT SERIES: {self.name} [{self.id}]"


class TicketGroup:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.ticket_ids = data["ticket_ids"]
        self.max_per_order = get_int_value("max_per_order", data)
        self.min_per_order = get_int_value("min_per_order", data)
        self.price = get_int_value("price", data, 0)
        self.ticket_types = []

    def quantity_total(self):
        if self.min_per_order is not None:
            return self.min_per_order
        if self.max_per_order is not None:
            return self.max_per_order
        return sum([t.quantity_total for t in self.ticket_types])

    def quantity_issued(self):
        return sum([t.quantity_issued for t in self.ticket_types])

    def __str__(self):
        identity = f"[{self.id}] {self.name}"
        levels = f"[{self.quantity_issued()}/{self.quantity_total()}]"
        return f"TICKET GROUP: {identity} {levels}"


class TicketGroupAggregate:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.elements = []
        self.ticket_ids = []
        self.ticket_types = []

    def add(self, other):
        self.count += 1
        self.ticket_ids += other.ticket_ids
        self.elements.append(other)

        current = {tt.name: tt for tt in self.ticket_types}
        for tt in other.ticket_types:
            if tt.name not in current.keys():
                current[tt.name] = TicketTypeAggregate(tt.name)
            current[tt.name].add(tt)
        self.ticket_types = current.values()

    def quantity_total(self):
        return sum([t.quantity_total() for t in self.elements])

    def quantity_issued(self):
        return sum([t.quantity_issued() for t in self.elements])

    def __str__(self):
        identity = f"TICKET GROUP: {self.name}"
        levels = f"[{self.quantity_issued()}/{self.quantity_total()}]"
        return f"{identity} {levels}"


class TicketType:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.price = get_int_value("price", data, 0)
        self.quantity_available = get_int_value("quantity", data, 0)
        self.quantity_held = get_int_value("quantity_held", data, 0)
        self.quantity_issued = get_int_value("quantity_issued", data, 0)
        self.quantity_total = get_int_value("quantity_total", data, 0)

    def __str__(self):
        identity = f"TICKET TYPE: {self.name} [{self.id}]"
        level = f"{self.quantity_issued}/{self.quantity_total}"
        return f"{identity} {level}"


class TicketTypeAggregate:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.elements = []
        self.quantity_available = 0
        self.quantity_held = 0
        self.quantity_issued = 0
        self.quantity_total = 0

    def add(self, ticket_type):
        self.elements.append(ticket_type)
        self.count += 1
        self.quantity_available += ticket_type.quantity_available
        self.quantity_held += ticket_type.quantity_held
        self.quantity_issued += ticket_type.quantity_issued
        self.quantity_total += ticket_type.quantity_total

    def __str__(self):
        return (
            f"TICKET TYPE: {self.name} [{self.quantity_issued}/{self.quantity_total}]"
        )
