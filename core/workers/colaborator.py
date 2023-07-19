


from core.scheduling.calendar import Calendar


class Colaborator:


    def __init__(self, name:str, cost:int):

        self.name = name
        self.cost = cost

        self.type = None

        self.calendar = Calendar()

    def get_cost(self) -> int:
        return self.cost

    
    def __str__(self) -> str:
        return f"{self.type} {self.name} {self.cost}"


if __name__ == "__main__":
    worker = Colaborator("Joao", 100)

    print(worker)

    