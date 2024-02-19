# This is the class represented the Adapter Pattern

class Adaptee:
    def specific_request(self):
        return "Adaptee"


class Adapter:

    adaptee = ""

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()


client = Adapter(Adaptee())
print(client.request())
