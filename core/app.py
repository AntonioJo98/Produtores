


from typing import List

from Produtores.core.workers.colaborador import Colaborator
from Produtores.core.workers.producer import Junior, Senior
from Produtores.core.workers.tech import Tech
from Produtores.core.workers.vips import Actor, Director


class Application:


    def __init__(self):
      
      self.colabs:List[Colaborator] = []



    def register_worker(self, type_worker:str, eww:bool, name:str, cost:int):
       
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

        

        self.colabs.append(worker)

        