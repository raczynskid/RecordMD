import unittest
from api.libs.work_calendar import Workday, Workmonth
from datetime import datetime, timedelta


class TestWorkday(unittest.TestCase):

    def test_is_weekday_monday(self):
        wd = Workday(2021, 2, 1)
        self.assertEqual(True, wd.is_weekday())

    def test_date_getter(self):
        wd = Workday(2021, 2, 1)
        self.assertEqual(datetime(year=2021, month=2, day=1), wd.date)

    def test_start_date_setter(self):
        wd = Workday(2021, 2, 1)
        wd.start_time = 7, 0
        self.assertEqual(datetime(2021, 2, 1, 7, 0), wd.start_time)

    def test_end_date_setter(self):
        wd = Workday(2021, 2, 1)
        wd.end_time = 15, 30
        self.assertEqual(datetime(2021, 2, 1, 15, 30), wd.end_time)

    def test_worktime_getter(self):
        wd = Workday(2021, 2, 1)
        wd.start_time = 7, 0
        wd.end_time = 15, 30
        self.assertEqual(timedelta(hours=8, minutes=30), wd.worktime)

    def test_worktime_no_start_time(self):
        wd = Workday(2021, 2, 1)
        wd.end_time = 15, 30
        self.assertEqual(timedelta(), wd.worktime)

    def test_worktime_no_end_time(self):
        wd = Workday(2021, 2, 1)
        wd.start_time = 15, 30
        self.assertEqual(timedelta(), wd.worktime)

    def test_worktime_no_start_no_end_time(self):
        wd = Workday(2021, 2, 1)
        self.assertEqual(timedelta(), wd.worktime)


class TestWorkmonth(unittest.TestCase):

    def test_correct_number_of_days(self):
        wm = Workmonth(2021, 1)
        self.assertEqual(31, len(wm))

    def test_creates_workdays(self):
        wm = Workmonth(2021, 1)
        self.assertIsInstance(wm.workdays[0], Workday)

    def test_indexing(self):
        wm = Workmonth(2021, 1)
        self.assertEqual(Workday(2021, 1, 3).date, wm[3].date)


if __name__ == '__main__':
    unittest.main()
