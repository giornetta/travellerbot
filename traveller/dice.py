from random import Random


def roll(dices: int = 1) -> int:
    sum: int = 0

    for i in range(dices):
        sum += Random().randint(1, 6)

    return sum
