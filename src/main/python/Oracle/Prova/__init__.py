class Class:
    def __init__(self, cosa_fa, cosa_fa2):
        print(cosa_fa)
        print(cosa_fa2)

    def woof(self):
        return "Abbaia"


class Class2:
    def __init__(self):
        Class().__init__("Abbaia", "Miagola")


#Class(Class2())
