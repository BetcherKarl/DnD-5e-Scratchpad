from .src.utils.die import Die

from typing import List, Union, Deque
import numpy as np
import matplotlib.pyplot as plt

def main():
    stat_generation_methods = [standard_5e,
                               drop_lowest,
                               abigails_method,
                               min_abigail,
                               drop_abigail]

    for roll_stats in stat_generation_methods:
        results = []
        totals = []
        for _ in range(30):
            rolls = roll_stats()
            results.append(rolls)
            totals.append(sum(rolls))






def drop_lowest(rolls):
    d6 = Die(sides=6)
    results = []
    for _ in range(7):
        rolls = d6.roll(rolls=5, summed=False)
        rolls.remove(min(rolls))
        results.append(sum(rolls))
    results.remove(min(results, key=lambda x: sum(x)))

    return results

def standard_5e():
    d6 = Die(sides=6)

    results = []
    for _ in range(6):
        rolls = d6.roll(rolls=4, summed=False)  # roll 4d6
        rolls.remove(min(rolls))  # drop lowest
        results.append(sum(rolls))

    return sorted(results)

def abigails_method():
    d6 = Die(sides=6)
    results = []
    for _ in range(7):
        rolls = d6.roll(rolls=4, summed=False)
        while 1 in rolls:
            min_indices = np.argmin(rolls)
            for index in min_indices:
                rolls[index] = d6.roll(rolls=1)

            results.append(rolls)
    results.remove(min(results, key=lambda x: sum(x)))
    return results

def min_abigail():
    d6 = Die(sides=6)
    results = []
    for _ in range(5):
        results.append([])
        for _ in range(6):
            rolls = d6.roll(rolls=3, summed=False)
            while 1 in rolls:
                for index in np.argmin(rolls):
                    rolls[index] = d6.roll()
                results[-1].append(rolls)

    return max(results, key=lambda x: sum(x))

def drop_abigail():
    d6 = Die(sides=6)
    results = []
    for _ in range(7):
        rolls = d6.roll(rolls=4, summed=False)
        rolls.remove(min(rolls))
        results.append(sum(rolls))
        while 1 in rolls:
            for index in np.argmin(rolls):
                rolls[index] = d6.roll()
    results.remove(min(results, key=lambda x: sum(x)))

    return results


