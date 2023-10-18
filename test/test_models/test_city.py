#!/usr/bin/python3
"""Defines unittests for models/city.py.
Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""

import contextlib
from datetime import datetime
from time import sleep
import os
import unittest

import models
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self) -> None:
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self) -> None:
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self) -> None:
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self) -> None:
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_name_is_public_class_attribute(self) -> None:
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_two_cities_unique_ids(self) -> None:
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self) -> None:
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self) -> None:
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self) -> None:
        dt_obj = datetime.now()
        dt_repr = repr(dt_obj)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt_obj
        cystr = str(city)
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn(f"'created_at': {dt_repr}", cystr)
        self.assertIn(f"'updated_at': {dt_repr}", cystr)

    def test_args_unused(self) -> None:
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_with_kwargs(self) -> None:
        dt_obj = datetime.now()
        dt_iso = dt_obj.isoformat()
        city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, dt_obj)
        self.assertEqual(city.updated_at, dt_obj)

    def test_instantiation_with_none_kwargs(self) -> None:
        with self.assertRaises(ValueError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUpClass(cls) -> None:
        with contextlib.suppress(IOError):
            os.rename("file.json", "tmp")

    @classmethod
    def tearDownClass(cls) -> None:
        with contextlib.suppress(IOError):
            os.remove("file.json")
        with contextlib.suppress(IOError):
            os.rename("tmp", "file.json")

    def test_one_save(self) -> None:
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_two_saves(self) -> None:
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_arg(self) -> None:
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self) -> None:
        city = City()
        city.save()
        cyid = f"City.{city.id}"
        with open("file.json", mode="r", encoding="utf-8") as file:
            self.assertIn(cyid, file.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self) -> None:
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self) -> None:
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self) -> None:
        city = City()
        city.middle_name = "Holberton"
        city.my_number = 98
        self.assertEqual("Holberton", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self) -> None:
        city = City()
        cy_dict = city.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self) -> None:
        dt_obj = datetime.now()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt_obj
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt_obj.isoformat(),
            'updated_at': dt_obj.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self) -> None:
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self) -> None:
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
