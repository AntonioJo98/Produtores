


from datetime import datetime, timedelta
from typing import List


class Event:
    def __init__(self,
                 day:datetime, 
                 duration:int,
                 stage_name:str, producer_name:str, director_name:str, tech_name:str, 
                 colabs:List[str]) -> None:
       
        self.start = day
        self.end = self.start + timedelta(minutes=duration)
        self.duration = duration
        self.stage_name = stage_name
        self.producer_name = producer_name
        self.director_name = director_name
        self.tech_name = tech_name
        self.optionals = colabs

        self.feud_number = 0

    def define_cost(self, cost:int) -> None:
        self.event_cost = cost

    def get_cost(self) -> int:
        return self.event_cost
    
    def suspend_recording(self) -> None:
        self.feud_number += 1  

    def resume_recording(self) -> None:
        self.feud_number -= 1
    
    def get_all_workers(self) -> List[str]:
        return [self.producer_name, self.director_name, self.tech_name] + self.optionals
    
    def get_alloted_hours(self) -> int:
        return self.duration // 60 + int((self.duration % 60) > 0)

    def __str__(self, include_stage=True) -> str:
        if include_stage:
            event_str = f"{datetime.strftime(self.start, '%Y %#m %#d')}; {self.stage_name}; {self.producer_name}; {self.director_name}."
        else:
            event_str = f"{datetime.strftime(self.start, '%Y %#m %#d')}; {self.producer_name}; {self.director_name}."

        return event_str
    