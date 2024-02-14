import os, copy

from os import close

from os import close, curdir

from Objects.VariableObject import VariableObject

x = 10

# Numeri a virgola mobile
y = 20.5

# Stringhe
s = "Ciao, mondo!"

# Liste
lista = [1, 2, 3, 4, 5]

# Tuple
tupla = (1, 2, 3, 4, 5)

# Dizionari
dizionario = {"chiave": "valore"}

# Set
insieme = {1, 2, 3, 4, 5}

# Booleani
vero = True
falso = False

# None (equivale a null in altri linguaggi)
n = None


# Constructor
def __init__():
    x = 10


def pippoa():
    x = 10


def pluto(arg):
    x = 10


def pippo2(arg, arg2) -> None:
    x = 10


def pluto2(arg, arg2):
    x = 10
    return x


def paperino(arg, arg2) -> str:
    return "quack"


def paperino4(arg, arg2) -> str:
    x = arg
    return x


def paperino3(arg, arg2) -> int:
    return 10


def paperino2(arg, arg2):
    import os, copy
    from os import close
    from os import close, curdir
    from Objects.VariableObject import VariableObject
    x = 10
    y = x
    z = arg
    return "quack"


class Class:
    pass


class Class3:
    import os, copy
    from os import close
    from os import close, curdir
    from Objects.VariableObject import VariableObject

    x = 10

    # Numeri a virgola mobile
    y = 20.5

    # Stringhe
    s = "Ciao, mondo!"

    # Liste
    lista = [1, 2, 3, 4, 5]

    # Tuple
    tupla = (1, 2, 3, 4, 5)

    # Dizionari
    dizionario = {"chiave": "valore"}

    # Set
    insieme = {1, 2, 3, 4, 5}

    # Booleani
    vero = True
    falso = False

    # None (equivale a null in altri linguaggi)
    n = None

    def __init__(self):
        x = 10

    def pippo(self):
        x = 10

    def pluto(self, arg):
        x = 10

    def pippo2(self, arg, arg2) -> None:
        x = 10

    def pluto2(self, arg, arg2):
        x = 10
        return x

    def paperino(self, arg, arg2) -> str:
        return "quack"

    def paperino4(self, arg, arg2) -> str:
        x = arg
        return x

    def paperino3(self, arg, arg2) -> int:
        return 10

    def paperino2(self, arg, arg2):
        import os, copy
        from os import close
        from os import close, curdir
        from Objects.VariableObject import VariableObject
        x = 10

        # Numeri a virgola mobile
        y = 20.5

        # Stringhe
        s = "Ciao, mondo!"

        # Liste
        lista = [1, 2, 3, 4, 5]

        # Tuple
        tupla = (1, 2, 3, 4, 5)

        # Dizionari
        dizionario = {"chiave": "valore"}

        # Set
        insieme = {1, 2, 3, 4, 5}

        # Booleani
        vero = True
        falso = False

        # None (equivale a null in altri linguaggi)
        n = None

        pippo_ = os.getcwd()

        pippo = list()

        self.x = 10

        # Numeri a virgola mobile
        self.y = 20.5

        # Stringhe
        self.s = "Ciao, mondo!"

        # Liste
        self.lista = [1, 2, 3, 4, 5]

        # Tuple
        self.tupla = (1, 2, 3, 4, 5)

        # Dizionari
        self.dizionario = {"chiave": "valore"}

        # Set
        self.insieme = {1, 2, 3, 4, 5}

        # Booleani
        self.vero = True
        self.falso = False

        # None (equivale a null in altri linguaggi)
        self.n = None

        self.pippo_ = os.getcwd()
        self.pippo = list()
        print("x")
        print("x", "y")
        print("x", "y", "z")
        print(x)
        print(x, y, s)
        print(os.getcwd())
        print(os.getcwd().split(""))
        print(os.getcwd().split("x").append("x"))
        print(os.path.split("x"))
        print(os.getcwd(), os.getcwd())
        print(os.getcwd().split("x"), os.getcwd().split("x"))
        print(x)
        print(x, "y")
        print(x, os.getcwd())
        print(x, os.getcwd().split("x"))
        os.getcwd()
        os.getcwd().split("x")
        os.getcwd().split("x").append("x")
        os.path.split("x").count("x")
        # os.getcwd().split(os.getcwd().split("x")[0])
        Class3().paperino("Quack", "Quack")
        Class3.paperino("Quack", "Quack")
        Class3.pluto("Woof")
        Class3().pluto("Woof")
        Class3.pluto(Class3.paperino("Quack", "Quack"))
        Class3().pluto(Class3.paperino("Quack", "Quack"))
        # class3 = Class3()
        return "quack"

    ciccio = vero
    pippo_ = os.getcwd()
    list_ = list()
    print("x")
    print("x", "y")
    print("x", "y", "z")
    print(x)
    print(x, y, s)
    print(os.getcwd())
    print(os.getcwd().split(""))
    print(os.getcwd().split("x").append("x"))
    print(os.path.split("x"))
    print(os.getcwd(), os.getcwd())
    print(os.getcwd().split("x"), os.getcwd().split("x"))
    print(x)
    print(x, "y")
    print(x, os.getcwd())
    print(x, os.getcwd().split("x"))
    os.getcwd()
    os.getcwd().split("x")
    os.getcwd().split("x").append("x")
    os.path.split("x").count("x")
    # os.getcwd().split(os.getcwd().split("x")[0])


class Class2:
    Class3().paperino("Quack", "Quack")
    Class3.paperino("Quack", "Quack")
    Class3.pluto("Woof")
    Class3().pluto("Woof")
    Class3.pluto(Class3.paperino("Quack", "Quack"))
    Class3().pluto(Class3.paperino("Quack", "Quack"))
    # class3 = Class3()


ciccio = vero

pippo = os.getcwd()

list_ = list()

# numeri = [i for i in range(10)]

print("x")
print("x", "y")
print("x", "y", "z")
print(x)
print(x, y, s)
print(os.getcwd())
print(os.getcwd().split(""))
print(os.getcwd().split("x").append("x"))
print(os.path.split("x"))
print(os.getcwd(), os.getcwd())
print(os.getcwd().split("x"), os.getcwd().split("x"))
print(x)
print(x, "y")
print(x, os.getcwd())
print(x, os.getcwd().split("x"))
os.getcwd()
os.getcwd().split("x")
os.getcwd().split("x").append("x")
os.path.split("x").count("x")
# os.getcwd().split(os.getcwd().split("x")[0])
Class3().paperino("Quack", "Quack")
Class3.paperino("Quack", "Quack")
Class3.pluto("Woof")
Class3().pluto("Woof")
Class3.pluto(Class3.paperino("Quack", "Quack"))
Class3().pluto(Class3.paperino("Quack", "Quack"))
# class3 = Class3()
