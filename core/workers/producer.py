

from core.workers.colaborator import Colaborator


class Producer(Colaborator):


    def __init__(self, name:str, cost:int):

        super().__init__(name, cost)



class Junior(Producer):


    def __init__(self, name:str, cost:int):

        super().__init__(name, cost)

        self.type = "produtor junior"


class Senior(Producer):

    
        def __init__(self, name:str, cost:int):
    
            super().__init__(name, cost)

            self.type = "produtor senior"


if __name__ == "__main__":
     
    worker = Senior("Joao", 100)

    print(worker)


