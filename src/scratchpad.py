from utils.die_roller import Die_Roller
from utils.die import Die
from utils.probability import prob
from utils.creature import Creature
from src.constants import print_distribution

import logging

logging.basicConfig(level=logging.WARN)

roller = Die_Roller()

def main():
    # stuff = [10, 12, 15, 8, 14, 13]
    stuff = {"strength": 10,
             "dexterity": 12,
             "constitution": 15,
             "intelligence": 8,
             "wisdom": 14,
             "charisma": 13}
    creature = Creature(stuff, level=1)
    rolls = []

    for i in range(100):
        rolls.append(creature.roll('2d8 + 2'))
    logging.info(f"Successfully Created Creature")
    print(min(rolls))
    print(max(rolls))


if __name__ == '__main__':
    main()
