
class ActiveModel:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url
        }

    def __str__(self):
        return f'ActiveModel({self.name},{self.url})'


class ActiveModelList:

    def __init__(self, models: list):
        self.models = models

    def to_dict(self):
        return {
            "models": [model.to_dict() for model in self.models]
        }

    def __str__(self):
        return f'ActiveModelList({self.models})'


class ActivationEvent:

    def __init__(self, model_id, state):
        self.model_id = model_id
        self.state = state

    def __str__(self):
        return f'ActivationEvent({self.model_id},{self.state})'

