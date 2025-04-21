from abc import ABC, abstractmethod
from random import randint
from typing import Protocol


class Dice(Protocol):

    max: int
    average_roll: float

    @staticmethod
    @abstractmethod
    def roll(n: int):
        pass


class D100(Dice, ABC):

    max = 100
    average_roll = 50.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 100) for _ in range(n)]


class D20(Dice, ABC):

    max = 20
    average_roll = 10.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 20) for _ in range(n)]


class D12(Dice, ABC):

    max = 12
    average_roll = 6.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 12) for _ in range(n)]


class D10(Dice, ABC):

    max = 10
    average_roll = 5.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 10) for _ in range(n)]


class D8(Dice, ABC):

    max = 8
    average_roll = 4.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 8) for _ in range(n)]


class D6(Dice, ABC):

    max = 6
    average_roll = 3.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 6) for _ in range(n)]


class D4(Dice, ABC):

    max = 4
    average_roll = 2.5

    @staticmethod
    def roll(n: int):
        return [randint(1, 4) for _ in range(n)]


class D1(Dice, ABC):

    max = 1
    average_roll = 1

    @staticmethod
    def roll(n: int):
        return [1 for _ in range(n)]
