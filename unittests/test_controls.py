import unittest
from api.libs.work_calendar import Workday, Workmonth
from api.db import models
from api import controls
from datetime import datetime, timedelta
import time


class TestControls(unittest.TestCase):

    def setUp(self) -> None:
        self.control = controls.Control(r"time_logs_dummy.db")
        self.control.model.add_record(year=2021,
                                      month=2,
                                      day=5,
                                      start_hour=7,
                                      start_minute=0,
                                      end_hour=15,
                                      end_minute=30)

    def test_control_can_read_start_time_from_database(self):
        self.control.create(2021, 2)
        obj_workmonth = self.control.months[2021, 2]
        obj_workday = obj_workmonth.workdays[2021, 2, 5]
        actual = obj_workday.start_time
        expected = datetime(2021, 2, 5, 7, 0)
        self.assertEqual(expected, actual)

    def test_control_can_read_end_time_from_database(self):
        self.control.create(2021, 2)
        obj_workmonth = self.control.months[2021, 2]
        obj_workday = obj_workmonth.workdays[2021, 2, 5]
        actual = obj_workday.end_time
        expected = datetime(2021, 2, 5, 15, 30)
        self.assertEqual(expected, actual)

    def test_control_can_read_worktime_from_database(self):
        self.control.create(2021, 2)
        obj_workmonth = self.control.months[2021, 2]
        obj_workday = obj_workmonth.workdays[2021, 2, 5]
        actual = obj_workday.worktime
        expected = timedelta(hours=8, minutes=30)
        self.assertEqual(expected, actual)

    def test_control_can_create_correct_number_of_days_in_march(self):
        self.control.create(2021, 3)
        obj_workmonth = self.control.months[2021, 3]
        actual = len(obj_workmonth.workdays)
        expected = 31
        self.assertEqual(expected, actual)

    def test_control_can_create_correct_number_of_days_in_february(self):
        self.control.create(2021, 2)
        obj_workmonth = self.control.months[2021, 2]
        actual = len(obj_workmonth.workdays)
        expected = 28
        self.assertEqual(expected, actual)

    def test_control_can_retrieve_workmonth(self):
        self.control.create(2021, 2)
        self.control.create(2021, 3)
        actual = self.control.retrieve(year=2021, month=2).month
        expected = Workmonth(2021, 2).month
        self.assertEqual(expected, actual)

    def test_control_can_retrieve_workday(self):
        self.control.create(2021, 2)
        self.control.create(2021, 3)
        actual = self.control.retrieve(year=2021, month=2, day=5).start_time
        expected = datetime(2021, 2, 5, 7, 0)
        self.assertEqual(expected, actual)

    def test_control_save_to_database(self):
        # check if cached changes in workmonth object
        # are saved to database via data model
        self.control.create(2021, 2)
        self.control.create(2021, 3)

        obj_workmonth = self.control.months[2021, 3]
        obj_workday = obj_workmonth.workdays[2021, 3, 15]
        obj_workday.start_time = (7, 30)
        obj_workday.end_time = (15, 30)

        self.control.save()

        actual = self.control.model.retrieve_record(2021, 3, 15)[1:]
        expected = ('20210315', 7, 30, 15, 30)

        self.assertEqual(expected, actual)

    def test_control_discard_change_not_saved_to_database(self):
        # check if cached changes are discarded
        # if database model is not called to store data
        self.control.create(2021, 2)
        self.control.create(2021, 3)

        obj_workmonth = self.control.months[2021, 3]
        obj_workday = obj_workmonth.workdays[2021, 3, 15]

        self.control.save()

        obj_workday.start_time = (7, 30)
        obj_workday.end_time = (15, 30)

        actual = self.control.model.retrieve_record(2021, 3, 15)[1:]
        expected = ('20210315', 7, 30, 15, 30)

        self.assertNotEqual(expected, actual)

    def test_control_edit_raises_error_if_no_month(self):
        # check if edit method raises key error
        # when attempting to edit nonexistent workmonth instance
        self.assertRaises(KeyError, self.control.edit, year=2005, month=12, day=1)

    def test_control_edit_changes_month(self):
        self.control.create(2021, 3)

        # edit the record
        self.control.edit(year=2021, month=3, day=15, start_time=(8, 30))

        # create compare object
        expected = datetime(2021, 3, 15, 8, 30)
        actual = self.control.retrieve(year=2021, month=3, day=15).start_time

        # assert
        self.assertEqual(expected, actual)
