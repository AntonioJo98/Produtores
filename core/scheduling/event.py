


from datetime import datetime
from typing import List


class Event:
    def __init__(self,
                 day:datetime, 
                 duration:int, 
                 stage_name:str, producer_name:str, director_name:str, tech_name:str, 
                 colabs:List[str]) -> None:
       
        self.day = day
        self.duration = duration
        self.stage_name = stage_name
        self.producer_name = producer_name
        self.director_name = director_name
        self.tech_name = tech_name
        self.colabs = colabs

    def __str__(self) -> str:
        return f"{self.name} {self.day.strftime('%H:%M')}"