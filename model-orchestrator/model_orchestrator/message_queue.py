import redis


class MessageQueueClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_message(self, channel, message):
        with redis.Redis(host=self.host, port=self.port, db=0) as r:
            r.publish(channel=channel, message=message)
