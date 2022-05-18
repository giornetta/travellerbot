from random import Random


def roll(dices: int = 1) -> int:
    n: int = 0

    for i in range(dices):
        n += Random().randint(1, 6)

    return n
