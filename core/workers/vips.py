



from core.workers.colaborator import Colaborator

class Vedeta(Colaborator):


    def __init__(self, name:str, cost:int, eww:str):

        super().__init__(name, cost)

        self.famous:str = eww # eww = "vedeta" ou "normal"

        self.burnbook = []



class Actor(Vedeta):

    def __init__(self, name:str, cost:int, eww:str):

        super().__init__(name, cost, eww)

        self.type = f"actor {self.famous}"


class Director(Vedeta):

    def __init__(self, name:str, cost:int, eww:str):

        super().__init__(name, cost, eww)

        self.type = f"realizador {self.famous}"


