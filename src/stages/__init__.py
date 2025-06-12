"""
Stages Package
==============

This package contains all stage classes for the game.
"""

from .battlefield import Battlefield
from .plains import Plains
from .base_stage import Stage, Platform, PlatformType
from .toybox_stage import ToyboxStage

__all__ = ['Battlefield', 'Plains', 'Stage', 'Platform', 'PlatformType'] 