from .die import Die
from src.constants import evaluate_expression

from typing import Dict, Union
import re

import logging


class Die_Roller:
    def __init__(self, dice: Union[type(None), Dict[str,Die]]=None):
        self._dice: Dict[str, Die]
        if dice is None:
            self._dice = {}
        elif isinstance(dice, dict):
            self._dice = dice
        else:
            logging.error(f"Invalid type for param dice: expected NoneType or Dict[str, Die], got {type(dice)} instead")
            logging.info("Exiting...")
            exit()

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