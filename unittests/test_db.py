import unittest
import sqlite3
from api.db import models


class TestDatabaseValidation(unittest.TestCase):
    def test_year_validation_correct_int(self):
        expected = "2020"
        actual = models.Validate.year(2020)
        self.assertEqual(expected, actual)

    def test_year_validation_incorrect_int(self):
        self.assertRaises(AttributeError, models.Validate.year, 202)

    def test_year_validation_correct_str(self):
        expected = "2020"
        actual = models.Validate.year("2020")
        self.assertEqual(expected, actual)

    def test_year_validation_incorrect_str(self):
        self.assertRaises(AttributeError, models.Validate.year, "202")

    def test_month_validation_correct_int(self):
        expected = "01"
        actual = models.Validate.month(1)
        self.assertEqual(expected, actual)

    def test_month_validation_incorrect_int(self):
        self.assertRaises(AttributeError, models.Validate.month, 13)

    def test_month_validation_correct_str(self):
        expected = "01"
        actual = models.Validate.month(1)
        self.assertEqual(expected, actual)

    def test_month_validation_incorrect_str(self):
        self.assertRaises(AttributeError, models.Validate.month, "13")

    def test_day_validation_correct_int(self):
        expected = "05"
        actual = models.Validate.day(5)
        self.assertEqual(expected, actual)

    def test_day_validation_incorrect_int(self):
        self.assertRaises(AttributeError, models.Validate.day, 32)

    def test_day_validation_correct_str(self):
        expected = "31"
        actual = models.Validate.day(31)
        self.assertEqual(expected, actual)

    def test_day_validation_incorrect_str(self):
        self.assertRaises(AttributeError, models.Validate.day, "33")

    def test_hour_validation_correct_int(self):
        expected = 23
        actual = models.Validate.hour(23)
        self.assertEqual(expected, actual)

    def test_hour_validation_incorrect_int(self):
        self.assertRaises(AttributeError, models.Validate.hour, 24)

    def test_hour_validation_correct_str(self):
        expected = 12
        actual = models.Validate.hour(12)
        self.assertEqual(expected, actual)

    def test_hour_validation_incorrect_str(self):
        self.assertRaises(AttributeError, models.Validate.hour, "25")

    def test_minute_validation_correct_int(self):
        expected = 23
        actual = models.Validate.minute(23)
        self.assertEqual(expected, actual)

    def test_minute_validation_incorrect_int(self):
        self.assertRaises(AttributeError, models.Validate.minute, 60)

    def test_minute_validation_correct_str(self):
        expected = 12
        actual = models.Validate.minute(12)
        self.assertEqual(expected, actual)

    def test_minute_validation_incorrect_str(self):
        self.assertRaises(AttributeError, models.Validate.minute, "321")

    def test_to_iso(self):
        expected = "20210112"
        actual = models.Validate.to_ISO(2021, 1, 12)
        self.assertEqual(expected, actual)


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = models.DB(r"time_logs_dummy.db")
        self.db.delete_all_records()
        self.db.add_record(year=2021, month=2, day=3, start_hour=7, start_minute=0)
        self.db.add_record(year=2021, month=2, day=4, start_hour=7, start_minute=0, end_hour=15, end_minute=30)
        self.db.add_record(year=2021, month=2, day=5, start_hour=7, start_minute=0, end_hour=15, end_minute=30)

    def test_database_retrieve_records(self):
        data = self.db.retrieve_all_records()
        rowcount_expected = 0
        for _ in data:
            rowcount_expected += 1
        self.assertEqual(rowcount_expected, 3)

    def test_database_delete_all_records(self):
        self.db.delete_all_records()
        data = self.db.retrieve_all_records()
        rowcount_expected = 0
        for _ in data:
            rowcount_expected += 1
        self.assertEqual(rowcount_expected, 0)

    def test_database_delete_record(self):
        self.db.delete_record(2021, 2, 5)
        data = self.db.retrieve_all_records()
        rowcount_expected = 0
        for _ in data:
            rowcount_expected += 1
        self.assertEqual(rowcount_expected, 2)

    def test_database_retrieve_record(self):
        actual = self.db.retrieve_record(2021, 2, 5)
        expected = (5, '20210205', 7, 0, 15, 30)
        self.assertEqual(expected, actual)

    def test_database_record_exists(self):
        exists = self.db.record_exists(2021, 2, 5)
        self.assertTrue(exists)

    def test_database_record_not_exists(self):
        exists = self.db.record_exists(2021, 2, 15)
        self.assertFalse(exists)

    def test_database_update_record(self):
        self.db.update_record(2021, 2, 3, end_hour=16, end_minute=30)
        data = self.db.retrieve_record(2021, 2, 3)
        expected = (3, '20210203', 7, 0, 16, 30)
        actual = [row for row in data][0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
