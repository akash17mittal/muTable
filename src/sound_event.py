from dataclasses import dataclass


@dataclass
class SoundEvent:
    """Data Class for Tap Object"""
    intensity: float
    locationX: float
    locationY: float