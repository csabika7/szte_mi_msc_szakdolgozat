import redis
import json


class ActivatedModelsRepositoryClient:

    def __init__(self, unix_socket, key):
        self.unix_socket = unix_socket
        self.key = key

    def get_activated_models(self):
        with redis.Redis(unix_socket_path=self.unix_socket) as r:
            value = r.get(self.key)
            return json.loads(value)
