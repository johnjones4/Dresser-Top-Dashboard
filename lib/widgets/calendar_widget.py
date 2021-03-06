from lib.widget import Widget
from exchangelib import DELEGATE, Account, Credentials, EWSDateTime
from datetime import date, datetime
import pytz
import requests
from icalendar import Calendar, Event

class CalendarWidget(Widget):
  def __init__(self, font_size, font_path, inset, config):
    super().__init__("Calendar", font_size, font_path, inset, config)
    self.timezone = pytz.timezone(config["timezone"])
    self.calendars = config["calendars"]
    
  def generate_content(self, drawable, x, y, width, height):
    today = date.today()
    this_morning = datetime(today.year, today.month, today.day, 0, 0, 0, 0, self.timezone)
    this_evening = datetime(today.year, today.month, today.day, 23, 59, 59, 0, self.timezone)
    events = self.get_calendars(this_morning, this_evening)
    # min_datetime = events[0]["start"]
    # max_datetime = datetime(today.year, today.month, today.year, 0, 0, 0)
    # for event in events:
    #   if event["end"] > max:
    #     max_datetime = event["end"]
    start_hour = 8
    cutoff = 3
    morning = start_hour * 60 * 60
    evening = cutoff * 60 * 60
    seconds_to_pixels = (height - y - self.inset) / ((24 * 60 * 60) - morning - evening)
    for hour in range(25 - start_hour - cutoff):
      hour_y = y + self.inset + int(hour * 60 * 60 * seconds_to_pixels)
      drawable.line(((x,hour_y),(width,hour_y)), fill=127, width=1)
      real_hour = start_hour + hour
      if real_hour < 24 - cutoff:
        twelve_hour = real_hour % 12
        if twelve_hour == 0:
          twelve_hour = 12
        drawable.text((x, hour_y + (self.inset / 2)), "%d:00" % (twelve_hour), font=self.get_font(int(self.font_size * 0.75)))
    for event in events:
      start = event["start"].astimezone(self.timezone)
      end = event["end"].astimezone(self.timezone)
      start_secs = self.date_to_seconds(start) - morning
      end_secs = self.date_to_seconds(end) - morning
      event_y = y + self.inset + int(start_secs * seconds_to_pixels)
      event_y1 = y + self.inset + int(end_secs * seconds_to_pixels)
      drawable.rectangle(((x, event_y), (width, event_y1)), fill=0, outline=255, width=1)
      text = "%s %s" % (start.strftime("%-I:%M"), event["subject"])
      drawable.text((x + self.inset, event_y + self.inset), text, font=self.get_font(int(self.font_size * 0.75)), fill=255)
 
  def date_to_seconds(self, dt):
    return dt.second + (dt.minute * 60) + (dt.hour * 60 * 60)
  
  def get_calendars(self, this_morning, this_evening):
    events = []
    for calendar in self.calendars:
      if calendar["type"] == "exchange":
        credentials = Credentials(username=calendar["username"], password=calendar["password"])
        account = Account(primary_smtp_address=calendar["address"], credentials=credentials, autodiscover=True, access_type=DELEGATE)
        calendar_items = account.calendar.view(
          start=account.default_timezone.localize(EWSDateTime(this_morning.year, this_morning.month, this_morning.day, 0, 0, 0)),
          end=account.default_timezone.localize(EWSDateTime(this_morning.year, this_morning.month, this_morning.day, 23, 59, 59))
        )
        for calendar_item in calendar_items:
          events.append({
            "subject": calendar_item.subject,
            "start": calendar_item.start,
            "end": calendar_item.end
          })
      elif calendar["type"] == "ics":
        c = Calendar.from_ical(requests.get(calendar["url"]).text)
        for component in c.walk():
          if 'DTSTART' in component and 'DTEND' in component:
            start = None
            end = None
            if isinstance(component["DTSTART"].dt, datetime):
              start = component["DTSTART"].dt.astimezone(self.timezone)
              end = component["DTEND"].dt.astimezone(self.timezone)
              if end >= this_morning and start <= this_evening:
                events.append({
                  "subject": component["summary"],
                  "start": start,
                  "end": end
                })
      else:
        raise Exception("The calendar type \"%s\" is not supported." % (calendar["type"], ))
    events.sort(key=lambda event: event["start"])
    return events

