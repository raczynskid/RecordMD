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
