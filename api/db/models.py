import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(e)

    return connection


class Validate:
    def __init__(self):
        pass

    @staticmethod
    def year(year):
        y = str(year)
        if len(y) != 4:
            raise AttributeError("Year value incorrect")
        return y

    @staticmethod
    def month(month):
        m = int(month)
        if m > 12:
            raise AttributeError("Month value incorrect")
        return str(m).zfill(2)

    @staticmethod
    def day(day):
        d = int(day)
        if d > 31:
            raise AttributeError("Day value incorrect")
        return str(d).zfill(2)

    @staticmethod
    def hour(hour):
        if hour is None:
            return "NULL"
        h = int(hour)
        if h > 23:
            raise AttributeError("Hour value incorrect")
        return h

    @staticmethod
    def minute(minute):
        if minute is None:
            return "NULL"
        m = int(minute)
        if m > 59:
            raise AttributeError("Minute value incorrect")
        return m

    @staticmethod
    def to_ISO(year, month, day):
        return Validate.year(year) + Validate.month(month) + Validate.day(day)


class DB:
    def __init__(self, path):
        self.path = path
        self.con = create_connection(self.path)

    def add_record(self, year, month, day, start_hour=None, start_minute=None, end_hour=None, end_minute=None):

        date = Validate.to_ISO(year, month, day)
        start_h = Validate.hour(start_hour)
        start_m = Validate.minute(start_minute)
        end_h = Validate.hour(end_hour)
        end_m = Validate.minute(end_minute)

        sql = f"""
        INSERT INTO
        time_logs (DATE, START_HOUR, START_MINUTE, END_HOUR, END_MINUTE)
        VALUES
        ('{date}', {start_h}, {start_m}, {end_h}, {end_m});
        """
        self.con.execute(sql)

    def retrieve_record(self, year, month, day):
        date = Validate.to_ISO(year, month, day)
        sql = f"SELECT * FROM time_logs WHERE DATE = {date};"
        return self.con.execute(sql)

    def delete_record(self, year, month, day):
        date = Validate.to_ISO(year, month, day)
        sql = f"DELETE FROM time_logs WHERE DATE = {date};"
        self.con.execute(sql)

    def update_record(self, year, month, day, **kwargs):
        date = Validate.to_ISO(year, month, day)
        update_string = ""
        for k, v in kwargs.items():
            update_partial = f"""{k.upper()} = {v} , """
            update_string += update_partial

        sql = f"""UPDATE time_logs SET
                  {update_string[:-3]}
                WHERE
                  DATE = {date};
                """

        self.con.execute(sql)

    def record_exists(self, year, month, day):
        date = Validate.to_ISO(year, month, day)
        sql = f"""SELECT EXISTS(SELECT 1 FROM time_logs WHERE DATE = {date});"""
        return bool([row for row in self.con.execute(sql)][0][0])

    def retrieve_all_records(self):
        sql = """SELECT * FROM time_logs"""
        return self.con.execute(sql)

    def delete_all_records(self):
        sql = """DELETE FROM time_logs"""
        self.con.execute(sql)