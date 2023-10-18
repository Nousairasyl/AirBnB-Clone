#!/usr/bin/python3
"""Define the state class"""

from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state

    Attributes:
        name (str): state name
    """
    name: str = ""
