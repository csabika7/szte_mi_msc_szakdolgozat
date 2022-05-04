

class Model:

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f'Model({self.id}, {self.name})'
