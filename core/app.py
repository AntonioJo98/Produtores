


import datetime
from typing import List, Mapping
from core.scheduling.calendar import Calendar
from core.scheduling.event import Event

from core.workers.colaborator import Colaborator
from core.workers.producer import Junior, Producer, Senior
from core.workers.tech import Tech
from core.workers.vips import Actor, Director, Vedeta
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
    
    def print_done(self) -> str:
        if len(self.done_calendar) == 0:
            return "Nenhuma gravacao realizada."
        
        done_str = self.done_calendar.__str__()
        done_str = done_str.replace("Suspensa!", "Cancelada!") 

        done_str += f"\n{self.done_calendar.get_total_cost(include_suspended=False)} euros gastos."
    

        return done_str
    
    def print_scheduled(self) -> str:
        return self.print_tbd(self.tbd_calendar)

    def print_tbd_colaborator(self, name:str) -> str:
        if name not in self.colabs:
            raise ValueError("Colaborador desconhecido.")
        
        if len(self.colabs[name].calendar) == 0:
            return f"Nenhuma gravacao prevista com {name}."
        
        return self.print_tbd(self.colabs[name].calendar, include_stage=False)
    
    def print_tbd_stage(self, stage_name:str) -> str:
        if stage_name not in self.stages:
            raise ValueError("Local desconhecido.")
        
        if len(self.stages[stage_name].calendar) == 0:
            return f"Nenhuma gravacao prevista em {stage_name}."
        
        return self.print_tbd(self.stages[stage_name].calendar, include_stage=False)
    
    def print_tbd(self, tbd:Calendar, include_stage=True) -> str:
        if len(tbd) == 0:
            return "Nenhuma gravacao prevista."
        
        tbd_str = tbd.__str__(include_stage)
        tbd_str += f"\n{tbd.get_total_cost()} euros orcamentados."

        return tbd_str


    def _calc_event_cost(self, event:Event) -> int:

        event_cost = 0

        allotad_hours = event.get_alloted_hours()

        event_cost += self.stages[event.stage_name].get_cost()
        event_cost += self.colabs[event.producer_name].get_cost()
        event_cost += self.colabs[event.director_name].get_cost()
        event_cost += self.colabs[event.tech_name].get_cost()

        event_cost += sum([self.colabs[n_person].get_cost() for n_person in event.optionals])

        return event_cost*allotad_hours
    

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
            
        result = self._conflicts(date, duration, stage_name, producer_name, director_name, tech_name, colabs)

        if isinstance(result, list):
            for event in result:
               self._reschedule(event)
            return True
        else: 
            if result:
                raise ValueError("Gravacao nao agendada por conflito de datas.")
        
        return False


    def _conflicts(self, start:datetime.datetime, duration:int, stage_name:str, producer_name:str, director_name:str, tech_name:str, colabs:List[str]):
        
        reschedules = [] # in the case the producer is senior, there can be a number of reschedules to be made
        
        stage = self.stages[stage_name]
        stage_calendar = stage.calendar
        event_in_conflict = stage_calendar.is_free(start, duration)

        for event in event_in_conflict:
            producer_conflict_name = event.producer_name
            producer_conflict = self.colabs[producer_conflict_name]
            new_producer = self.colabs[producer_name]
            if isinstance(producer_conflict, Junior) and isinstance(new_producer, Senior):
                if event not in reschedules:
                    reschedules.append(event) # reschedule
            else:
                return True # there's a conflict and, thus, this event cannot be scheduled
        
        workers = [producer_name, director_name, tech_name] + colabs
        for worker_name in workers:
            worker_calendar = self.colabs[worker_name].calendar
            event_in_conflict = worker_calendar.is_free(start, duration)

            for event in event_in_conflict:
                producer_conflict_name = event.producer_name
                producer_conflict = self.colabs[producer_conflict_name]
                new_producer = self.colabs[producer_name]
                if isinstance(producer_conflict, Junior) and isinstance(new_producer, Senior):
                    if event not in reschedules:
                        reschedules.append(event) # reschedule
                else:
                    return True # there's a conflict and, thus, this event cannot be scheduled

        if len(reschedules) > 0:
           return reschedules # return the list of events to be rescheduled
        return False # there's no conflict and, thus, this event can be scheduled


    def _reschedule(self, event:Event) -> None:
        current_day = event.start + datetime.timedelta(days=0)
        event_duration = event.duration

        event_stage = self.stages[event.stage_name]
        event_workers = [event.producer_name, event.director_name, event.tech_name] + event.optionals

        while True:
            current_day = current_day + datetime.timedelta(days=1)

            booked = event_stage.calendar.is_free(current_day, event_duration)
            if len(booked) > 0:
                continue

            for worker_name in event_workers:
                worker = self.colabs[worker_name]
                booked = worker.calendar.is_free(current_day, event_duration)
                if len(booked) > 0:
                    break

            if len(booked) == 0:
                break

        event.start = current_day

    
    def schedule(self, date:datetime.datetime, 
                 duration:int, 
                 stage_name:str, producer_name:str, director_name:str, tech_name:str, 
                 colabs:List[str]) -> bool:
        
        event = Event(date, duration, stage_name, producer_name, director_name, tech_name, colabs)
        event.define_cost(self._calc_event_cost(event))

        event_workers = [producer_name, director_name, tech_name] + colabs
        
        for worker_name in event_workers:
            worker = self.colabs[worker_name]
            worker.calendar.add_event(event)
            if isinstance(worker, Vedeta) and worker.famous == "vedeta":
                if len(worker.burnbook) != 0:
                    for burn in worker.burnbook:
                        if burn in event_workers:
                            event.suspend_recording()    

        self.stages[stage_name].calendar.add_event(event)
        self.tbd_calendar.add_event(event) 

        return event.feud_number > 0


    def record(self):

        if len(self.tbd_calendar) == 0:
            return "Nenhuma gravacao agendada."
        
        event = next(iter(self.tbd_calendar.calendar))
        
        self.tbd_calendar.pop(event)
        self.done_calendar.add_event(event)

        for worker_name in event.get_all_workers():
            self.colabs[worker_name].calendar.pop(event)
        
        self.stages[event.stage_name].calendar.pop(event)

        if event.feud_number == 0:
            return f"{event} Gravada!"
        
        return f"{event} Cancelada!"
    
    def amua(self, vedeta_name:str, colaborador:str) -> int:
        
        vedeta:Vedeta = self.colabs[vedeta_name]

        vedeta.burn(colaborador)

        vedeta_calendar = vedeta.calendar
        colaborador_calendar = self.colabs[colaborador].calendar

        common_recordings = [event for date, event in vedeta_calendar.calendar.items() if date in colaborador_calendar.calendar]
        
        suspend_counter = 0
        for event in common_recordings:
            if event.feud_number == 0:
                suspend_counter += 1
            event.suspend_recording()

        return suspend_counter    

    def check_amua(self, vedeta_name:str, colaborador:str):
        if vedeta_name not in self.colabs:
            raise ValueError(f"{vedeta_name} nao e uma vedeta.")
        
        vedeta = self.colabs[vedeta_name]
        if not isinstance(vedeta, Vedeta) or vedeta.famous != "vedeta":
            raise ValueError(f"{vedeta_name} nao e uma vedeta.")

        if colaborador not in self.colabs:  
            raise ValueError(f"{colaborador} nao e um colaborador.")

        if colaborador in vedeta.burnbook:
            raise ValueError(f"Que falta de paciencia para divas...")


    def reconcilia(self, vedeta_name:str, colaborador:str) -> int:

        vedeta:Vedeta = self.colabs[vedeta_name]

        vedeta.hug(colaborador)

        vedeta_calendar = vedeta.calendar
        colaborador_calendar = self.colabs[colaborador].calendar

        common_recordings = [event for date, event in vedeta_calendar.calendar.items() if date in colaborador_calendar.calendar]

        saved_counter = 0
        for event in common_recordings:
            event.resume_recording()
            if event.feud_number == 0:
              saved_counter += 1

        return saved_counter
        

    def check_reconcilia(self, vedeta_name:str, colaborador:str):
        if vedeta_name not in self.colabs:
            raise ValueError(f"{vedeta_name} nao e uma vedeta.")
        
        vedeta = self.colabs[vedeta_name]
        if not isinstance(vedeta, Vedeta) or vedeta.famous != "vedeta":
            raise ValueError(f"{vedeta_name} nao e uma vedeta.")
        
        if colaborador not in vedeta.burnbook or colaborador not in self.colabs:
            raise ValueError(f"Nao existe zanga com {colaborador}.")
        


    def print_amuancos(self, vedeta_name:str) -> str:
        vedeta:Vedeta = self.colabs[vedeta_name]
        vedeta_burnbook = vedeta.burnbook

        if len(vedeta_burnbook) == 0:
            return f"{vedeta_name} da-se bem com todos!"
        
        amuancos_str =""
        # brunbook = ["colab1", "colab2", ..., "colabk"]
        for colaborador in vedeta_burnbook:
            amuancos_str += colaborador + "\n"

        return amuancos_str


    def check_amuancos(self, vedeta_name:str):

        vedeta = self.colabs.get(vedeta_name, None)  
              
        if vedeta is None or not isinstance(vedeta, Vedeta) or vedeta.famous != "vedeta":
            raise ValueError(f"Mas quem e {vedeta_name}?")