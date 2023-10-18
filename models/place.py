#!/usr/bin/python3
"""Define the place class"""

from typing import List
from models.base_model import BaseModel


class Place(BaseModel):
    """Represents a place

    Attributes:
        city_id (str): city id
        user_id (str): user id
        name (str): state name
        description (str): place description
        number_rooms (int): room's number
        number_bathrooms (int): number of bathrooms
        max_guest (int): maximum guest
        price_by_night (int): price by night
        latitude (float): latitude of the place
        longitude (float): longitude of the place
        amenity_ids (str): amenity id
    """
    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: List[str] = []
