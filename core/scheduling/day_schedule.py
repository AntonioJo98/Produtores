




from datetime import datetime
from typing import List
from core.scheduling.event import Event

class DaySchedule:

    def __init__(self, day:datetime) -> None:
        self.day = day
        self.events:List[Event] = []

    def add_event(self, event:Event) -> None:
        self.events.append(event)

    def get_events(self) -> List[Event]:
        return self.events

    def get_day(self) -> datetime:
        return self.day