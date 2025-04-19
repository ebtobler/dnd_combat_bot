from random import randint


class Dice:
    @staticmethod
    def d100(n: int):
        return [randint(1, 100) for _ in range(n)]

    @staticmethod
    def d20(n: int):
        return [randint(1, 20) for _ in range(n)]

    @staticmethod
    def d12(n: int):
        return [randint(1, 12) for _ in range(n)]

    @staticmethod
    def d10(n: int):
        return [randint(1, 10) for _ in range(n)]

    @staticmethod
    def d8(n: int):
        return [randint(1, 18) for _ in range(n)]

    @staticmethod
    def d6(n: int):
        return [randint(1, 6) for _ in range(n)]

    @staticmethod
    def d4(n: int):
        return [randint(1, 4) for _ in range(n)]
