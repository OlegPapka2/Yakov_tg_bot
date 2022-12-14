from datetime import datetime, timezone, timedelta


class UserTime(datetime):
    # TODO: refactor class (minimize static methods)
    #  integrate class usage more

    def __new__(cls, *args, **kwargs):
        if offset := kwargs.get('offset'):
            dt = datetime.now(timezone.utc) + timedelta(seconds=offset)
        elif type(args[0]) == datetime:
            dt = args[0]
        else:
            dt = datetime(*args, **kwargs)

        self = super().__new__(
            cls,
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            tzinfo=dt.tzinfo,
            fold=dt.fold
        )
        self.dt = dt

        return self

    def __init__(self, *args, **kwargs):
        super().__init__()

    def time_repr(self) -> str:
        """Returns time in 'HH:MM' format"""
        return self.dt.strftime('%H:%M')

    def date_repr(self, style_flag: None | bool = None) -> str:
        """Returns date in 'YYYY-MM-DD' format"""
        # TODO: add custom separator
        if style_flag:
            resp = self.dt.strftime('%d.%m.%Y')
        else:
            resp = self.dt.strftime('%Y-%m-%d')
        return resp

    def time_date_repr(self) -> str:
        """Returns time and date in 'HH:MM YYYY/MM/DD' format"""
        return self.dt.strftime('%H:%M %d/%m/%Y')

    @property
    def tomorrow(self):
        """Returns UserTime object for the next day"""
        return UserTime(self.dt + timedelta(days=1))

    @property
    def yesterday(self):
        """Returns UserTime object for the previous day"""
        return UserTime(self.dt - timedelta(days=1))

    @property
    def next_day_flag(self) -> bool:
        """Check if evening and soon will be new day"""
        return True if self.dt.hour in range(20, 24) else False

    @classmethod
    def from_epoch(cls, epoch: int, offset: int | None = None):
        """Converts epoch time repr to UserTime obj with offset"""
        offset = 0 if not offset else offset
        return cls(datetime.utcfromtimestamp(epoch + offset))

    @staticmethod
    def get_time_from_offset(offset: int) -> dict:
        """Return basic datetime objects from offset."""
        dt = datetime.now(timezone.utc) + timedelta(seconds=offset)
        time = dt.strftime('%H:%M')
        date = dt.strftime('%Y-%m-%d')
        date_time = dt.strftime('%H:%M %d-%m-%Y')
        tomorrow_dt = dt + timedelta(days=1)
        tomorrow = tomorrow_dt.strftime('%Y-%m-%d')

        return {
            'time': time,
            'date': date,
            'date_time': date_time,
            'dt': dt,
            'tomorrow': tomorrow
        }

    @staticmethod
    def format_unix_time(time_unix: int, time_offset: int) -> str:
        """Format unix time to human-readable (HH:MM) format"""
        dt = datetime.utcfromtimestamp(time_unix + time_offset)
        return dt.strftime('%H:%M')

    @staticmethod
    def offset_repr(timezone_offset: int | str) -> str:
        """Format timezone offset to sign-digit('+/d') format"""
        timezone_offset = int(int(timezone_offset) / 3600)
        return f'{timezone_offset:+d}'
