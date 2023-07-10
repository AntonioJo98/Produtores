




from workers import Colaborator


class Vedeta(Colaborator):


    def __init__(self, name:str, cost:int, eww:bool):

        super().__init__(name, cost)

        self.famous = eww

        self.burnbook = []


class Actor(Vedeta):

    def __init__(self, name:str, cost:int, eww:bool):

        super().__init__(name, cost, eww)



class Director(Vedeta):

    def __init__(self, name:str, cost:int, eww:bool):

        super().__init__(name, cost, eww)

