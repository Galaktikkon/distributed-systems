class ClientData:
    def __init__(self):
        self.active_stream = None
        self.subscriptions = {}
        self.buffer = []
        self.listening = False
