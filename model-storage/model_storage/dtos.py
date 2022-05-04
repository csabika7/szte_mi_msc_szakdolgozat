

class Model:

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return f'Model({self.id}, {self.name})'


class ModelList:

    def __init__(self, models: list):
        self.models = models

    def to_dict(self):
        return {
            "models": [model.to_dict() for model in self.models]
        }

    def __str__(self):
        return f'ModelList({self.models})'
