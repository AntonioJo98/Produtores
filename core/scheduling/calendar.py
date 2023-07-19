



from datetime import datetime, timedelta
from typing import List


from core.scheduling.event import Event


class Calendar:


    def __init__(self) -> None:
        
        self.calendar:List[Event] = []


    def __len__(self) -> int:
        return len(self.calendar)
    
    def __str__(self, include_stage=True) -> str:
        events = sorted(self.calendar, key=lambda x: x.start)
        # events = list(self.calendar.values())
        events_str = []
        for event in events:
            e_str = event.__str__(include_stage)
            if event.feud_number:
                e_str += " Suspensa!"
            events_str.append(e_str)

        return "\n".join(events_str)
    
    def get_total_cost(self, include_suspended=True) -> int:
        if include_suspended:
            return sum([e.get_cost() for e in self.calendar])
        else:
            return sum([e.get_cost() for e in self.calendar if e.feud_number == 0])
        
    def pop(self, event:Event) -> Event:
        return self.calendar.remove(event)

    def add_event(self, event:Event) -> None:
        self.calendar.append(event)
        self.calendar = sorted(self.calendar, key=lambda x: x.start)

    # def change_event_date(self, event:Event, new_date:datetime) -> None:
    #     self.pop(event.start)
    #     self.calendar[new_date] = event

    def is_free(self, new_event_start:datetime, duration:int):
        new_event_end = new_event_start + timedelta(minutes=duration)
        conflict_events:List[Event] = []
        for event in self.calendar:
            if (event.start <= new_event_start < event.end) or (event.start < new_event_end <= event.end) or (new_event_start <= event.start and new_event_end >= event.end):
                # print(f"> {event.start} {event.end} {new_event_start} {new_event_end}")
                conflict_events.append(event)
                
        return conflict_events



       
        



    


