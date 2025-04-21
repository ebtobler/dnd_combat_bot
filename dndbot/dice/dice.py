from abc import ABC, abstractmethod
from random import randint

class Dice(ABC):

    @staticmethod
    @abstractmethod
    def roll(n: int):
        pass

    @staticmethod
    @abstractmethod
    def range():
        pass

    @staticmethod
    @abstractmethod
    def average_roll(n: int):
        pass


class D100(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 100) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 100

    @staticmethod
    def average_roll(n: int):
        pass


class D20(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 20) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 20

    @staticmethod
    def average_roll(n: int):
        pass


class D12(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 12) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 12

    @staticmethod
    def average_roll(n: int):
        pass


class D10(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 10) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 10

    @staticmethod
    def average_roll(n: int):
        pass


class D8(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 8) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 8

    @staticmethod
    def average_roll(n: int):
        pass


class D6(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 6) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 6

    @staticmethod
    def average_roll(n: int):
        pass


class D4(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [randint(1, 4) for _ in range(n)]

    @staticmethod
    def range():
        return 1, 4

    @staticmethod
    def average_roll(n: int):
        pass


class D1(Dice, ABC):

    @staticmethod
    def roll(n: int):
        return [1 for _ in range(n)]

    @staticmethod
    def range():
        return 1, 1

    @staticmethod
    def average_roll(n: int):
        return 1

"""
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

    @staticmethod
    def d1(n: int):
        return [1 for _ in range(n)]"""
