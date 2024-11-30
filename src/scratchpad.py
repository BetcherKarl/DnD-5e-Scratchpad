from utils.die_roller import Die_Roller
from utils.die import Die
from utils.probability import prob
from utils.creature import Creature
from src.constants import print_distribution

import logging

logging.basicConfig(level=logging.WARN)

roller = Die_Roller()

def main():
    distribution = {}

    n = 2
    f = 6
    sample_size = 500000
    step = 0.01

    min_val = n
    max_val = n * f
    print("CALCULATED PROBABILITIES")
    temp = prob(None, n, f)

    for i in range(min_val, max_val + 1):
        distribution[i] = temp[i]

    print_distribution(distribution, step_size=step)

    logging.info(f"Testing creature creation...")
    # stuff = [10, 12, 15, 8, 14, 13]
    stuff = {"strength": 10,
             "dexterity": 12,
             "constitution": 15,
             "intelligence": 8,
             "wisdom": 14,
             "charisma": 13}
    creature = Creature(stuff)
    print(creature._stats)
    logging.info(f"Successfully Created Creature")

    print("\nEXPERIMENTAL RESULTS")
    # test data
    data = {i: 0 for i in range(min_val, max_val + 1)}
    die = Die(f)
    for _ in range(sample_size):
        roll = die.roll(rolls=n)
        data[roll] += 1
    # normalize the data
    for key in data.keys():
        data[key] /= sample_size

    print_distribution(data, step_size=step)


if __name__ == '__main__':
    main()
