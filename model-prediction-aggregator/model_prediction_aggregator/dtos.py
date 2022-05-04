

class ActiveModel:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return f'ActiveModel({self.name},{self.url})'


class PredictionResponse:

    def __init__(self, name, certainty):
        self.name = name
        self.certainty = certainty

    def to_dict(self):
        return {
            "name": self.name,
            "certainty": self.certainty
        }

    def __str__(self):
        return f'PredictionResponse({self.name},{self.certainty})'
