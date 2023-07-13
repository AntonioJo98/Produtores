



from datetime import datetime
from typing import Mapping

from core.scheduling.day_schedule import DaySchedule
from core.scheduling.event import Event


class Calendar:


    def __init__(self) -> None:
        
        self.calendar:Mapping[datetime, DaySchedule] = {}


    def add_event(self, event:Event) -> None:

        if event.day in self.calendar:
            self.calendar[event.day].add_event(event)
        else:
            day_schedule = DaySchedule(event.day)
            day_schedule.add_event(event)
            self.calendar[event.day] = day_schedule
        


    


