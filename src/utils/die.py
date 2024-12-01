from numpy.random import randint

from typing import List, Union, Deque
from collections import deque
from functools import lru_cache

class Die():
    def __init__(self, sides: int):
        self._sides = sides
        self._history = deque(maxlen=50)

    @property
    def sides(self):
        return self._sides

    @property
    def history(self):
        return self._history

    @property
    def last_roll(self) -> int:
        return self._history[-1]

    def roll(self, rolls=1, summed=True) -> Union[int, List[int]]:
        """Rolls the die (return random integer between 1 and sides (inclusive) )

        :param rolls: (int) number of times to roll the die
        :param summed: (bool) returns int sum of all rolls when True.
                              returns list of all rolls when False.

        :return: (int) sum total of all rolls OR
                 (List[int]) all rolls"""
        results = randint(1, self.sides+1, rolls)
        if summed:
            results = sum(results)
        self._history.append(results)
        return results
