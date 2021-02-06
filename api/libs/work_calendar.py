from datetime import datetime, timedelta
import calendar


class Workmonth:
    # container class for Workday objects
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.workdays = {}

    def save_to_database(self, model):
        # save all workday items into sqlite database according to the model
        for wd in self.workdays:
            if not model.record_exists(wd.date.year, wd.date.month, wd.date.day):
                model.add_record(year=wd.date.year,
                                 month=wd.date.month,
                                 day=wd.date.day,
                                 start_hour=wd.start_hour,
                                 start_minute=wd.start_minute,
                                 end_hour=wd.end_hour,
                                 end_minute=wd.end_minute
                                 )
            else:
                model.update_record(year=wd.date.year,
                                    month=wd.date.month,
                                    day=wd.date.day,
                                    start_hour=wd.start_hour,
                                    start_minute=wd.start_minute,
                                    end_hour=wd.end_hour,
                                    end_minute=wd.end_minute
                                    )

    def read_from_database(self, model):
        # create empty workdays, check for existing entries in database
        # update instance if record exists
        empty_workdays = [Workday(self.year, self.month, day)
                          for day in
                          calendar.Calendar().itermonthdays(self.year, self.month)
                          if day != 0]

        for wd in empty_workdays:
            if model.record_exists(wd.date.year, wd.date.month, wd.date.day):
                ix, dt_str, sh, sm, eh, em = model.retrieve_record(wd.date.year, wd.date.month, wd.date.day)
                wd.start_time = (sh, sm)
                wd.end_time = (eh, em)
            self.workdays[wd.date.year, wd.date.month, wd.date.day] = wd

    def __len__(self):
        # override len method
        # to match number of days in month
        return len(self.workdays)

    def __getitem__(self, index):
        # indexing days where index = day
        return self.workdays[index - 1]

    def __iter__(self):
        # allow iteration through object
        return WorkmonthIterator(self)


class WorkmonthIterator:
    def __init__(self, workmonth: Workmonth):
        self._workmonth = workmonth
        self._index = 0

    def __next__(self):
        if self._index < len(self._workmonth.workdays):
            self._index += 1
            return self._workmonth.workdays[self._index]
        raise StopIteration


class Workday:
    # base class for producing editable instances of workdays
    def __init__(self, year, month, day):
        self._record_date = datetime(year, month, day)
        self._start_time = None
        self._end_time = None

    @property
    def date(self):
        return self._record_date

    @property
    def weekday(self):
        return self.is_weekday()

    def is_weekday(self):
        if self._record_date.weekday() in (5, 6):
            return False
        return True

    def time_setup(self, new_time: tuple):
        hour, minute = new_time
        new_datetime = self._record_date.replace(hour=hour, minute=minute)
        return new_datetime

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, new_time: tuple):
        self._start_time = self.time_setup(new_time)

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, new_time: tuple):
        self._end_time = self.time_setup(new_time)

    @property
    def worktime(self) -> timedelta:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return timedelta()

    @property
    def start_hour(self):
        if self._start_time is not None:
            return self._start_time.hour
        return None

    @property
    def start_minute(self):
        if self._start_time is not None:
            return self._start_time.minute
        return None

    @property
    def end_hour(self):
        if self._end_time is not None:
            return self._end_time.hour
        return None

    @property
    def end_minute(self):
        if self._end_time is not None:
            return self._end_time.minute
        return None

    def __repr__(self):
        return f"Workday object for date {self._record_date.strftime('%d/%m/%Y')}\n" \
               f"Work started: {self.start_time}\n" \
               f"Work finished: {self.end_time}\n" \
               f"Total hours: {self.worktime}\n" \
               f"Weekday: {self.weekday}\n\n"
