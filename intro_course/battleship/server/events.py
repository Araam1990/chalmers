class Events:
    def __init__(self):
        self.subscribers = dict()

    def sub(self, event, fn):
        if not event in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(fn)

    def post(self, event, *data):
        if not event in self.subscribers:
            return
        for fn in self.subscribers[event]:
            fn(*data)

events = Events()