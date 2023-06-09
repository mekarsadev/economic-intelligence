import time
from datetime import datetime


def datestring2unix(datestring: str) -> int:
    if type(datestring) == str:
        date_object = datetime.strptime(datestring, "%Y-%m-%d")
    else:
        date_object = datestring
    unix_timestamp = int(time.mktime(date_object.timetuple()))

    return unix_timestamp


class dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, dict2obj(b) if isinstance(b, dict) else b)
