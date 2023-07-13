


from core.workers.colaborator import Colaborator

class Tech(Colaborator):


    def __init__(self, name, cost):

        super().__init__(name, cost)

        self.type = "tecnico"