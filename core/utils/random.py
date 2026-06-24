from random import randint


def roll_percentage(chance: int) -> bool:
    if not 1 <= chance <= 100:
        raise ValueError("chance must be between 1 and 100")
    return randint(1, 100) <= chance
