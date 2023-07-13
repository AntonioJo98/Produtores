




from core.scheduling.calendar import Calendar


class Stage:

    def __init__(self, stage_name:str, stage_price:int):

        self.name = stage_name
        self.cost = stage_price

        self.calendar = Calendar()

    def __str__(self) -> str:
        return f"{self.name} {self.cost}."
