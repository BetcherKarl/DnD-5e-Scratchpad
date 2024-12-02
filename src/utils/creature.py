from src.utils.die import Die
from src.utils.die_roller import Die_Roller
from src.constants import ability_modifier, proficiency_bonus

from abc import abstractmethod, ABC
from typing import List, Union, Dict
from functools import lru_cache
import logging
from math import floor


class Creature(ABC):
    def __init__(self, stats: Union[List[int], Dict[str, int]], level: int, speed: int = 30, max_hp: int = 0):
        logging.info(f"src.utils.creature: Creating Creature({stats})")
        self._dice = {"d4": Die(4),
                      "d6": Die(6),
                      "d8": Die(8),
                      "d12": Die(12),
                      "d20": Die(20)}
        self._roller = Die_Roller(dice=self._dice)
        self._stats = {}
        self._saving_prof = {"STR": 0,
                             "DEX": 0,
                             "CON": 0,
                             "INT": 0,
                             "WIS": 0,
                             "CHA": 0}
        self._skills = {"Acrobatics": ("DEX", 0),
                        "Animal Handling": ("WIS", 0),
                        "Arcana": ("INT", 0),
                        "Athletics": ("STR", 0),
                        "Deception": ("CHA", 0),
                        "History": ("INT", 0),
                        "Insight": ("WIS", 0),
                        "Intimidation": ("CHA", 0),
                        "Investigation": ("INT", 0),
                        "Medicine": ("WIS", 0),
                        "Nature": ("INT", 0),
                        "Perception": ("WIS", 0),
                        "Performance": ("CHA", 0),
                        "Persuasion": ("CHA", 0),
                        "Sleight of Hand": ("DEX", 0),
                        "Stealth": ("DEX", 0),
                        "Survival": ("WIS", 0)}

        self._death_saves = {1: 0,
                             -1: 0}

        # Error Checking
        errors = False

        if not isinstance(max_hp, int):
            errors = True
            logging.error(f"max_hp must be an integer, not {type(max_hp)}")
        elif max_hp > 0:
            errors = True
            logging.error(f"max_hp must be a positive integer, not {max_hp}")

        if not isinstance(speed, int):
            errors = True
            logging.error(f"Invalid speed type: expected int, got {type(speed)}")
        elif speed < 0 or speed % 5 != 0:
            errors = True
            logging.error(f"Invalid speed value: expected a non-negative int divisible by 5, got {speed}")

        if not (1 <= level <= 30):
            errors = True
            logging.error(f"\tInvalid level: {level}, must be between 1 and 30")

        if len(stats) != 6:
            errors = True
            logging.error("\tstats must have exactly 6 elements, but got {len(stats)} instead")

        if errors:
            logging.info("Exiting...")
            exit()

        self._level = level
        self._speed = speed
        self._max_hp = max_hp
        self._current_hp = self._max_hp
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

        logging.info("Stats values have been set")

    @property
    def proficiency_bonus(self):
        return proficiency_bonus[self._level]

    @property
    def level(self):
        return self._level

    @property
    def stats(self):
        return self._stats

    @property
    def speed(self):
        return self._speed

    def ability_mod(self, key: str) -> int:
        return ability_modifier[self._stats[key]]

    def roll_skill(self, skill: str):
        roll = self._dice["d20"].roll()
        if skill in self._stats.keys():
            return roll + ability_modifier[self._stats[skill]]
        if skill in self._skills.keys():
            base_stat = self._skills[skill][0]
            prof = self._skills[skill][1]
            return roll + self.ability_mod(base_stat) + floor(prof * self.proficiency_bonus)
        logging.error(f"\tInvalid skill: {skill}, not found in self._skills.keys() or self._stats.keys()")
        logging.info(f"\tExiting...")
        exit()

    def roll_save(self, ability: str):
        if ability.lower() == 'death':
            return self.roll_skill('CON')
        return self.roll_skill(ability) + floor(self._saving_prof[ability] * self.proficiency_bonus)

    def roll(self, command:str):
        if isinstance(command, str):
            return self._roller.roll(command)

    def make_death_save(self, dc: int = 10):
        logging.info(f"Creature making death save with DC {dc}")
        if not isinstance(dc, int) or dc <= 0:
            logging.warning(f"\tDeath Save DC must a positive integer. DC reset to default 10.")
            dc = 10
        if self._current_hp == 0:
            roll = self.roll_save('death')
            logging.info(f"Creature rolled {roll}")
            if roll >= dc + 10:
                self._death_saves[1] = 3
            elif roll <= dc - 10:
                self._death_saves[-1] += 2
            elif roll >= dc:
                self._death_saves[1] += 1
            else:
                self._death_saves[-1] += 1

            if self._death_saves[-1] >= 3:
                self._die()
            elif self._death_saves[1] >= 3:
                self._death_saves = {1: 0,
                                     -1: 0}

        else:
            logging.warning(f"\tOnly make a death save at zero HP, currently at {self._current_hp}")

    def _die(self):
        raise NotImplementedError()