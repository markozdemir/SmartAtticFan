from datetime import datetime
from pytz import timezone
from dateutil import tz

# Convert time zone
east = timezone('US/Eastern')


def get_curr_time():
    now = datetime.utcnow()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    local_time = local.strftime("%Y/%m/%d, %H:%M:%S")
    l = extract(local_time)
    times = {}
    times["year"]       = l[0]
    times["month"]      = l[1]
    times["day"]        = l[2]
    times["hour"]       = l[3]
    times["minute"]     = l[4]
    times["second"]     = l[5]
    return times

def extract(current_time):
    parts = current_time.split(", ")
    times = parts[1].split(":")
    hour = times[0]
    minute = times[1]
    sec = times[2]

    days = parts[0].split("/")
    year = days[0]
    month = days[1]
    day = days[2]

    return int(year), int(month), int(day), int(hour), int(minute), int(sec)
