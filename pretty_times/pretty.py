from datetime import datetime, tzinfo, timedelta
from django.utils.translation import pgettext, ugettext as _


__all__ = ("date", )


class UTC(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=0, minutes=0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


def date(time):
    now = get_now(time)

    if time > now:
        past = False
        diff = time - now
    else:
        past = True
        diff = now - time

    days = diff.days

    if days is 0:
        return get_small_increments(diff.seconds, past)
    else:
        return get_large_increments(days, past)


def get_now(time):
    if time.tzinfo:
        utc = UTC()
    else:
        utc = None
    return datetime.now(utc)


def get_small_increments(seconds, past):
    if seconds < 10:
        result = _('just now')
    elif seconds < 60:
        result = _pretty_format(seconds, 1, _('seconds'), past)
    elif seconds < 120:
        result = past and _('a minute ago') or _('in a minute')
    elif seconds < 3600:
        result = _pretty_format(seconds, 60, _('minutes'), past)
    elif seconds < 7200:
        result = past and _('an hour ago') or _('in an hour')
    else:
        result = _pretty_format(seconds, 3600, _('hours'), past)
    return result


def get_large_increments(days, past):
    if days == 1:
        result = past and _('yesterday') or _('tomorrow')
    elif days < 7:
        result = _pretty_format(days, 1, _('days'), past)
    elif days < 14:
        result = past and _('last week') or _('next week')
    elif days < 31:
        result = _pretty_format(days, 7, _('weeks'), past)
    elif days < 61:
        result = past and _('last month') or _('next month')
    elif days < 365:
        result = _pretty_format(days, 30, _('months'), past)
    elif days < 730:
        result = past and _('last year') or _('next year')
    else:
        result = _pretty_format(days, 365, _('years'), past)
    return result


def _pretty_format(diff_amount, units, text, past):
    pretty_time = (diff_amount + units / 2) / units
    if past:
        base = pgettext(
            'Moment in the past',
            "%(amount)d %(quantity)s ago"
        )
    else:
        base = pgettext(
            'Moment in the future',
            "in %(amount)d %(quantity)s"
        )
    return base % dict(amount=pretty_time, quantity=text)
