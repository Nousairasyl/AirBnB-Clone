#!/usr/bin/python3
"""Defines unittests for models/state.py.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""

import contextlib
import os
import unittest
from datetime import datetime
from time import sleep

import models
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self) -> None:
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self) -> None:
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self) -> None:
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self) -> None:
        st_inst = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st_inst))
        self.assertNotIn("name", st_inst.__dict__)

    def test_two_states_unique_ids(self) -> None:
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_two_states_different_created_at(self) -> None:
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_two_states_different_updated_at(self) -> None:
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(self) -> None:
        dt_inst = datetime.now()
        dt_repr = repr(dt_inst)
        st_inst = State()
        st_inst.id = "123456"
        st_inst.created_at = st_inst.updated_at = dt_inst
        ststr = str(st_inst)
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn(f"'created_at': {dt_repr}", ststr)
        self.assertIn(f"'updated_at': {dt_repr}", ststr)

    def test_args_unused(self) -> None:
        st_inst = State(None)
        self.assertNotIn(None, st_inst.__dict__.values())

    def test_instantiation_with_kwargs(self) -> None:
        date = datetime.now()
        dt_iso = date.isoformat()
        st_inst = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st_inst.id, "345")
        self.assertEqual(st_inst.created_at, date)
        self.assertEqual(st_inst.updated_at, date)

    def test_instantiation_with_none_kwargs(self) -> None:
        with self.assertRaises(ValueError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

    @classmethod
    def setUpClass(cls) -> None:
        with contextlib.suppress(IOError):
            os.rename("file.json", "tmp")

    def tearDown(self) -> None:
        with contextlib.suppress(IOError):
            os.remove("file.json")
        with contextlib.suppress(IOError):
            os.rename("tmp", "file.json")

    def test_one_save(self) -> None:
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def test_two_saves(self) -> None:
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def test_save_with_arg(self) -> None:
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self) -> None:
        state = State()
        state.save()
        stid = f"State.{state.id}"
        with open("file.json", "r", encoding="utf-8") as file:
            self.assertIn(stid, file.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self) -> None:
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self) -> None:
        st_inst = State()
        self.assertIn("id", st_inst.to_dict())
        self.assertIn("created_at", st_inst.to_dict())
        self.assertIn("updated_at", st_inst.to_dict())
        self.assertIn("__class__", st_inst.to_dict())

    def test_to_dict_contains_added_attributes(self) -> None:
        state = State()
        state.middle_name = "Holberton"
        state.my_number = 98
        self.assertEqual("Holberton", state.middle_name)
        self.assertIn("my_number", state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self) -> None:
        state = State()
        st_dict = state.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self) -> None:
        date = datetime.now()
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self) -> None:
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self) -> None:
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
