import time
from datetime import datetime


def str2unix(date_string) -> int:
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    unix_time = time.mktime(date_object.timetuple())
    return int(unix_time)
