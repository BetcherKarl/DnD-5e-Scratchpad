from scipy.signal import fftconvolve
from numpy import ndarray

from functools import lru_cache
from typing import Union, List

import logging

# logging.basicConfig(level=logging.DEBUG)

@lru_cache(maxsize=20, typed=False)
def prob(total: Union[int, type(None)], num_rolls: int, faces: int) -> Union[float, List[float]]:
    """Calculates the probability of rolling a given total when rolling (num_rolls)d(faces) Ex. 2d6, 3d12"""
    logging.info(f" src.utils.probability.prob: Calculating p({total}: {num_rolls}d{faces})...")
    # Error Checking
    errors = False
    if not (isinstance(total, int) or isinstance(total, type(None))):
        message = "\tparam total must be an integer or NoneType"
        logging.error(message)
        errors = True
    if not isinstance(num_rolls, int):
        message = "\tnum_rolls must be an integer"
        logging.error(message)
        errors = True
    if not isinstance(faces, int):
        message = "\tfaces must be an integer"
        logging.error(message)
        errors = True
    if errors:
        logging.info("Exiting...")
        exit()

    if num_rolls <= 0:
        message = "\tnum_rolls must be a positive integer"
        logging.error(message)
        errors = True
    if faces <= 0:
        message = "\tfaces must be a positive integer"
        logging.error(message)
        errors = True
    if not (total is None or num_rolls <= total <= num_rolls * faces):
        message = f"\ttotal is not between {num_rolls} (num_rolls) and {num_rolls * faces} (num_rolls * faces)"
        logging.error(message)
        errors = True
    if errors:
        logging.info("Exiting...")
        exit()

    # Base case: 1 die roll
    if num_rolls == 1:
        baseline = [0] + (faces * [1 / faces])
        if total is None:
            return baseline
        return baseline[1]

    down = num_rolls // 2
    up = num_rolls - down

    # Recursive step: Convolve p(t; floor(n/2), faces) & p(t; ceil(n/2), faces)
    distribution = fftconvolve(prob(None, up, faces), prob(None, down, faces))

    if total is None:
        return distribution
    else:
        return distribution[total]

