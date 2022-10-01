from parseICS import getCalEvents, getLastMonth, processRepeatedEvents
from dateutil import rrule
import datetime

shreyEvents = getCalEvents("shreyjoshi2004@gmail.com.ics")
nevinEvents = getCalEvents("nevingilday@gmail.com.ics")

nevinEvents = processRepeatedEvents(nevinEvents)
shreyEvents = processRepeatedEvents(shreyEvents)

shreyLastMonth = getLastMonth(shreyEvents)
nevinLastMonth = getLastMonth(nevinEvents)

def isFree(time, events):
    free = True
    for event in events:
        if time > event['start'] and time < event['end']:
            free = False
    return free

for event in shreyLastMonth:
    print(event)

whenBothFree = []
whenShreyFree = []
whenNevinFree = []

end = datetime.datetime.now(datetime.timezone.utc)
start = end - datetime.timedelta(days=7)
for dt in rrule.rrule(rrule.HOURLY, dtstart=start, until=end):
    shreyFree = isFree(dt, shreyLastMonth)
    nevinFree = isFree(dt, nevinLastMonth)
    if shreyFree and nevinFree:
        whenBothFree.append(dt)
    elif shreyFree and not nevinFree:
        whenShreyFree.append(dt)
    elif not shreyFree and nevinFree:
        whenNevinFree.append(dt)

for i in whenBothFree:
    print(i)