class Publisher:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.notify(message)

class Subscriber:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print(f"{self.name} received message: {message}")