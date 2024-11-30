from src.utils.die import Die
from src.constants import ability_modifier, proficiency_bonus

from abc import abstractmethod, ABC
from typing import List, Union, Dict
import logging


class Creature(ABC):
    def __init__(self, stats: Union[List[int], Dict[str, int]]):
        logging.info(f"src.utils.creature: Creating Creature({stats})")
        self._dice = {"d4": Die(4),
                      "d6": Die(6),
                      "d8": Die(8),
                      "d12": Die(12),
                      "d20": Die(20)}
        self._stats = {}

        # Error Checking
        errors = False

        if len(stats) != 6:
            errors = True
            logging.error("\tstats must have exactly 6 elements, but got {len(stats)} instead")
        names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

        if isinstance(stats, list):
            for stat in stats:
                if not isinstance(stat, int):
                    errors = True
                    logging.error(f"\tInvalid stat in stats (list): {type(stat)}, expected int")
                if not (1 <= stat <= 30):
                    errors = True
                    logging.error(f"\tInvalid stat in stats (list): {stat}, value must be between 1 and 30")
            if errors:
                logging.info("Exiting...")
                exit()

            # No Errors, fill data in stats
            for i in range(6):
                self._stats[names[i]] = stats[i]

        elif isinstance(stats, dict):
            for key in stats.keys():
                if not isinstance(key, str):
                    errors = True
                    logging.error(f"\tInvalid key type in stats(Dict): {type(key)}, expected str")
            for value in stats.values():
                if not isinstance(value, int):
                    errors = True
                    logging.error(f"\tInvalid value type in stats(Dict): {type}")
                if not (1 <= value <= 30):
                    errors = True
                    logging.error(f"\tInvalid value in stats(Dict): {value} must be between 1 and 30")

            keys = list(stats.keys())
            for i in range(len(keys)):
                keys[i] = keys[i][:3].upper()

            # Check keys for validity
            if sorted(keys) != sorted(names):
                errors = True
                logging.error(f"\tInvalid keys in stats(Dict): {stats.keys()} converted into {keys}, expected {names}")

            if errors:
                logging.info("Exiting...")
                exit()

            # No Errors: fill in data
            for name in names:
                self._stats[name] = stats[list(stats.keys())[keys.index(name)]]

        else:
            logging.error(f"\tInvalid type for param stats: expected List[int] or Dict[str, int], got {type(stats)}")
            logging.info(f"\tExiting...")
            exit()


