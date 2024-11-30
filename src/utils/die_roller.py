from .die import Die
from src.constants import evaluate_expression

from typing import Dict
import re


class Die_Roller:
    def __init__(self):
        self._dice: Dict[str, Die]
        self._dice = {}

    def roll(self, dice:str):
        command = dice
        result = re.finditer('(?P<num_rolls>\d*)(?P<die>d\d+)', command)
        for match in result:
            num_rolls = match.group('num_rolls')
            if num_rolls == '':
                num_rolls = 1
            else:
                num_rolls = int(num_rolls)
            die = match.group('die')

            if die not in self._dice.keys():
                self._dice[die] = Die(int(die[1:]))

            roll = self._dice[die].roll(rolls=num_rolls)

            command = command.replace(match.group(), str(roll))

        return evaluate_expression(command)