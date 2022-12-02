from dataclasses import dataclass
from enum import Enum


class Hand(Enum):
    LEFT = 1
    RIGHT = 2


@dataclass
class Tap:
    """Data Class for Tap Object"""
    hand: Hand
    intensity: float
    checkHandLocation: bool
