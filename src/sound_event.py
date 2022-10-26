from dataclasses import dataclass


@dataclass
class SoundEvent:
    """Data Class for Sound Event Object"""
    intensity: float
    locationX: float
    locationY: float