import time
from datetime import datetime


def datestring2unix(datestring: str) -> int:
    if type(datestring) == str:
        date_object = datetime.strptime(datestring, "%Y-%m-%d")
    else:
        date_object = datestring
    unix_timestamp = int(time.mktime(date_object.timetuple()))

    return unix_timestamp
