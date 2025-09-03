"""
Primitives package for DeepChem Server.

This package contains modularized primitive classes that inherit from a base Primitive class.
Each primitive implements the 'run' method to execute its specific functionality.
"""

from .base import Primitive
from .featurize import Featurize
from .train import Train
from .evaluate import Evaluate
from .infer import Infer

__all__ = [
    "Primitive",
    "Featurize",
    "Train",
    "Evaluate",
    "Infer",
]
