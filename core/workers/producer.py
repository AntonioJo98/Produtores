


from workers import Colaborator


class Producer(Colaborator):


    def __init__(self, name:str, cost:int):

        super().__init__(name, cost)



class Junior(Producer):


    def __init__(self, name:str, cost:int):

        super().__init__(name, cost)


class Senior(Producer):

    
        def __init__(self, name:str, cost:int):
    
            super().__init__(name, cost)


