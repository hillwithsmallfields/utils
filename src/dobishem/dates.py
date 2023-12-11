"""Some date and time handling functions."""

import datetime
import re

ISO_DATE = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
SLASHED_DATE = re.compile("[0-9]{4}/[0-9]{2}/[0-9]{2}")

def normalize_date(date_in):
    if ISO_DATE.match(date_in):
        return date_in
    if SLASHED_DATE.match(date_in):
        return date_in.replace('/', '-')
    return date_in

def as_datetime(date_in):
    return (date_in
            if isinstance(date_in, datetime.datetime)
            else (datetime.datetime.fromisoformat(datetime)
                  if isinstance(date_in, str)
                  else (datetime.datetime.combine(date_in, datetime.time())
                        if isinstance(date_in, datetime.date)
                        else date_in)))

def as_date(date_in):
    return (date_in
            if isinstance(date_in, datetime.date)
            else (datetime.date.fromisoformat(datetime)
                  if isinstance(date_in, str)
                  else (date_in.date
                        if isinstance(date_in, datetime.datetime)
                        else date_in)))

def back_from(when, years_back, months_back, days_back):
    if isinstance(when, str):
        when = datetime.date.fromisoformat(when)
    if months_back and months_back >= 12:
        years_back = (years_back or 0) + months_back // 12
        months_back %= 12
    if years_back:
        when = when.replace(year=when.year - years_back)
    if months_back:
        target_month = ((when.month - months_back)
                        if (when.month > months_back)
                        else ((when.month + 12) - months_back))
        target_year = (when.year
                       if months_back <= when.month
                       else (when.year - 1))
        max_day = calendar.monthrange(target_year, target_month)[1]
        if months_back >= when.month:
            when = when.replace(year=when.year - 1,
                                month=12 + when.month - months_back,
                                day=min(when.day, max_day))
        else:
            when = when.replace(month=when.month - months_back,
                                day=min(when.day, max_day))
    if days_back:
        when = when - datetime.timedelta(days=days_back)
    return when # datetime.datetime.combine(when, datetime.time())

def forward_from(when, years_forward, months_forward, days_forward):
    if isinstance(when, str):
        when = datetime.date.fromisoformat(when)
    if months_forward and months_forward >= 12:
        years_forward = (years_forward or 0) + months_forward / 12
        months_forward %= 12
    if years_forward:
        when = when.replace(year=when.year + years_forward)
    if months_forward:
        if months_forward + when.month >= 12:
            when = when.replace(year=when.year + 1, month=(when.month + months_forward) % 12)
        else:
            when = when.replace(month=when.month + months_forward)
    if days_forward:
        when = when + datetime.timedelta(days=days_forward)
    return when # datetime.datetime.combine(when, datetime.time())

later = datetime.timedelta(0, 1)

def yesterday():
    return back_from(datetime.date.today(), 0, 0, 1)
