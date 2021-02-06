from .libs import work_calendar as wc
from .db import models
from datetime import datetime


class Control:
    def __init__(self, db_path):
        self.model = models.DB(db_path)
        self.months = {}

    def create(self, year=datetime.now().year, month=datetime.now().month):
        self.months[year, month] = wc.Workmonth(year, month)
        self.months[year, month].read_from_database(self.model)

    def retrieve(self, year=datetime.now().year, month=datetime.now().month):
        return self.months[year, month]

    def save(self):
        pass

    def edit(self):
        pass
