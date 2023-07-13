


import datetime
from typing import List, Mapping
from core.scheduling.calendar import Calendar
from core.scheduling.event import Event

from core.workers.colaborator import Colaborator
from core.workers.producer import Junior, Producer, Senior
from core.workers.tech import Tech
from core.workers.vips import Actor, Director
from core.stages.stage import Stage

VALID_TYPE_WORKERS = ["senior", "junior", "actor", "realizador", "tecnico"]

class Application:


    def __init__(self):
      
      self.colabs:Mapping[str, Colaborator] = {}
      self.stages:Mapping[str, Stage] = {}

      self.tbd_calendar = Calendar()
      self.done_calendar = Calendar()



    def check_worker(self, type_worker:str, eww:bool, name:str, cost:int):

        # check if worker already exists
        if self.colabs.get(name, None):
            raise ValueError("Ja existe um colaborador com o mesmo nome.")
            
        # check if type is valid
        if type_worker not in VALID_TYPE_WORKERS:
            raise ValueError("Tipo de colaborador desconhecido.")
        
        if (type_worker == "actor" or type_worker == "realizador") \
            and eww != "vedeta" and eww != "normal":
                    raise ValueError(f"Notoriedade invalida.")
            
        # check if cost is valid
        if cost < 0:
            raise ValueError("Acha mesmo que este colaborador vai pagar para trabalhar?")
        

    def register_worker(self, type_worker:str, eww:str, name:str, cost:int):


        if type_worker == "senior":
            worker = Senior(name, cost)
        elif type_worker == "junior":
            worker = Junior(name, cost)
        elif type_worker == "actor":
            worker = Actor(name, cost, eww)
        elif type_worker == "realizador":
            worker = Director(name, cost, eww)
        elif type_worker == "tecnico":
            worker = Tech(name, cost)
        else:
            raise ValueError("Tipo de colaborador desconhecido.")

        self.colabs[name] = worker


    def print_staff(self) -> str:

        if len(self.colabs) == 0:
            return "Nao existem colaboradores registados."

        staff_str = [str(worker) for worker in self.colabs.values()]
        staff_str = "\n".join(staff_str)
        return staff_str


    def register_stage(self, stage_name, stage_price):

        stage = Stage(stage_name, stage_price)
        self.stages[stage_name] = stage

    def check_stage(self, stage_name:str, stage_price:int):

        if self.stages.get(stage_name, None):
            raise ValueError("Localizacao ja tinha sido registada.")

        if stage_price < 0:
            raise ValueError("Acha que eles nos pagam para gravar la?")
        
    def print_stages(self) -> str:

        if len(self.stages) == 0:
            return "Nao existem localizacoes registadas."

        stages_str = [str(stage) for stage in self.stages.values()]
        stages_str = "\n".join(stages_str)
        return stages_str
    

    def check_event(self, date:datetime.datetime, duration:int, stage_name:str, producer_name:str, director_name:str, tech_name:str, colabs:List[str]):
        if stage_name not in self.stages:
            raise ValueError("Local desconhecido.")
        
        if len(self.done_calendar.calendar) > 0:
            if max(self.done_calendar.calendar.keys()) > date:
                raise ValueError("Data de gravacao invalida.")
        
        if duration <= 0:
            raise ValueError("Duracao invalida.")
        
        if self.colabs.get(producer_name, None) is None or not isinstance(self.colabs[producer_name], Producer):
            raise ValueError("Produtor desconhecido.")

        if self.colabs.get(director_name, None) is None or not isinstance(self.colabs[director_name], Director):
            raise ValueError("Realizador desconhecido.")
        
        if self.colabs.get(tech_name, None) is None or not isinstance(self.colabs[tech_name], Tech):
            raise ValueError("Tecnico desconhecido.")
        
        for colab in colabs:
            if self.colabs.get(colab, None) is None:
                raise ValueError("Colaborador desconhecido.")
    
    
    def schedule(self, date:datetime.datetime, 
                 duration:int, 
                 stage_name:str, producer_name:str, director_name:str, tech_name:str, 
                 colabs:List[str]):
        

        event = Event(date, duration, stage_name, producer_name, director_name, tech_name, colabs)
        
        event_workers = [producer_name, director_name, tech_name] + colabs
        

        for worker_name in event_workers:
            self.colabs[worker_name].calendar.add_event(event)
        
        self.stages[stage_name].calendar.add_event(event)

        self.tbd_calendar.add_event(event) 