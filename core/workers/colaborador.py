




class Colaborator:


    def __init__(self, name:str, cost:int):

        self.name = name
        self.cost = cost

        self.calendar = []


    def add_appointment(self, appointment):

        self.calendar.append(appointment)





if __name__ == "__main__":
    worker = Colaborator("Joao", 100)


    worker.add_appointment("2020-01-01 10:00:00")

    