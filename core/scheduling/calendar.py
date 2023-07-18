



from datetime import datetime
from collections import OrderedDict


from core.scheduling.event import Event


class Calendar:


    def __init__(self) -> None:
        
        self.calendar:OrderedDict[datetime, Event] = {}


    def __len__(self) -> int:
        return len(self.calendar)
    
    def __str__(self, include_stage=True) -> str:
        events = list(self.calendar.values())
        events_str = []
        for event in events:
            e_str = event.__str__(include_stage)
            if event.feud_number:
                e_str += " Suspensa!"
            events_str.append(e_str)

        return "\n".join(events_str)
    
    def get_total_cost(self, include_suspended=True) -> int:
        if include_suspended:
            return sum([e.get_cost() for e in self.calendar.values()])
        else:
            return sum([e.get_cost() for e in self.calendar.values() if e.feud_number == 0])
        
    def pop(self, date:datetime) -> Event:
        return self.calendar.pop(date)

    def add_event(self, event:Event) -> None:
        self.calendar[event.start] = event
       
        



    


