from http.client import NOT_EXTENDED
from icalendar import Calendar, Event
import datetime
from pytz import UTC # timezone

def getCalEvents(filename):
    calFile = open(filename, 'rb')
    cal = Calendar.from_ical(calFile.read())
    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary') if (component.get('summary')) else None
            start = component.get('dtstart').dt if (component.get('dtstart')) else None
            end = component.get('dtend').dt if (component.get('dtend')) else None
            created = component.get('dtstamp').dt if (component.get('dtstamp')) else None
            repeat = component.get('rrule')

            events.append({"summary": summary, "start": start, "end": end, "created": created, "repeat": repeat})
    
    calFile.close()
    return events

# get events from the past month of september
# at the time of writing this code the date was october 1, so we decided to run this on the past weeks events as a test
def getLastMonth(events):
    newEvents = []
    thisMonth = datetime.datetime.now().month
    lastMonth = thisMonth-1
    for event in events:
        if event['start'].month == lastMonth:
            newEvents.append(event)
    return newEvents

# 0 count weekday, starting from monday
# 0 monday, 1 tuedsya, 2 wed, 3 thu, 4 fri, 5 sat, 6 sunday
def getNextWeeklyEvent(origEvent, byday):
    conversion_dict = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    origStart = origEvent['start']
    origEnd = origEvent['end']

    origWeekday = origStart.weekday()
    # this is the byday array but converted to integers
    bydayAsNum = [conversion_dict[day] for day in byday]
    bydayAsNum.sort()

    # get the next number in the array bigger than origWeekday
    i = 0
    while i!=len(bydayAsNum) and bydayAsNum[i]<=origWeekday:
        i+=1
    
    if i==len(bydayAsNum):
        i = 0

    # get next start/end based on byday weekly repeat
    nextStart = origStart + datetime.timedelta( (bydayAsNum[i]-origStart.weekday()) % 7 )
    nextEnd = origEnd + datetime.timedelta( (bydayAsNum[i]-origEnd.weekday()) % 7 )

    return {"summary": origEvent['summary'], "start": nextStart, "end": nextEnd, "created": origEvent['created'], "repeat": origEvent['repeat']}


# process repeate events to add every instance onto the dict object
# max 100 repeats
def processRepeatedEvents(calEvents):
    newEvents = []
    for event in calEvents:
        if not event['repeat']:
            continue
        
        repeatData = event['repeat']
        freq = event['repeat']['FREQ']
        newEvents.append(event) # add original event to calendar

        # if weekly frequency, add 50 iterations
        if freq==["WEEKLY"]:
            if "BYDAY" in repeatData:
                print("<<<<EVENT: ", event)
                for iteration in range(50):
                    event = getNextWeeklyEvent(event, repeatData["BYDAY"])
                    newEvents.append(event)
                    print("---NEXT_EVENT: ", event)
    return newEvents

def main():
    pass

if __name__=="__main___":
    main()